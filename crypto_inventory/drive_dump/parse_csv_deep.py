import re
import json
from pathlib import Path
from datetime import datetime

def scan_text(text):
    btc_legacy = r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,33}\b'
    btc_bech32 = r'\bbc1[ac-hj-np-z0-9]{38,59}\b'
    eth_addr = r'\b0x[a-fA-F0-9]{40}\b'
    
    matches = set()
    for pattern in [btc_legacy, btc_bech32, eth_addr]:
        found = re.findall(pattern, text, re.IGNORECASE)
        for m in found:
            matches.add(m)
    return matches

def main():
    dump_dir = Path("/data/data/com.termux/files/home/crypto_inventory/drive_dump")
    csv_files = list(dump_dir.glob("*.csv"))
    
    if not csv_files:
        print("[!] No CSV files found in drive_dump.")
        return

    ledger_path = Path("assets_ledger.json")
    ledger_data = {"assets": []}
    if ledger_path.exists():
        try:
            with open(ledger_path, "r") as f:
                ledger_data = json.load(f)
        except Exception:
            pass

    existing_addresses = {item["address"] for item in ledger_data["assets"]}
    new_found_count = 0

    for csv_file in csv_files:
        print(f"[*] Deep parsing CSV: {csv_file.name}")
        with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
            for line_no, line in enumerate(f, start=1):
                addrs = scan_text(line)
                for addr in addrs:
                    if addr not in existing_addresses:
                        asset_entry = {
                            "address": addr,
                            "source": f"{csv_file.name}:line_{line_no}",
                            "discovered_at": datetime.now().isoformat()
                        }
                        ledger_data["assets"].append(asset_entry)
                        existing_addresses.add(addr)
                        new_found_count += 1
                        print(f"    [+] Found at line {line_no}: {addr}")

    with open(ledger_path, "w") as f:
        json.dump(ledger_data, f, indent=4)

    print(f"\n[*] CSV Deep Scan Complete. New addresses found: {new_found_count}. Total in ledger: {len(ledger_data['assets'])}")

if __name__ == "__main__":
    main()
