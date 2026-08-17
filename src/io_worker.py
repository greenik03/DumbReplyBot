import os
import stat

SYS_MESSAGE_PREFIX = "[IOWorker]: "
DATA_PATH = "data/"
FILE_PATH = f"{DATA_PATH}phrases.txt"

def __open_data_file__():
    return None if not os.path.exists(FILE_PATH) \
        else open(FILE_PATH)

def grant_permissions():
    os.chmod(FILE_PATH, stat.S_IRWXU)

def create_absent_files() -> None:
    if not os.path.exists(DATA_PATH):
        print(SYS_MESSAGE_PREFIX + f"Folder {DATA_PATH} in current directory not found. Creating...")
        os.mkdir(DATA_PATH)
        print(SYS_MESSAGE_PREFIX + "Folder created.")
    if not os.path.exists(FILE_PATH):
        print(SYS_MESSAGE_PREFIX + f"File {FILE_PATH} not found. Creating...")
        with open(FILE_PATH, "w") as file:
            file.write("Placeholder text")
        os.chmod(FILE_PATH, stat.S_IRWXU)
        print(SYS_MESSAGE_PREFIX + "File created.")

def read_content() -> list[str]:
    file = __open_data_file__()
    if file is None:
        create_absent_files()
        print(SYS_MESSAGE_PREFIX + f"WARNING: Attempted to read from nonexistent {FILE_PATH}. Using placeholder data as fallback.")
        print(SYS_MESSAGE_PREFIX + f"Replace the placeholder data in {FILE_PATH} with actual content, then run 'cache-reset' to add the content to memory.")
        return ["Placeholder text",]
    # content = file.readlines()
    content = [line.rstrip() for line in file]
    file.close()
    print(SYS_MESSAGE_PREFIX + f"Successfully read {len(content)} phrase(s) from file.")
    return content
