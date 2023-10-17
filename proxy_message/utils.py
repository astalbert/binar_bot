import hashlib


def combine_hash(*args: str) -> str:
    return hashlib.md5(','.join(args).encode()).hexdigest()
