import os
import json

def parse_crypto_inventory(input_file="keys_input.txt", output_report="wallet_inventory_report.txt"):
    """
    Reads local keys, seed phrases, or public addresses offline,
    categorizes them, and outputs a formatted local inventory report.
    """
    print("--- Running Offline Crypto Inventory & Mapping ---")
    
    if not os.path.exists(input_file):
        print(f"[!] Input file '{input_file}' not found.")
        print(f"--> Create '{input_file}' in this folder and paste your keys/addresses line by line.")
        return

    inventory = []
    
    with open(input_file, "r") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines, 1):
        item = line.strip()
        if not item or item.startswith("#"):
            continue

        words = item.split()
        
        # Categorize item format
        if len(words) in [12, 18, 24]:
            entry_type = "Mnemonic Seed Phrase"
            notes = f"Contains {len(words)} words"
        elif len(item) in [64, 66] and not item.startswith("0x1"):
            entry_type = "Raw Hex Private Key"
            notes = "EVM / Secp256k1 key candidate"
        elif item.startswith("0x") and len(item) == 42:
            entry_type = "EVM Public Address"
            notes = "Ethereum / Polygon / BNB"
        elif item.startswith("1") or item.startswith("3") or item.startswith("bc1"):
            entry_type = "Bitcoin Public Address"
            notes = "Legacy, P2SH, or Bech32 Native SegWit"
        else:
            entry_type = "Uncategorized Raw Data"
            notes = "Manual inspection required"

        inventory.append({
            "id": idx,
            "type": entry_type,
            "data": item,
            "notes": notes
        })

    # Save formatted report locally
    with open(output_report, "w") as out:
        out.write("====================================================\n")
        out.write("     OFFLINE CRYPTO WALLET & ADDRESS INVENTORY     \n")
        out.write("====================================================\n\n")
        
        for record in inventory:
            out.write(f"Item #{record['id']} [{record['type']}]\n")
            out.write(f"  Data : {record['data']}\n")
            out.write(f"  Notes: {record['notes']}\n")
            out.write("-" * 52 + "\n")

    print(f"[+] Complete. Processed {len(inventory)} entries.")
    print(f"[+] Output written to: {output_report}")

if __name__ == "__main__":
    parse_crypto_inventory()

