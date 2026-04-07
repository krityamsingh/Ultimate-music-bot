# ============================================================
#  services/youtube.py  —  Use Gemini to find a YouTube link
# ============================================================

import re
import aiohttp
from config import GEMINI_API_KEY

GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
)

PROMPT_TEMPLATE = (
    "Find the best matching YouTube video URL for the song: '{query}'.\n"
    "Return ONLY the full YouTube URL (https://www.youtube.com/watch?v=...) "
    "and nothing else. No explanation, no markdown, just the raw URL."
)


async def get_youtube_link(query: str) -> str | None:
    """
    Ask Gemini to return a YouTube URL for the given song query.
    Returns the URL string, or None if not found.
    """
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": PROMPT_TEMPLATE.format(query=query)}
                ]
            }
        ]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(GEMINI_URL, json=payload) as resp:
            if resp.status != 200:
                return None
            data = await resp.json()

    # Extract the text from the Gemini response
    try:
        raw_text: str = (
            data["candidates"][0]["content"]["parts"][0]["text"].strip()
        )
    except (KeyError, IndexError):
        return None

    # Validate it actually looks like a YouTube URL
    match = re.search(
        r"(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w\-]+)",
        raw_text,
    )
    if match:
        return match.group(1)

    return None
