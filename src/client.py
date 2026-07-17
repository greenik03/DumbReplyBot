import traceback
import atproto.exceptions
from atproto import Client

SYS_MESSAGE_PREFIX = "[Client]: "


def login(handle: str, password: str) -> Client | None:
    try:
        client = Client()
        client.login(handle, password)
        print(SYS_MESSAGE_PREFIX + f"{client.me.handle} logged in successfully.")
        return client
    except atproto.exceptions.AtProtocolError as e:
        print(SYS_MESSAGE_PREFIX + "An error occurred while trying to login.")
        traceback.print_exc()
        return None
