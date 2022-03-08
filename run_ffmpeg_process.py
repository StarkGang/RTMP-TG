import asyncio
import shlex
from config import *


yt_installed = True

try:
    import youtube_dl
    from ytdl_exc_ import get_direct_link
except ImportError: # import issue
    yt_installed = False


async def run_cmd(cmd: str):
    """Runs a shell command asyncronously."""
    args = shlex.split(cmd) # we don't need split ourselves, it may look neat though, but still i prefer this
    process = await asyncio.create_subprocess_exec(FFMPEG_PATH, *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    return process

async def ffmpeg_rtmp_stream(url, key, to_stream):
    """Streams a video from a rtmp server to a ffmpeg process."""
    if yt_installed:
        url = await get_direct_link(url) # bad method but yes. it is fine lol
    cmd_ = f'-stream_loop -1 -re -i "{to_stream}" -c:v libx264 -preset veryfast -b:v 2500k -maxrate 2500k -bufsize 5000k -pix_fmt yuv420p -g 50 -c:a aac -b:a 128k -ac 2 -ar 44100 -f flv {url}{key}'
    process_ = await run_cmd(cmd_)
    return process_