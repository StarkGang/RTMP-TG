import dotenv
import os
import loggers

dotenv.load_dotenv("local.env")

api_id = int(os.environ.get("API_ID") or 6)
api_hash = os.environ.get("API_HASH")
STRING_SESSION = os.environ.get("STRING_SESSION")
FFMPEG_PATH = os.environ.get("FFMPEG_PATH") or "ffmpeg"