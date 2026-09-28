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

    def is_user_labelled(self, user_did) -> bool:
        pass

    def is_post_labelled(self, user_post_cid: str, user_post_uri: str) -> bool:
        pass

    def has_extembed_or_link(self, user_post_cid: str, user_post_uri: str) -> bool:
        pass

    # TODO: add additional check for blacklisted/whitelisted words

    # TODO
    def make_reply(self, user_post_cid: str, user_post_uri: str, user_did: str):
        # check if user post exists first (in case it gets deleted in the time it takes for the bot to respond)
        post = self.cli.app.bsky.feed.get_posts([user_post_uri]).posts[0]

        # then, check if the user has any labels added by Bluesky (rude, impersonator, scammer, etc.)
        # TODO: if self.is_user_labelled(user_did):
        #     return

        # or if the post has labels
        # TODO: if self.is_post_labelled(user_post_cid, user_post_uri):
        #     return

        # additionally, check if the post has links or external embeds (i think Bluesky hates that)
        # TODO: if self.has_extembed_or_link(user_post_cid, user_post_uri):
        #     return

        # if all those checks passed, grab a random phrase from the list and send a reply
        text: str = self.rand.choice(self.phrases)
        print(SYS_MESSAGE_PREFIX + post)
        print(SYS_MESSAGE_PREFIX + text)

    def __str__(self) -> str:
        return f"""{self.name}
    Full handle: {self.handle}
    DID: {self.cli.me.did}
    Number of phrases: {len(self.phrases)}
                """