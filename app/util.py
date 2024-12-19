import re
import hashlib

PATTERN = re.compile(r'\d+\.\d+\.\d+(\.\d+)?')

def find_version_in_string(s: str):
    match = PATTERN.search(s)
    return match.group() if match else None

def compute_sha512(file_path: str):
    sha512 = hashlib.sha512()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha512.update(chunk)
    return sha512.hexdigest()