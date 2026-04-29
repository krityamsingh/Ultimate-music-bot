# 🎵 Ultimate Music Bot

Plays music directly in Telegram Voice Chats. No API keys needed — searches YouTube with yt-dlp.

---

## How it works

```
User: /play Blinding Lights

Bot: 🔍 Finding music...       ← searches YouTube via yt-dlp (no API)
     ⏳ Loading track...        ← gets stream URL + thumbnail
     🔊 Joining voice chat...   ← pytgcalls joins the VC
     ▶️ Now Playing [thumbnail] ← card with title, artist, duration
```

The private log group receives a silent record of every queued track.

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

> **ffmpeg must be installed on your system:**
> - Ubuntu: `sudo apt install ffmpeg`
> - macOS:  `brew install ffmpeg`
> - Railway/Heroku: handled by nixpacks.toml

### 2. Configure credentials

Edit `config.py` OR set environment variables:

| Variable         | Description                                  |
|------------------|----------------------------------------------|
| `API_ID`         | Telegram API ID (my.telegram.org)            |
| `API_HASH`       | Telegram API Hash                            |
| `BOT_TOKEN`      | Bot token from @BotFather                    |
| `STRING_SESSION` | Pyrogram string session for the userbot      |
| `LOG_GC_ID`      | Chat ID of your private logging group        |
| `AUDIO_QUALITY`  | `LOW` / `MEDIUM` / `HIGH` (default: HIGH)    |

### 3. Generate a String Session (if you don't have one)

```python
from pyrogram import Client
async with Client("my_account", api_id=API_ID, api_hash=API_HASH) as app:
    print(await app.export_session_string())
```

### 4. Run

```bash
python start.py
```

---

## Commands

| Command   | Description                              |
|-----------|------------------------------------------|
| `/play <song>` | Search YouTube and play in Voice Chat |
| `/stop`   | Stop music and leave the voice chat      |
| `/pause`  | Pause the current track                  |
| `/resume` | Resume a paused track                    |
| `/np`     | Show the currently playing track card    |

---

## Requirements

- Python 3.10+
- ffmpeg (system dependency)
- An active Telegram Voice Chat in the group
- The userbot account must be a member of the group
