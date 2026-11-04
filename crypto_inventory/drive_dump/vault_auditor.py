
import os
import glob
import json

def audit_vault_folder(base_dir="."):
    print("======================================================")
    print("       UNIFORM VAULT AUDIT & GAP-ANALYSIS REPORT       ")
    print("======================================================\n")
    
    supported_extensions = ['.txt', '.json', '.csv', '.dat', '.bak']
    
    total_files = 0
    readable_files = 0
    unknown_formats = []




    
    # Walk through all folders and subfolders recursively
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            # Skip python scripts and report files themselves
            if file.endswith('.py') or file.endswith('_report.txt'):
                continue
                
            total_files += 1
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()
            
            print(f"[*] Analyzing: {file_path}")
            
            # Check file compatibility and requirements
            if file_ext in ['.txt', '.csv']:
                readable_files += 1
                print(f"    -> Status: Plain text format. Ready for direct parsing.")
            elif file_ext == '.json':
                readable_files += 1
                print(f"    -> Status: JSON structure. May require specific keys or decryption passwords.")
            elif file_ext in ['.dat', '.bak'] or file_ext == '':
                unknown_formats.append(file_path)
                print(f"    -> Status: Proprietary/Binary backup format.")
                print(f"    -> REQUIREMENT: Needs specific wallet schema, decryption password, or helper library.")
            else:
                unknown_formats.append(file_path)
                print(f"    -> Status: Unrecognized extension ({file_ext}).")
                print(f"    -> REQUIREMENT: Manual inspection or custom parser needed.")
            print("-" * 50)

    print("\n======================================================")
    print(f" AUDIT SUMMARY:")
    print(f" Total files scanned : {total_files}")
    print(f" Directly readable   : {readable_files}")
    print(f" Need requirements   : {len(unknown_formats)}")
    print("======================================================")

if __name__ == "__main__":
    audit_vault_folder()

