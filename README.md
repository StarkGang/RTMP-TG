# RTMP TG
Play streams in your chats using this userbot !

# Requirements
> **Python:** `python3`  
> **FFmpeg:** `ffmpeg`  
> **Pyrogram:** `pyrogram`  
> **Youtube Dl :** `youtube_dl` - (optional)

# How to run?
## Local

- run `pip install -r requirements.txt`
- fill your vars in `local.env`
- run `python3 main.py`   
- Now play using `!stream (url)`  

## Heroku

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

Warning : Heroku bans repo's with "youtube_dl" as requirement, So, make sure you remove the requirement and then deploy. (yes, the bot will still work but you won't get direct link support for youtube_dl supported sites :p)

### You need two build packs to get this userbot running 
> FFMPEG -  https://github.com/jonathanong/heroku-buildpack-ffmpeg-latest   
> Python - https://github.com/heroku/python

## Variables
- `STRING_SESSION` : Your pyrogram String Session
- `API_ID` : Your Telegram API ID
- `API_HASH` : Your Telegram API Hash
- `FFMPEG_PATH` : Path to FFmpeg
- `SUDO_USERS` : List of users allowed to use the userbot (set to 'all' to allow global access)