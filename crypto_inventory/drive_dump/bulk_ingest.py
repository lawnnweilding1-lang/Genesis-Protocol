import re
from pathlib import Path

def scan_text(text):
    btc_legacy = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,33}\b'
    btc_bech32 = r'\bbc1[ac-hj-np-z0-9]{38,59}\b'
    eth_addr = r'\b0x[a-fA-F0-9]{40}\b'
    
    matches = set()
    for pattern in [btc_legacy, btc_bech32, eth_addr]:
        found = re.findall(pattern, text)
        for m in found:
            matches.add(m)
    return matches

def main():
    search_paths = [
        Path("/data/data/com.termux/files/home/crypto_inventory/drive_dump"),
        Path("/data/data/com.termux/files/home/storage/shared/Download")
    ]
    
    print(f"[*] Starting comprehensive address scan...")
    total_found = set()

    for base_dir in search_paths:
        if not base_dir.exists():
            continue
        for f in base_dir.rglob("*"):
            if not any(x in str(f) for x in ["proc", "mountinfo", "bugreport"]):
                # 1. Check filename
                name_matches = scan_text(f.name)
                if name_matches:
                    print(f"\n[+] Found in FILENAME: {f.name}")
                    for addr in name_matches:
                        print(f"    -> {addr}")
                        total_found.add(addr)
                
                # 2. Check file content if it's a file
                if f.is_file():
                    try:
                        content = f.read_bytes().decode('utf-8', errors='ignore')
                        content_matches = scan_text(content)
                        if content_matches:
                            print(f"\n[+] Found in CONTENT of: {f.relative_to(base_dir)}")
                            for addr in content_matches:
                                print(f"    -> {addr}")
                                total_found.add(addr)
                    except Exception:
                        pass

    print(f"\n[*] Scan complete. Total unique addresses discovered: {len(total_found)}")

if __name__ == "__main__":
    main()
