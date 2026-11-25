key_str = "HY71N-34HMY-8UT4S-LW5GR-7VNJE-RZYNV-BAPVT-N596R-XUUXD-WZQ84".replace("-", "")

# Crockford's Base32 alphabet uses numbers/letters excluding I, L, O, U
# Let's check character frequency and unique symbols
unique_chars = sorted(list(set(key_str)))
print(f"[*] Unique Characters Used ({len(unique_chars)}): {''.join(unique_chars)}")
