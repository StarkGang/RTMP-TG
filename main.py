import asyncio
import signal
from config import *
from loggers import *
from pyrogram import Client, idle, filters
from pyrogram.raw.functions.phone import *
from monkeypatched_method import *
from pyrogram.raw.functions.phone import GetGroupCallStreamRtmpUrl, GetGroupCall
from run_ffmpeg_process import ffmpeg_rtmp_stream
from pyrogram.raw.functions import Ping
import time

ubbot_client = Client(STRING_SESSION, api_id, api_hash)

async def begin_bot():
    logging.info("Starting Userbot.")
    await ubbot_client.start()
    ubbot_client.me = await ubbot_client.get_me()
    logging.info("Userbot started - Logined as : {}".format(ubbot_client.me.first_name))
    await idle()

async def try_to_create_gp_call(c: Client, chat_id):
    """Create a group call"""
    peer = await c.resolve_peer(chat_id)
    await c.send(CreateGroupCall(peer=peer, random_id=c.rnd_id() // 9000000000))

async def get_rmtp_key_and_url(c, chat_id):
    """Get rtmp key and url of a group_call"""
    peer_ = await c.resolve_peer(chat_id)
    c = await c.send(GetGroupCallStreamRtmpUrl(peer=peer_, revoke=True))
    return c.url, c.key

GC_S = {}

@ubbot_client.on_message(filters.command("ping", [".", "/", "!"]))
@sudo_wrap
async def ping_bot(c, m):
    st_time = time.perf_counter()
    await c.send(Ping(ping_id=9999999))
    end_ = round((time.perf_counter() - st_time)  * 1000, 2)
    await m.edit(f"<b>PONG!</b> \n<b>Time Taken :</b> <code>{end_}ms</code>")

@ubbot_client.on_message(filters.command("stream", prefixes=[".", "/", "!"]))
@sudo_wrap
async def stream_now(c, m):
    input_str = m.input_str
    if not input_str:
        return await m.edit("<b>Please add a link or a file path to stream to telegram</b>")
    if m.chat.id in GC_S:
        GC_S[m.chat.id].send_signal(signal.SIGTERM)
        del GC_S[m.chat.id]
    try:
        await try_to_create_gp_call(c, m.chat.id)
    except Exception as e:
        return await m.edit(f"<b>Error While making a group call</b> \n<b>Error:</b> <code>{e}</code>")
    try:
        url, key = await get_rmtp_key_and_url(c, m.chat.id)
    except Exception as e:
        return await m.edit("<b>AN error occured while trying to get rmtp url and key</b> \n<b>Error:</b> <code>{}</code>".format(e))
    if not (key or url):
        return await m.edit("<b>Failed to get rtmp key and url</b>")
    logging.info(f"Key : {key}")
    logging.info("URL : {}".format(url))
    if not input_str.endswith(("m3u8", "m3u")) and not os.path.exists(input_str):
        return await m.edit("<b>File or url not found</b>")
    logging.info("Sending to FFMPEG")
    p = await ffmpeg_rtmp_stream(url, key, input_str)
    GC_S[m.chat.id] = p
    await m.edit("<b>Streaming to telegram...</b>")
    st_time = time.perf_counter()
    stdout, stderror = await p.wait()
    if stderror:
        stderror = stderror.decode("utf-8")
    if stdout:
        stdout = stdout.decode("utf-8")
    end_time = round(time.perf_counter() - st_time, 2)
    if (end_time < 10) and (p.returncode != 0) and (stderror):
        logging.error(stderror)
        return await m.edit("</code>Stream Ended too quickly also, some errors were detected. please check your logs to know more</code>")
    await m.edit(f"<b>Stream ended</b> in __{end_time}ms !__")

@ubbot_client.on_message(filters.command("stop", prefixes=["!", ".", "/"]))
@sudo_wrap
async def stop_pro(c, m):
    if m.chat.id in GC_S:
        GC_S[m.chat.id].send_signal(signal.SIGTERM)
        del GC_S[m.chat.id]
        await m.edit("<b>Stopped Stream</b>")
    else:
        await m.edit("<b>No ongoing stream</b>")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(begin_bot())