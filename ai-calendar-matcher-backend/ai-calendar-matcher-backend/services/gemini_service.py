import os, json
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-1.5-flash"

SCHEMA = {
  "type":"array",
  "items":{
    "type":"object",
    "properties":{
      "windowStart":{"type":"string"},
      "windowEnd":{"type":"string"},
      "title":{"type":"string"},
      "description":{"type":"string"},
      "durationMinutes":{"type":"integer"},
      "estimatedCostPerPerson":{"type":"string","enum":["$","$$","$$$"]},
      "indoorOutdoor":{"type":"string","enum":["indoor","outdoor","either"]},
      "bookingRecommended":{"type":"boolean"},
      "category":{"type":"string"},
      "notes":{"type":"string"}
    },
    "required":["windowStart","windowEnd","title","durationMinutes"],
    "additionalProperties":False
  }
}


def _prompt(location: str, preferences: List[str], free_windows: List[dict]) -> str:
    return (
        "You are a group activity planner.\n"
        "Return ONLY JSON matching the schema. One suggestion per free window.\n"
        f"Location: {location}\n"
        f"Preferences: {preferences}\n"
        f"Free windows (ISO): {free_windows}\n"
    )

def generate_suggestions(*, location: str,
                         preferences: List[str],
                         free_windows: List[dict]) -> List[dict]:
    model = genai.GenerativeModel(
        MODEL,
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": SCHEMA,
        },
    )
    resp = model.generate_content(_prompt(location, preferences, free_windows))
    try:
        return json.loads(resp.text)
    except Exception:
        return []
