from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.gemini_service import generate_suggestions
router = APIRouter(tags=["ai"]) 

class FreeWindow(BaseModel):
    start: str  # ISO 8601 with timezone, e.g. "2025-10-05T14:00:00-07:00"
    end: str

class SuggestionIn(BaseModel):
    location: str
    preferences: List[str] = []
    freeWindows: List[FreeWindow] = []

# makes sure our servers are mounted
@router.get("/ping")
def ping():
    return {"ok": True}

@router.post("/suggest")
def suggest(body: SuggestionIn):
    try:
        return generate_suggestions(
            location=body.location,
            preferences=body.preferences,
            free_windows=[{"start": w.start, "end": w.end} for w in body.freeWindows],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))