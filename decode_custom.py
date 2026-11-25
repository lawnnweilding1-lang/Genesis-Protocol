# Uppercase Base58 / custom variant alphabet found in your token
ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZ"
base = len(ALPHABET)

key_str = "HY71N-34HMY-8UT4S-LW5GR-7VNJE-RZYNV-BAPVT-N596R-XUUXD-WZQ84".replace("-", "")

# Decode from base-N to a large integer
val = 0
for char in key_str:
    val = val * base + ALPHABET.index(char)

# Convert integer to raw bytes
byte_length = (val.bit_length() + 7) // 8
decoded_bytes = val.to_bytes(byte_length, 'big')

print(f"[*] Base Base: {base}")
print(f"[*] Decoded Integer: {val}")
print(f"[*] Decoded Hex: {decoded_bytes.hex()}")
