import re, os
from concurrent.futures.thread import ThreadPoolExecutor
from time import sleep
import src.client, src.listener, src.io_worker
from dotenv import load_dotenv

SHUTDOWN_BOT = False
SYS_MESSAGE_PREFIX = "[Main]: "
COMMANDS: dict[str, str] = {
    "home": "Print the latest post from home (following) timeline",
    "info": "Print client and listener info",
    "cache-reset": "Re-read phrases.txt and store new phrases in memory",
    "q(uit)/exit/logout/stop": "Stop the bot",
}

def help_msg() -> None:
    print(SYS_MESSAGE_PREFIX + "Here are all available commands:")
    for name, desc in zip(COMMANDS.keys(), COMMANDS.values()):
        print(f"\t{name} - {desc}")

def open_phrases_file() -> list[str]:
    try:
        phrases = src.io_worker.read_content()
    except PermissionError as e:
        print(e)
        print(SYS_MESSAGE_PREFIX + "Missing read permission for phrases file. Attempting to add permission...")
        src.io_worker.grant_permissions()
        phrases = src.io_worker.read_content()
        print(SYS_MESSAGE_PREFIX + "Read permission for phrases file added.")
    return phrases

def console_init(client: src.client.DRBClient, listener: src.listener.DRBListener) -> None:
    global SHUTDOWN_BOT

    while not SHUTDOWN_BOT:
        input_str = input(SYS_MESSAGE_PREFIX + "Insert command:\n").lower()

        # command strings should be in lower case
        if re.search("^quit|^exit|^logout|^q$|^stop", input_str):
            SHUTDOWN_BOT = True
        elif input_str in COMMANDS:
            match input_str:
                case "home": # TODO: placeholder command, just here to test API
                    timeline = client.cli.get_timeline()
                    post = timeline.feed[0].post
                    print(f"{post.author.display_name}: {post.record.text}")
                case "info":
                    print(client)
                    print(listener)
                case "cache-reset":
                    client.phrases = open_phrases_file()
                case _: # case "q(uit)/exit/logout/stop" already covered before match-case
                    print(SYS_MESSAGE_PREFIX + "WARNING: Command exists, but not implemented!")
        else:
            help_msg()


def main() -> None:
    global SHUTDOWN_BOT
    load_dotenv()
    handle, password = os.getenv("HANDLE"), os.getenv("PASSWORD")
    phrases = open_phrases_file()
    assert handle is not None
    assert password is not None
    assert len(phrases) > 0
    client = src.client.DRBClient(handle, password, phrases)
    cli = client.login() # only using this variable to validate login

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

    assert cli is not None # cli is no longer None, it's safe to assume that bot is successfully logged in from here
    del cli # delete the variable since it's no longer needed, use client.cli instead
    listener = src.listener.DRBListener(client)
    tpe = ThreadPoolExecutor(max_workers=1)
    tpe.submit(listener.listen) # start the listener on a separate thread
    console_init(client, listener) # enters while loop in function, user input required to break loop
    listener.shutdown()
    tpe.shutdown()

if __name__ == '__main__':
    main()