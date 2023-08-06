from pathlib import Path
from bs4 import BeautifulSoup
from json import JSONDecodeError

def make_dir(dir_name) -> None:
    try:
        Path(dir_name).mkdir()
        print(f"Creating directory '{dir_name}'..")
    except FileExistsError:
        # print(f"Directory '{dir_name}' exists..")
        pass

def full_path(dir: str) -> str:
    return str(Path(dir).absolute())

def file_exists(file_path: str) -> bool:
    return Path(file_path).is_file()

def html_from_file(file_path: str) -> BeautifulSoup:
    if file_exists(file_path):
        try:
            with open(file_path, encoding="utf8") as f:
                data = BeautifulSoup(f, 'html.parser')
                if data.body:
                    return data
                raise TypeError(f"File {file_path} is not a valid HTML file")
        except JSONDecodeError:
            return None
    raise FileNotFoundError(f'File "{file_path}" not found')
