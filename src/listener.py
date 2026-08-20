import atproto, time
from src import client
from datetime import datetime

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
        bsky = self.cli.cli.app.bsky
        # TODO: test code here, needs to be replaced
        while not self.shutdown_signal:
            print(datetime.now().time())
            time.sleep(3)

            # grab unread notifications, save them in a var
            # call cli.make_post() if bot gets tagged, pass the post did as argument
            # additionally, delete replies to deleted posts every hour???
            # mark notifs as read
            # delay cycle by 1-2 seconds to avoid spamming the servers with requests multiple times a second?

    def shutdown(self):
        self.shutdown_signal = True

    def __str__(self) -> str:
        return f"""{self.name}
    Assigned to: {self.cli.name}
    Is running: {not self.shutdown_signal}
                """
