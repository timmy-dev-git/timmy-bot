import os
import json
from typing import Any

class Data:
    def __init__(self, id: int, category: str):
        directory = f"data/users/{str(id)}/"
        os.makedirs(directory, exist_ok=True)
        self.path = directory + category

        with open(self.path, "a+"):
            return

    def read(self) -> dict[str, Any]:
        if os.path.getsize(self.path) == 0:
            output: dict[str, Any] = { }
            return output
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def overwrite(self, data: dict[str, Any]) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def append(self, data: dict[str, Any]) -> None:
        file = self.read()
        for key, value in data.items():
            file[key] = value
        self.overwrite(file)

    def delete(self) -> None:
        os.remove(self.path)