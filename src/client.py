import traceback
from random import Random
from atproto import Client, exceptions

SYS_MESSAGE_PREFIX = "[Client]: "

class DRBClient:
    def __init__(self, handle: str, password: str):
        self.handle = handle
        self.password = password
        self.rand = Random()
        self.cli = Client()
        self.phrases = list() # TODO: invoke IOWorker for list of phrases
        print(SYS_MESSAGE_PREFIX + f"Client for {self.handle} initialized.")

    def login(self) -> Client | None:
        try:
            self.cli.login(self.handle, self.password)
            print(SYS_MESSAGE_PREFIX + f"{self.cli.me.handle} logged in successfully.")
            return self.cli
        except exceptions.AtProtocolError as e:
            print(SYS_MESSAGE_PREFIX + "An error occurred while trying to log in.")
            traceback.print_exc()
            return None

    def create_post(self) -> str:
        pass