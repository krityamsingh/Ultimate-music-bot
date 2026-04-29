# ============================================================
#  services/youtube.py
#
#  Searches YouTube using yt-dlp — NO API KEY required.
#  Returns stream URL, thumbnail, title, duration, etc.
# ============================================================

import asyncio
import yt_dlp


# ── yt-dlp options ────────────────────────────────────────────
_YDL_OPTS = {
    "format":          "bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio/best",
    "noplaylist":      True,
    "quiet":           True,
    "no_warnings":     True,
    "source_address":  "0.0.0.0",
    # Do NOT download — we only want the stream URL
    "skip_download":   True,
}


def _extract_sync(query: str) -> dict | None:
    """Blocking yt-dlp call — run in executor to avoid blocking the event loop."""
    with yt_dlp.YoutubeDL(_YDL_OPTS) as ydl:
        try:
            data = ydl.extract_info(f"ytsearch1:{query}", download=False)
        except Exception:
            return None

    if not data or "entries" not in data or not data["entries"]:
        return None

    entry = data["entries"][0]

    # ── Pick the best audio-only direct stream URL ────────────
    stream_url: str | None = None
    best_abr = 0

    for fmt in entry.get("formats", []):
        vcodec = fmt.get("vcodec", "none")
        acodec = fmt.get("acodec", "none")
        url    = fmt.get("url", "")

        if acodec != "none" and vcodec in ("none", None, "") and url:
            abr = fmt.get("abr") or 0
            if abr >= best_abr:
                best_abr   = abr
                stream_url = url

    # Fallback to the generic 'url' field
    if not stream_url:
        stream_url = entry.get("url") or entry.get("webpage_url")

    # ── Best thumbnail (highest resolution) ───────────────────
    thumbnail = ""
    thumbs = entry.get("thumbnails") or []
    if thumbs:
        # Sort by width descending; fall back to last entry
        sorted_thumbs = sorted(thumbs, key=lambda t: t.get("width") or 0, reverse=True)
        thumbnail = sorted_thumbs[0].get("url", "")
    if not thumbnail:
        thumbnail = entry.get("thumbnail", "")

    return {
        "title":       entry.get("title",      "Unknown Title"),
        "uploader":    entry.get("uploader",    "Unknown Artist"),
        "thumbnail":   thumbnail,
        "duration":    int(entry.get("duration") or 0),
        "webpage_url": entry.get("webpage_url", ""),
        "stream_url":  stream_url,
        "views":       entry.get("view_count",  0),
    }


async def search_youtube(query: str) -> dict | None:
    """
    Async wrapper around the blocking yt-dlp call.
    Returns a dict with track info, or None on failure.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _extract_sync, query)
