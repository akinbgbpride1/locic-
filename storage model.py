import pickle
import zlib
import pathlib
import os

class VirtualMemoryStore:
    def __init__(self, storage_dir="data_store"):
        self.storage_dir = pathlib.Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        print(f"Virtual memory initialized at: {self.storage_dir.absolute()}")

    def _get_path(self, key: str) -> pathlib.Path:
        # Sanitize key to be a safe filename
        return self.storage_dir / f"{key}.bin"

    def save(self, key: str, data: any):
        """Compresses and saves data to disk."""
        compressed_data = zlib.compress(pickle.dumps(data))
        with open(self._get_path(key), "wb") as f:
            f.write(compressed_data)

    def load(self, key: str):
        """Loads and decompresses data from disk."""
        path = self._get_path(key)
        if not path.exists():
            return None
        
        with open(path, "rb") as f:
            compressed_data = f.read()
            return pickle.loads(zlib.decompress(compressed_data))