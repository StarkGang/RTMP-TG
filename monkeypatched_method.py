from pyrogram.types import Message
from typing import Union
from utils import *

@monkeypatch(Message)
class utils_:
    def __init__(self) -> None:
        super().__init__()

    @property
    def input_str(self) -> Union[str, None]:
        text_to_return = self.text
        if self.text is None:
            return None
        if " " not in text_to_return:
            return None
        try:
            return self.text.split(None, 1)[1]
        except IndexError:
            return None