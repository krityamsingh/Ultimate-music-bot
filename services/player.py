# ============================================================
#  services/player.py
#
#  Thin wrapper around PyTgCalls.
#  Handles: play, pause, resume, stop, active-call tracking.
# ============================================================

from __future__ import annotations

from pytgcalls import PyTgCalls
from pytgcalls.types import MediaStream, AudioQuality
from config import AUDIO_QUALITY

# ── Singleton ─────────────────────────────────────────────────
_calls: PyTgCalls | None = None

# ── Currently playing track info per chat ─────────────────────
# { chat_id: { title, uploader, thumbnail, webpage_url, duration } }
_now_playing: dict[int, dict] = {}


# ─────────────────────────────────────────────────────────────
#  Init / Start
# ─────────────────────────────────────────────────────────────

def init_player(userbot) -> PyTgCalls:
    global _calls
    _calls = PyTgCalls(userbot)
    return _calls


async def start_player() -> None:
    """Must be called AFTER userbot.start()"""
    if _calls is None:
        raise RuntimeError("Call init_player() before start_player()")
    await _calls.start()


# ─────────────────────────────────────────────────────────────
#  Playback controls
# ─────────────────────────────────────────────────────────────

def _quality():
    q = AUDIO_QUALITY.upper()
    return {
        "LOW":    AudioQuality.LOW,
        "MEDIUM": AudioQuality.MEDIUM,
        "HIGH":   AudioQuality.HIGH,
    }.get(q, AudioQuality.HIGH)


async def play_audio(chat_id: int, stream_url: str, track_info: dict) -> None:
    """
    Join the voice chat in `chat_id` and start streaming `stream_url`.
    `track_info` is stored so /np can show what's playing.
    """
    if _calls is None:
        raise RuntimeError("Player not initialised.")

    await _calls.play(
        chat_id,
        MediaStream(
            stream_url,
            audio_parameters=_quality(),
        ),
    )
    _now_playing[chat_id] = track_info


async def pause_audio(chat_id: int) -> None:
    if _calls is None:
        raise RuntimeError("Player not initialised.")
    await _calls.pause_stream(chat_id)


async def resume_audio(chat_id: int) -> None:
    if _calls is None:
        raise RuntimeError("Player not initialised.")
    await _calls.resume_stream(chat_id)


async def stop_audio(chat_id: int) -> None:
    if _calls is None:
        raise RuntimeError("Player not initialised.")
    await _calls.leave_call(chat_id)
    _now_playing.pop(chat_id, None)


def get_now_playing(chat_id: int) -> dict | None:
    return _now_playing.get(chat_id)


def get_calls() -> PyTgCalls:
    return _calls
