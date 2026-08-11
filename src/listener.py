import atproto, time

from src import client

SYS_MESSAGE_PREFIX = "[Listener]: "

class DRBListener:
    def __init__(self, cli: client.DRBClient):
        self.cli = cli
        print(SYS_MESSAGE_PREFIX + f"Listener for {cli.handle} client initialized.")

    def listen(self) -> None:
        pass

def thread_test(seconds) -> None:
    while True:
        print(time.time())
        time.sleep(seconds)
