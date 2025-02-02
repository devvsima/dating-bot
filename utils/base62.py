import string

BASE62_ALPHABET = string.digits + string.ascii_letters


def encode_base62(num: int) -> str:
    """Кодирует число"""
    base = len(BASE62_ALPHABET)
    encoded = []
    while num:
        num, rem = divmod(num, base)
        encoded.append(BASE62_ALPHABET[rem])
    return "".join(reversed(encoded))


def decode_base62(encoded_str: str) -> str:
    """Декодирует строку"""
    base = len(BASE62_ALPHABET)
    num = 0
    for char in encoded_str:
        num = num * base + BASE62_ALPHABET.index(char)
    return num
