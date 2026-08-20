import traceback
from random import Random
from atproto import Client, exceptions

SYS_MESSAGE_PREFIX = "[Client]: "

class DRBClient:
    def __init__(self, handle: str, password: str, phrases: tuple[str]):
        self.handle = handle
        self.password = password
        self.rand = Random()
        self.cli = Client()
        self.phrases = phrases
        username = handle.split(".")[0]
        self.name = f"CLI-{username}"
        print(SYS_MESSAGE_PREFIX + f"Client for {self.handle} initialized: {self.name}")

    def login(self) -> Client | None:
        try:
            self.cli.login(self.handle, self.password)
            print(SYS_MESSAGE_PREFIX + f"{self.cli.me.handle} logged in successfully.")
            return self.cli
        except exceptions.AtProtocolError as e:
            print(SYS_MESSAGE_PREFIX + "An error occurred while trying to log in.")
            # traceback.print_exc()
            print(e)
            return None

    def make_post(self, user_post_did: str):
        # TODO
        # user_post_did: the ID of the post in which the bot is tagged in
        # check if user_post_did exists first (in case it gets deleted in the time it takes for the bot to respond)
        # then, check if the user has any labels added by Bluesky (rude, impersonator, scammer, etc.)
        # additionally, check if the post has links or external embeds (i think Bluesky hates that)
        # if all those checks passed, grab a random phrase from the list and send a reply
        pass

    def __str__(self) -> str:
        return f"""{self.name}
    Full handle: {self.handle}
    DID: {self.cli.me.did}
    Number of phrases: {len(self.phrases)}
                """