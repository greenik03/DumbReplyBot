import os

SYS_MESSAGE_PREFIX = "[IOWorker]: "
DATA_DIR = "../data/"

def __open_data_file__(file_name: str):
    return None \
        if not os.path.exists(DATA_DIR + file_name) \
        else open(DATA_DIR + file_name)

def create_absent_files() -> None:
    pass

def read_contents() -> list:
    pass

