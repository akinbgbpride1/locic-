# src/memory/storage.py
import json
import pathlib
from typing import Any

class VirtualMemoryStore:
    def __init__(self, storage_dir="data_store"):
        self.storage_dir = pathlib.Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

    def save(self, key: str, data: Any):
        """Saves data as a human-readable JSON file."""
        file_path = self.storage_dir / f"{key}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load(self, key: str, default=None) -> Any:
        """Loads data from a JSON file."""
        path = self.storage_dir / f"{key}.json"
        if not path.exists():
            return default
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)