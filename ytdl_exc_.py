from youtube_dl import YoutubeDL
from utils import *

ytdl_ = YoutubeDL({
    "format": "best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "quiet": True,
    "logtostderr": False
})

extract_info_ytdl = async_wrap(ytdl_.extract_info)

async def get_direct_link(url: str):
    try:
        data = await extract_info_ytdl(url)
        return data.get("link")
    except Exception: # hopefully, exception will raised for urls not supported by ytdl
        return url