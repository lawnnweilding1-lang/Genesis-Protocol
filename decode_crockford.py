import sys

# Crockford's Base32 symbol map
CROCKFORD_MAP = {
    '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
    'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17,
    'J': 18, 'K': 19, 'M': 20, 'N': 21, 'P': 22, 'Q': 23, 'R': 24, 'S': 25,
    'T': 26, 'V': 27, 'W': 28, 'X': 29, 'Y': 30, 'Z': 31,
    # Handle common substitutions (I/L -> 1, O -> 0)
    'I': 1, 'L': 1, 'O': 0
}

key_str = "HY71N-34HMY-8UT4S-LW5GR-7VNJE-RZYNV-BAPVT-N596R-XUUXD-WZQ84".replace("-", "")

# Convert symbols to 5-bit integer array
bits = []
for char in key_str:
    if char in CROCKFORD_MAP:
        bits.append(CROCKFORD_MAP[char])
    else:
        print(f"[*] Unknown character: {char}")

print(f"[*] Successfully parsed {len(bits)} symbols into 5-bit values.")
