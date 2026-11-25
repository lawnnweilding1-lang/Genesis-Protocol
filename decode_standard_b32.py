import base64

# Standard Base32 usually expects padding and specific uppercase formatting
key_str = "HY71N-34HMY-8UT4S-LW5GR-7VNJE-RZYNV-BAPVT-N596R-XUUXD-WZQ84".replace("-", "")

# Add standard padding if needed
padded = key_str + "=" * ((8 - len(key_str) % 8) % 8)
print(f"[*] Processed String Length: {len(key_str)}")

# Let's write a direct standard 32-symbol mapper if standard base64/b32 strict encoder complains about 8/9
RFC32_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"

bits = []
for char in key_str:
    if char in RFC32_ALPHABET:
        bits.append(RFC32_ALPHABET.index(char))
    elif char in '89':
        # Map digits 8/9 if part of a custom variant
        bits.append(int(char))
    else:
        print(f"[*] Unhandled character: {char}")

print(f"[*] Successfully mapped {len(bits)} characters into integer values.")
