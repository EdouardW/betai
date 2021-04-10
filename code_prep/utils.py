from pathlib import Path

def create_input_folder(path: Path) -> None:
    if path.is_dir() is False:
        path.mkdir(parents=True)