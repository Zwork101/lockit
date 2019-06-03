from pathlib import Path
import json

from appdirs import user_data_dir

PROJECT_NAME = "lockit"
PROJECT_AUTHOR = "lockit"


class Cache:

    DATA_DIR = user_data_dir(PROJECT_NAME, PROJECT_AUTHOR)
    UNKNOWN = -1
    FILE = 0
    DIRECTORY = 1

    def __init__(self, data_dir: str=DATA_DIR):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.file_types = self.data_dir / "file_types.json"
        self.types = self.get_data(self.file_types)

    def get_data(self, path: Path):
        path.touch()
        data = path.read_text()
        if not data:
            return {}
        return json.loads(data)

    def save(self):
        with self.file_types.open("w") as file:
            json.dump(self.types, file)

    def set_path(self, abs_path: str, data_type: int):
        self.types[abs_path] = data_type
        self.save()

    def pop_type(self, abs_path: str):
        typ = self.UNKNOWN if abs_path not in self.types else self.types.pop(abs_path)
        if typ != self.UNKNOWN:
            self.save()
        return typ
