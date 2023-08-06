from pathlib import Path

def make_dir(dir_name) -> None:
    try:
        Path(dir_name).mkdir()
        print(f"Creating directory '{dir_name}'..")
    except FileExistsError:
        # print(f"Directory '{dir_name}' exists..")
        pass

def full_path(dir: str) -> str:
    return str(Path(dir).absolute())
