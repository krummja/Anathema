from __future__ import annotations

from typing import *

from anathema.engine.message import Message

if TYPE_CHECKING:
    pass


class Messenger:

    def __init__(self, loop: EngineLoop) -> None:
        self.loop = loop
        self.messages: List[Message] = []

    def add_message(self, message: Message) -> None:
        if self.messages and self.messages[-1].text == message.text:
            self.messages[-1].count += 1
        else:
            self.messages.append(message)
