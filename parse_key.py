key_str = "HY71N-34HMY-8UT4S-LW5GR-7VNJE-RZYNV-BAPVT-N596R-XUUXD-WZQ84".replace("-", "")
print(f"[*] Raw Character Length: {len(key_str)}")

has_89 = any(c in '89' for c in key_str)
print(f"[*] Contains digits 8/9: {has_89}")

chunks = ["HY71N", "34HMY", "8UT4S", "LW5GR", "7VNJE", "RZYNV", "BAPVT", "N596R", "XUUXD", "WZQ84"]
print(f"[*] Total Chunks: {len(chunks)}")
for i, chunk in enumerate(chunks):
    print(f"    [{i}] {chunk}")
