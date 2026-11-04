import os
import shutil

def check_and_sync_storage():
    print("======================================================")
    print("          TERMUX STORAGE INGESTION CHECKER            ")
    print("======================================================\n")
    
    # Potential storage paths on Android/Termux
    search_paths = [
        os.path.expanduser("~/storage/downloads"),
        os.path.expanduser("~/storage/shared/Download"),
        "/storage/emulated/0/Download",
        os.path.expanduser("~/downloads")
    ]
    
    target_dir = os.path.expanduser("~/crypto_inventory/drive_dump")
    os.makedirs(target_dir, exist_ok=True)
    
    found_any = False
    
    for path in search_paths:
        print(f"[*] Checking path: {path}")
        if os.path.exists(path):
            print(f"    -> SUCCESS: Path exists.")
            try:
                items = os.listdir(path)
                print(f"    -> Found {len(items)} items.")
                for item in items:
                    if item.startswith('.'):
                        continue
                    src_item = os.path.join(path, item)
                    print(f"        - Discovered: {item}")
                    found_any = True
                    
                    # Copy item to workspace
                    dest_item = os.path.join(target_dir, item)
                    if os.path.isdir(src_item):
                        if not os.path.exists(dest_item):
                            shutil.copytree(src_item, dest_item)
                            print(f"          [+] Copied folder to workspace.")
                    else:
                        shutil.copy2(src_item, dest_item)
                        print(f"          [+] Copied file to workspace.")
            except Exception as e:
                print(f"    -> Error reading directory: {e}")
        else:
            print(f"    -> Path not accessible or doesn't exist.")
        print("-" * 50)
        
    print("\n======================================================")
    if found_any:
        print(" SYNC COMPLETE: Files moved to ~/crypto_inventory/drive_dump/")
        print(" Run: python3 vault_auditor.py")
    else:
        print(" STATUS: No items found in standard download paths yet.")
        print(" Try sharing/saving a file directly to Termux or check permissions.")
    print("======================================================")

if __name__ == "__main__":
    check_and_sync_storage()

