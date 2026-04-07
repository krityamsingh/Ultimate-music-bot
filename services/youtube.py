"""Gemini API -> YouTube link finder service."""

from typing import Optional


async def find_youtube_link(query: str) -> Optional[str]:
    """Return a YouTube URL for a given text query.

    TODO: integrate Gemini API to resolve best matching YouTube URL.
    """
    if not query.strip():
        return None

    # Placeholder implementation.
    return f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
