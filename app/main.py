from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import recommend, analyze, generate_description

app = FastAPI(title="Product Recommendation API (skeleton)")

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

app.include_router(recommend.router, prefix="/api/recommend", tags=["recommend"])
app.include_router(analyze.router, prefix="/api/analyze", tags=["analyze"])
app.include_router(generate_description.router, prefix="/api/generate_description", tags=["generate_description"])

@app.get("/")
async def root():
    return {"status": "ok", "service": "product-recommendation-api"}
