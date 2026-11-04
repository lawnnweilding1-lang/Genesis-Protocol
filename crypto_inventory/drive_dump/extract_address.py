import re
from pathlib import Path

root_dir = Path("/data/data/com.termux/files/home/storage/shared/Download")
pdf_path = root_dir / "Untitled document.pdf"

print(f"[*] Scanning {pdf_path.name} for cryptocurrency address patterns...")

if not pdf_path.exists():
    print(f"[!] Error: {pdf_path} not found.")
else:
    try:
        content = pdf_path.read_bytes()
        
        # Regex patterns for common crypto addresses
        btc_legacy = rb'\b[13][a-km-zA-HJ-NP-Z1-9]{25,33}\b'
        btc_bech32 = rb'\bbc1[ac-hj-np-z0-9]{38,59}\b'
        eth_addr = rb'\b0x[a-fA-F0-9]{40}\b'
        
        matches = set()
        for pattern in [btc_legacy, btc_bech32, eth_addr]:
            found = re.findall(pattern, content)
            for m in found:
                matches.add(m.decode('utf-8', errors='ignore'))
                
        if matches:
            print(f"\n[+] Found {len(matches)} potential candidate address(es):")
            for idx, addr in enumerate(matches, 1):
                print(f"    {idx}. {addr}")
        else:
            print("[-] No standard cryptocurrency address patterns matched in the document bytes.")
            
    except Exception as e:
        print(f"[!] Read exception: {e}")
