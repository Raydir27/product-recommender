from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class RecommendRequest(BaseModel):
    user_prompt: str
    top_k: int = 5

class Product(BaseModel):
    uniq_id: str
    title: str
    score: float

@router.post("/query")
async def recommend(req: RecommendRequest):
    # placeholder demo logic: returns dummy recommendations
    demo = [
        {"uniq_id": "p1", "title": "Wooden Chair - Modern", "score": 0.95},
        {"uniq_id": "p2", "title": "Minimalist Coffee Table", "score": 0.88},
    ]
    return {"prompt": req.user_prompt, "top_k": req.top_k, "recommendations": demo[:req.top_k]}
