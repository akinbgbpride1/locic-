import zlib
import pickle

def save_to_memory(data):
    """Compresses data to save space."""
    serialized = pickle.dumps(data)
    return zlib.compress(serialized)

def load_from_memory(compressed_data):
    """Decompresses data for the agent to read."""
    decompressed = zlib.decompress(compressed_data)
    return pickle.loads(decompressed)