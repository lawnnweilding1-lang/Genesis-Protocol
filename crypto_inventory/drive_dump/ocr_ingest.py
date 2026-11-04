import os
import re
import json
from pathlib import Path
from datetime import datetime

def scan_text(text):
    # Expanded patterns: Full EVM, partial 0x, ENS domains, and token IDs
    eth_addr = r'\b0x[a-fA-F0-9]{40}\b'
    partial_eth = r'\b0x[a-fA-F0-9\.]{10,45}\b'
    ens_domain = r'\b[a-zA-Z0-9\-\.]+\.eth\b'
    token_id = r'token\s*id[:\s]*([0-9]+)'
    
    matches = set()
    
    for pattern in [eth_addr, partial_eth, ens_domain]:
        found = re.findall(pattern, text, re.IGNORECASE)
        for m in found:
            matches.add(m)
            
    # Also grab token IDs explicitly if present
    t_found = re.findall(token_id, text, re.IGNORECASE)
    for t in t_found:
        matches.add(f"TokenID:{t}")
        
    return matches

def main():
    photos_dir = Path("/data/data/com.termux/files/home/crypto_inventory/drive_dump/incoming_photos")
    photos_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Scanning local photo directory: {photos_dir}")
    image_files = list(photos_dir.glob("*.[jJ][pP][gG]")) + list(photos_dir.glob("*.[pP][nN][gG]")) + list(photos_dir.glob("*.[jJ][pP][eE][gG]"))
    
    if not image_files:
        print(f"[-] No images found in {photos_dir}.")
        return

    ledger_path = Path("assets_ledger.json")
    ledger_data = {"assets": []}
    if ledger_path.exists():
        try:
            with open(ledger_path, "r") as f:
                ledger_data = json.load(f)
        except Exception:
            pass

    existing_identifiers = {item["address"] for item in ledger_data["assets"]}
    new_found_count = 0

    for img_path in image_files:
        print(f"[*] Processing image: {img_path.name}")
        try:
            # Basic text blob combining filename and raw bytes/strings
            blob_text = img_path.name + "\n" + img_path.read_bytes().decode('utf-8', errors='ignore')
            
            # Try loading OCR via Pillow/Tesseract if available
            try:
                from PIL import Image
                import pytesseract
                ocr_text = pytesseract.image_to_string(Image.open(img_path))
                blob_text += "\n" + ocr_text
                print(f"    -> OCR text extracted successfully.")
            except ImportError:
                print(f"    -> Note: Tesseract/PIL module not loaded; parsing raw file strings.")

            identifiers = scan_text(blob_text)
            for ident in identifiers:
                if ident not in existing_identifiers:
                    asset_entry = {
                        "address": ident,
                        "source": f"handwritten_note:{img_path.name}",
                        "discovered_at": datetime.now().isoformat()
                    }
                    ledger_data["assets"].append(asset_entry)
                    existing_identifiers.add(ident)
                    new_found_count += 1
                    print(f"    [+] Logged to Ledger: {ident}")
        except Exception as e:
            print(f"    [!] Error reading image: {e}")

    with open(ledger_path, "w") as f:
        json.dump(ledger_data, f, indent=4)

    print(f"\n[*] Scan complete. Added {new_found_count} new entries. Total in ledger: {len(ledger_data['assets'])}")

if __name__ == "__main__":
    main()
