import re, os
from time import sleep
import src.client
from atproto import *
from asyncio import Queue
from dotenv import load_dotenv

LOGIN_ATTEMPT_DELAY_SEC = 5 # value > 0 recommended, >= 3 preferred, as to not spam bsky servers
LOGIN_ATTEMPTS = 4
SYS_MESSAGE_PREFIX = "[Main]: "

def main() -> None:
    load_dotenv()
    handle, password = os.getenv("HANDLE"), os.getenv("PASSWORD")
    assert handle is not None
    assert password is not None
    client = src.client.login(handle, password)

    if not client:
        for _ in range(LOGIN_ATTEMPTS):
            print(SYS_MESSAGE_PREFIX + f"Login failed, trying again in {LOGIN_ATTEMPT_DELAY_SEC} seconds...")
            # thread sleeps on fail, loop breaks on success
            sleep(LOGIN_ATTEMPT_DELAY_SEC)
            client = src.client.login(handle, password)
            if client:
                break
    if not client:
        input(SYS_MESSAGE_PREFIX + "Multiple login attempts failed! Press Enter to terminate program...")
        return

    while True:
        input_str = input(SYS_MESSAGE_PREFIX + "what to do?\n").lower()

        if re.search("^quit|^exit|^esc|^q$", input_str):
            break
        if input_str == "home":
            timeline = client.get_timeline()
            post = timeline.feed[0].post
            print(f"{post.author.display_name}: {post.record.text}")
        else:
            print(SYS_MESSAGE_PREFIX + "Unknown command.")

if __name__ == '__main__':
    main()