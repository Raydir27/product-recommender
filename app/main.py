from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import analyze, generate_description, recommend_og
from .routes.recommend import router as recommend_router, init_pinecone_client
import logging

# Configure logging for proper error handling, as the original code was suppressing errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic (code before yield)
    try:
        # Initialize the Pinecone client imported from the recommend module
        logger.info("Initializing Pinecone client...")
        init_pinecone_client()
        logger.info("Pinecone client initialized successfully.")
    except Exception as e:
        # Log the error, but let the app start (to maintain original behavior)
        logger.error(f"Failed to initialize Pinecone client: {e}")
        pass

    # The 'yield' signals that the application is ready and can start serving requests
    yield

    # Shutdown logic (code after yield)
    # Add any cleanup code here if necessary, e.g., closing a connection pool.
    logger.info("Application shutdown complete.")


# Initialize FastAPI with the lifespan context manager
app = FastAPI(title="Ikarus Product Recommendation API", lifespan=lifespan)

# Allow local frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(recommend_router, prefix="/api/recommend", tags=["recommend"])
app.include_router(recommend_og.router, prefix="/api/recommend/legacy", tags=["recommend-legacy"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["analyze"])
app.include_router(generate_description.router, prefix="/api/generate_description", tags=["generate_description"])

@app.get("/")
async def root():
    return {"status": "ok", "service": "ikarus-recommend"}