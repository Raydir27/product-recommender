from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
async def dataset_summary():
    # placeholder: return fake analytics summary
    return {
        "total_items": 2345,
        "unique_categories": 12,
        "top_categories": [
            {"category": "Chairs", "count": 540},
            {"category": "Tables", "count": 420}
        ]
    }
