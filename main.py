import re, os
from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep
import src.client, src.listener, src.io_worker
from dotenv import load_dotenv

SHUTDOWN_BOT = False
SYS_MESSAGE_PREFIX = "[Main]: "

def help_msg() -> None: # TODO: print message for available commands
    pass

def console_init(client: src.client.DRBClient, listener: src.listener.DRBListener) -> None:
    global SHUTDOWN_BOT

    while not SHUTDOWN_BOT:
        input_str = input(SYS_MESSAGE_PREFIX + "Insert command:\n").lower()

        # command strings should be in lower case
        if re.search("^quit|^exit|^logout|^q$|^stop", input_str):
            SHUTDOWN_BOT = True
        elif input_str == "home": # TODO: placeholder command, just here to test API
            timeline = client.cli.get_timeline()
            post = timeline.feed[0].post
            print(f"{post.author.display_name}: {post.record.text}")
        elif input_str == "info":
            print(client)
            print(listener)
        else:
            print(SYS_MESSAGE_PREFIX + "Unknown command.") # call help_msg() instead

def main() -> None:
    global SHUTDOWN_BOT
    load_dotenv()
    handle, password = os.getenv("HANDLE"), os.getenv("PASSWORD")
    assert handle is not None
    assert password is not None
    client = src.client.DRBClient(handle, password)
    cli = client.login()

    if not cli: # login() returned None
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

    if SHUTDOWN_BOT: # perform check here to avoid unnecessary assertion error
        return

    assert cli is not None # cli is no longer None, it's safe to assume that it's an ATProto client from here
    listener = src.listener.DRBListener(client)
    # start the listener on a separate thread
    tpe = ThreadPoolExecutor(max_workers=1)
    tpe.submit(listener.listen)
    console_init(client, listener) # enters while loop in function, user input required to break loop
    listener.shutdown()
    tpe.shutdown()

if __name__ == '__main__':
    main()