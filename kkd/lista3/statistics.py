import os


def calculate_compression(input_path, encoded_path):
    original = os.path.getsize(input_path)
    compressed = os.path.getsize(encoded_path)
    return original, compressed, round(compressed * 100 / original, 0)


def file_length(path) -> int:
    if path[-4:] == '.bin':
        with open(path, 'rb') as f:
            return len(f.read())
    else:
        with open(path, 'r') as f:
            return len(f.read())
