# routes/recommend.py
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import numpy as np
from sentence_transformers import SentenceTransformer
import logging
from pinecone import Pinecone
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter()

# --------- Request / Response models ----------
class RecommendRequest(BaseModel):
    prompt: str
    top_k: Optional[int] = 5
    namespace: Optional[str] = None

class MatchItem(BaseModel):
    id: str
    score: float
    metadata: Optional[Dict[str, Any]] = None

class RecommendResponse(BaseModel):
    prompt: str
    top_k: int
    results: List[MatchItem]

# --------- Startup: load model + init Pinecone client ----------
# Environment / config expected:
# PINECONE_API_KEY, PINECONE_ENV, PINECONE_INDEX_NAME, optionally PINECONE_INDEX_HOST
API_KEY = os.getenv("PINECONE_API_KEY")
ENV = os.getenv("PINECONE_ENV")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
INDEX_HOST = os.getenv("PINECONE_INDEX_HOST")  # optional: host string used by some client variants
NAMESPACE=os.getenv("PINECONE_NAMESPACE")

if not API_KEY or not ENV:
    logger.warning("PINECONE_API_KEY or PINECONE_ENV not set. Set env vars or supply them securely.")

# Load embedding model once (heavy operation)
MODEL_NAME = os.getenv("EMBEDDING_MODEL")
logger.info(f"Loading SentenceTransformer model: {MODEL_NAME}")
sbert = SentenceTransformer(MODEL_NAME)

# Init Pinecone client (attempt new-style, be resilient)
pc = Pinecone(api_key=API_KEY, environment=ENV)
index_obj = None

def init_pinecone_client():
    global pc, index_obj, sbert
    
    try:
        if sbert is None:
            sbert = SentenceTransformer(MODEL_NAME)
            logger.info("SentenceTransformer model loaded successfully.")
    except Exception as e:
        logger.error("Failed to load SentenceTransformer model: %s", e)

    try:
        from pinecone import Pinecone
        pc = Pinecone(api_key=API_KEY, environment=ENV)
        logger.info("Connected to Pinecone using new Pinecone(...) client.")
    except Exception as e_new:
        logger.warning("New Pinecone client import failed: %s", e_new)
        try:
            import pinecone as pinecone_legacy
            pinecone_legacy.init(api_key=API_KEY, environment=ENV)
            pc = pinecone_legacy
            logger.info("Connected using legacy pinecone client.")
        except Exception as e_legacy:
            logger.error("Failed to initialise any Pinecone client: %s | %s", e_new, e_legacy)
            raise RuntimeError("Pinecone client init failed.") from e_legacy

    # Now create/get index object. Try multiple patterns seen in docs:
    try:
        # Prefer host-based Index if INDEX_HOST provided (per your ipynb / docs)
        if INDEX_HOST:
            try:
                index_obj = pc.Index(host=INDEX_HOST)  # some versions expect host
                logger.info("Indexed with pc.Index(host=INDEX_HOST)")
                return
            except Exception as e:
                logger.info("pc.Index(host=...) failed; will try other patterns: %s", e)

        # Try named index access (some variations)
        try:
            index_obj = pc.Index(INDEX_NAME)
            logger.info("Indexed with pc.Index(INDEX_NAME)")
            return
        except Exception as e:
            logger.info("pc.Index(INDEX_NAME) failed: %s", e)

        # Legacy style: pc.index(name)
        try:
            index_obj = pc.index(INDEX_NAME)
            logger.info("Indexed with pc.index(INDEX_NAME)")
            return
        except Exception as e:
            logger.info("pc.index(INDEX_NAME) failed: %s", e)

        raise RuntimeError("Could not obtain Pinecone Index object using known patterns.")
    except Exception as e:
        logger.exception("Error creating index object: %s", e)
        raise

# Initialise at import time
try:
    init_pinecone_client()
except Exception as e:
    logger.error("Pinecone init failed at startup: %s", e)
    # do not raise here to allow service to start — endpoint will return 500 if pc/index missing

# --------- Helper utilities ----------
def embed_and_normalize(text: str) -> np.ndarray:
    vec = sbert.encode([text], convert_to_numpy=True, show_progress_bar=False)[0]
    norm = np.linalg.norm(vec)
    if norm == 0:
        return vec
    return vec / norm

def parse_matches(resp) -> List[Dict[str, Any]]:
    """
    Parse different response shapes from Pinecone clients into a consistent list of dicts:
    each dict: { 'id': str, 'score': float, 'metadata': dict|None }
    """
    matches = []
    # Common shapes:
    # - resp.matches (list of objects)
    # - resp['matches'] (dict returned)
    # - resp.get('results') with nested matches
    try:
        if hasattr(resp, "matches"):
            raw_matches = resp.matches
        elif isinstance(resp, dict) and "matches" in resp:
            raw_matches = resp["matches"]
        elif isinstance(resp, dict) and "results" in resp:
            # some wrappers put results -> matches
            raw_matches = resp["results"][0].get("matches", [])
        else:
            raw_matches = []
    except Exception:
        raw_matches = []

    for m in raw_matches:
        if isinstance(m, dict):
            mid = m.get("id")
            score = m.get("score") or m.get("similarity") or None
            metadata = m.get("metadata")
        else:
            # object-like
            mid = getattr(m, "id", None)
            score = getattr(m, "score", None) or getattr(m, "similarity", None)
            metadata = getattr(m, "metadata", None)
        matches.append({"id": mid, "score": score, "metadata": metadata})
    return matches

# --------- Endpoint ----------
@router.post("/query", response_model=RecommendResponse, summary="Query Pinecone index for recommendations")
def recommend(req: RecommendRequest):
    if pc is None or index_obj is None:
        raise HTTPException(status_code=500, detail="Pinecone client/index not initialised on server. Check logs.")

    if not req.prompt or req.prompt.strip() == "":
        raise HTTPException(status_code=400, detail="prompt must be a non-empty string")

    # Embed and normalize
    try:
        qvec = embed_and_normalize(req.prompt)
    except Exception as e:
        logger.exception("Embedding failed: %s", e)
        raise HTTPException(status_code=500, detail="Failed to embed prompt")

    # Convert to python list for the client
    vect_list = qvec.tolist()

    # Build query args
    query_kwargs = {
        "vector": vect_list,
        "top_k": req.top_k,
        "include_values": False,
        "include_metadata": True,
    }
    if req.namespace:
        query_kwargs["namespace"] = req.namespace

    # Query index (handle different client method signatures)
    try:
        # many clients: index_obj.query(vector=..., top_k=..., include_metadata=True, ...)
        resp = None
        try:
            resp = index_obj.query(**query_kwargs)
        except TypeError:
            # some clients name parameters differently (topK or includeMetadata)
            alt_kwargs = {
                "vector": vect_list,
                "topK": req.top_k,
                "includeMetadata": True,
                "includeValues": False,
            }
            if req.namespace:
                alt_kwargs["namespace"] = req.namespace
            resp = index_obj.query(**alt_kwargs)
    except Exception as e:
        logger.exception("Pinecone query failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Pinecone query error: {str(e)}")

    matches = parse_matches(resp)
    # Convert raw scores to floats and ensure metadata is JSON-serializable
    cleaned = []
    for m in matches:
        try:
            score = float(m["score"]) if m.get("score") is not None else None
        except Exception:
            score = None
        cleaned.append(MatchItem(id=str(m.get("id")), score=score, metadata=m.get("metadata")))

    return RecommendResponse(prompt=req.prompt, top_k=req.top_k, results=cleaned)
