import re, os
import threading
from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep

import src.client, src.listener, src.io_worker
from dotenv import load_dotenv

SHUTDOWN_BOT = False
SYS_MESSAGE_PREFIX = "[Main]: "

def main() -> None:
    global SHUTDOWN_BOT
    load_dotenv()
    handle, password = os.getenv("HANDLE"), os.getenv("PASSWORD")
    assert handle is not None
    assert password is not None
    client = src.client.DRBClient(handle, password)
    cli = client.login()

    if not cli:
        print(SYS_MESSAGE_PREFIX + "Login attempt failed! Read the error message to find out more.")
    while not cli:
        sleep(1) # delay the message so that it appears after the error message
        input_str = input(SYS_MESSAGE_PREFIX + "Would you like to try again? [y/n]\n").lower()
        if re.search("^yes|^y$", input_str):
            cli = client.login()
        elif re.search("^no|^n$", input_str):
            SHUTDOWN_BOT = True
            break
        else:
            print(SYS_MESSAGE_PREFIX + "Valid answers are: y(es), n(o)")

    listener = src.listener.DRBListener(client)

    # TODO
    '''
    Create a ThreadPoolExecutor here for the following threads:
    - Listener (pass client as parameter to listen for tags)
    - Controller (the remaining code below which will be its own function and/or module)
    
    code would look like this:
    
    with ThreadPoolExecutor(max_workers=2) as tpe:
        tpe.submit(Listener)
        tpe.submit(Controller)
        # run until stop command from controller, which then does:
        tpe.shutdown()
    '''

    # login successful, control the bot with commands from terminal
    while not SHUTDOWN_BOT:
        input_str = input(SYS_MESSAGE_PREFIX + "Insert command:\n").lower()

        # command strings should be in lower case
        if re.search("^quit|^exit|^logout|^q$|^stop", input_str):
            SHUTDOWN_BOT = True
        elif input_str == "home":
            timeline = cli.get_timeline()
            post = timeline.feed[0].post
            print(f"{post.author.display_name}: {post.record.text}")
        else:
            print(SYS_MESSAGE_PREFIX + "Unknown command.")

if __name__ == '__main__':
    main()