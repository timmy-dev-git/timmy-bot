import json
import os
from typing import Any

class Data:
    def __init__(
        self,
        author_id: int,
        category : str,
        base_dir : str = "data/users",
    ) -> None:
        self._closed = False
        self.author_id = str(author_id)
        self.category  = category
        self.dir_path  = os.path.join(base_dir, self.author_id)
        self.file_path = os.path.join(self.dir_path, f"{self.category}.json")

        os.makedirs(self.dir_path, exist_ok=True)
        with open(self.file_path, "a+"):
            return

    def read(self) -> dict[str, Any]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def overwrite(self, data: dict[str, Any]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def append(self, key: str, value: Any) -> None:
        data = self.read()
        data[key] = value
        self.overwrite(data)

    def delete(self) -> None:
        os.remove(self.file_path)
        self._closed = True

    def close(self) -> None:
        self._closed = True