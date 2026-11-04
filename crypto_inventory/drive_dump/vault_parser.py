import os
from pathlib import Path

root_dir = Path("/data/data/com.termux/files/home/storage/shared/Download")
print(f"[*] Initializing Binary Vault Parser targeting: {root_dir}")

binary_files = [
    f for f in root_dir.rglob("*") 
    if f.is_file() and not f.name.endswith(".py") and (
        f.suffix.lower() in ['.dat', '.bin', ''] or 
        'wallet' in f.name.lower() or 
        'bugreport' in f.name.lower()
    )
]

print(f"[*] Found {len(binary_files)} binary/vault candidates for deep inspection.\n")

for bfile in binary_files:
    print(f"--- Inspecting: {bfile.relative_to(root_dir)} ---")
    try:
        with open(bfile, 'rb') as f:
            header = f.read(64)
            if header.startswith(b'SQLite format 3'):
                print("   [+] Signature Match: SQLite Database (Index/Wallet structure)")
            elif b'\x00\x05\x31\x62' in header or b'\x62\x31\x05\x00' in header:
                print("   [+] Signature Match: Berkeley DB (Classic wallet.dat format)")
            elif b'xprv' in header or b'xpub' in header:
                print("   [+] Signature Match: Extended Key Material (xprv/xpub)")
            else:
                print(f"   [i] Custom/Raw Binary Blob (First 16 hex bytes): {header[:16].hex()}")
    except Exception as e:
        print(f"   [!] Read exception: {e}")

print("\n[*] Binary vault inspection pass complete.")
