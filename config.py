# ============================================================
#  config.py
# ============================================================

import os

API_ID         = int(os.getenv("API_ID",         "27941605"))
API_HASH       = os.getenv("API_HASH",            "dd6639871a2f54a059151dc0b3277bb8")
BOT_TOKEN      = os.getenv("BOT_TOKEN",           "8749817037:AAH1YECmimuQJ9fFObzhXxaegEIhTxol5Fw")

STRING_SESSION = os.getenv("STRING_SESSION", (
    "BQGqWuUAaEt0lcZQBgGgi2hYeWLZY7Rn_JUZDO9uuAqSP3SsqzjvrIb8dBdHv60y9amfZnhJxnn3R4jORtpqhLR5aIkv8Q9m0e-ilPGA9j_L5VCwAIyGve0mNCBrSh1ex"
    "zPYyEVe0WdcXIZj_CH11INe_bVSEL2ILsxJ4h5TwdoA9RiFj_l8hRt-bMdRl-FA6kIH29eJjxAUkf6SwlwgxYWGPEq3zdq-TreX2uXydJ3p0j8aUmdMAsl0CxM0HzxQl5V"
    "p3n7yiMrusMhVQz4uAWkp23NFjCrBKozw4GkU2m864knc_p1GRSumSpUcJD5u-VxNhBjzd2dBiDz3FULRCCXRzZzNLwAAAAFJwHCDAA"
))

# Private log group where MegaSaverBot lives
LOG_GC_ID        = int(os.getenv("LOG_GC_ID", "-1003864293232"))
MEGA_SAVER_BOT   = "MegaSaverBot"
WAIT_FOR_BUTTONS = 30
WAIT_FOR_FILE    = 120

# Audio quality: LOW | MEDIUM | HIGH
AUDIO_QUALITY = os.getenv("AUDIO_QUALITY", "HIGH")
