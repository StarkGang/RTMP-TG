import logging

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.basicConfig(
            level=logging.DEBUG,
            datefmt="[%d/%m/%Y %H:%M:%S]",
            format="%(asctime)s - [STREAMERUB] >> %(levelname)s << %(message)s",
            handlers=[logging.FileHandler("streamerub.log"), logging.StreamHandler()],
    )