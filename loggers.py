import logging

logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.basicConfig(
            level=logging.INFO,
            datefmt="[%d/%m/%Y %H:%M:%S]",
            format="%(asctime)s - [STREAMERUB] >> %(levelname)s << %(message)s",
            handlers=[logging.FileHandler("streamerub.log"), logging.StreamHandler()],
    )