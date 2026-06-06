# src/memory/storage.py
import pickle
import zlib
import pathlib

class VirtualMemoryStore:
    def __init__(self, storage_dir="data_store"):
        self.storage_dir = pathlib.Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)

    def save(self, key: str, data: any):
        compressed_data = zlib.compress(pickle.dumps(data))
        with open(self.storage_dir / f"{key}.bin", "wb") as f:
            f.write(compressed_data)

    def load(self, key: str, default=None):
        path = self.storage_dir / f"{key}.bin"
        if not path.exists():
            return default
        with open(path, "rb") as f:
            return pickle.loads(zlib.decompress(f.read()))