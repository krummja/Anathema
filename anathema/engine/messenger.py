from __future__ import annotations
from typing import *

from anathema.engine.message import Message
from anathema import log
from anathema.print_utils import cprint, bcolors

if TYPE_CHECKING:
    from anathema.typedefs import Color
    from anathema.session import Session
    from anathema.client import Client


class Messenger:

    def __init__(self, loop: EngineLoop) -> None:
        self.loop = loop
        self.messages: List[Message] = []

    def add_message(self, message: Message) -> None:
        if self.messages and self.messages[-1].text == message.text:
            self.messages[-1].count += 1
        else:
            self.messages.append(message)
