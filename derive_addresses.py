import hmac
import hashlib

# Pure Python base58 and address formatting engine
ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_encode(b: bytes) -> str:
    n = int.from_bytes(b, 'big')
    res = []
    while n > 0:
        n, rem = divmod(n, 58)
        res.append(ALPHABET[rem])
    pad = 0
    for byte in b:
        if byte == 0:
            pad += 1
        else:
            break
    return ALPHABET[0] * pad + ''.join(reversed(res))

print("[*] Local motor engine initialized with native base58 support.")
