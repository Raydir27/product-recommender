from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class GenReq(BaseModel):
    title: str
    # brand: str = None
    brand: str | None = None

@router.post("/create")
async def generate_description(req: GenReq):
    # placeholder: simple templated description
    brand = req.brand or "Our Collection"
    desc = f"{req.title} — an elegant piece from {brand}. Crafted to blend form and function."
    return {"title": req.title, "description": desc}
