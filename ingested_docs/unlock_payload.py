import sys
from pathlib import Path
from cryptography.fernet import Fernet

KEY_PATH = Path.home() / ".config" / "genesis" / "key.key"

def decrypt_payload(token_str: str):
    if not KEY_PATH.exists():
        print("[-] Error: Local decryption key not found on this node.")
        sys.exit(1)
    
    key = KEY_PATH.read_bytes()
    f = Fernet(key)
    try:
        decrypted = f.decrypt(token_str.encode())
        print("\n[+] UNLOCKED DATA:")
        print(decrypted.decode())
    except Exception as e:
        print(f"[-] Decryption failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 unlock_payload.py '<cipher_text>'")
        sys.exit(1)
    decrypt_payload(sys.argv[1])
