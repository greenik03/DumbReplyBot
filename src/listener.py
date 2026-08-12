import atproto, time
from src import client

SYS_MESSAGE_PREFIX = "[Listener]: "

class DRBListener:
    def __init__(self, cli: client.DRBClient):
        self.cli = cli
        self.shutdown_signal = False
        username = self.cli \
            .handle \
            .split(".")[0]
        self.name = f"LSTNR-{username}"
        print(SYS_MESSAGE_PREFIX + f"Listener for client initialized: {self.name}")

    def listen(self) -> None:
        # TODO: test code here, needs to be replaced
        while not self.shutdown_signal:
            print(time.time())
            time.sleep(2)

    def shutdown(self):
        self.shutdown_signal = True

    def __str__(self) -> str:
        return f"""{self.name}
    Assigned to: {self.cli.name}
    Is running: {not self.shutdown_signal}
                """
