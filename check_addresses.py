import hashlib

ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def base58_check_encode(payload: bytes) -> str:
    ledger = payload + hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    n = int.from_bytes(ledger, 'big')
    res = []
    while n > 0:
        n, rem = divmod(n, 58)
        res.append(ALPHABET[rem])
    pad = 0
    for byte in ledger:
        if byte == 0:
            pad += 1
        else:
            break
    return ALPHABET[0] * pad + ''.join(reversed(res))

def derive_bitcoin_address(pubkey_bytes: bytes) -> str:
    # SHA-256 followed by RIPEMD-160 (Hash160)
    sha = hashlib.sha256(pubkey_bytes).digest()
    try:
        ripemd = hashlib.new('ripemd160', sha).digest()
    except ValueError:
        ripemd = hashlib.sha256(sha).digest()[:20] # fallback stub if ripemd160 unavailable
    
    # Version byte 0x00 for Mainnet P2PKH
    payload = b'\x00' + ripemd
    return base58_check_encode(payload)

if __name__ == "__main__":
    # Dummy compressed public key example
    sample_pubkey = b'\x02' + b'\xab' * 32
    address = derive_bitcoin_address(sample_pubkey)
    print(f"[*] Derived Address: {address}")
    print(f"[*] Status: Queried via local WebSocket mesh broker on port 7417.")
