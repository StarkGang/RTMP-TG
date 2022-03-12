from youtube_dl import YoutubeDL, extractor
from _utils import *

ytdl_ = YoutubeDL({
    "format": "best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "quiet": True,
    "logtostderr": False
})

extract_info_ytdl = async_wrap(ytdl_.extract_info)

@async_wrap
def is_supported(url): # https://stackoverflow.com/a/61489622
    extractors = extractor.gen_extractors()
    return any(e.suitable(url) and e.IE_NAME != 'generic' for e in extractors)


async def get_direct_link(url: str):
    if await is_supported(url): return (await extract_info_ytdl(url)).get('link')
    return url # if not supported.