import os, json
from typing import List
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest")  # <= change here

def _prompt(location: str, preferences: List[str], free_windows: List[dict]) -> str:
    return (
        "You are a group activity planner.\n"
        "Return ONLY JSON (an array). One suggestion per free window.\n"
        "Each item must include: windowStart, windowEnd, title, durationMinutes.\n"
        f"Location: {location}\nPreferences: {preferences}\nFree windows (ISO): {free_windows}\n"
    )

def generate_suggestions(*, location: str, preferences: List[str], free_windows: List[dict]) -> List[dict]:
    model = genai.GenerativeModel(
        MODEL,
        generation_config={"response_mime_type": "application/json"}  # keep simple first
    )
    resp = model.generate_content(_prompt(location, preferences, free_windows))
    return json.loads(resp.text)


# def _prompt(location: str, preferences: List[str], free_windows: List[dict]) -> str:
#     return (
#         "You are a group activity planner.\n"
#         "Return ONLY JSON matching the schema. One suggestion per free window.\n"
#         f"Location: {location}\n"
#         f"Preferences: {preferences}\n"
#         f"Free windows (ISO): {free_windows}\n"
#     )

# def generate_suggestions(*, location: str,
#                          preferences: List[str],
#                          free_windows: List[dict]) -> List[dict]:
#     model = genai.GenerativeModel(
#         MODEL,
#         generation_config={
#             "response_mime_type": "application/json",
#             "response_schema": SCHEMA,
#         },
#     )
#     resp = model.generate_content(_prompt(location, preferences, free_windows))
#     try:
#         return json.loads(resp.text)
#     except Exception:
#         return []
