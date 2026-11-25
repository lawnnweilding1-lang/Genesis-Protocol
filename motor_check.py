def parse_derivation_path(path_str: str):
    elements = path_str.split('/')
    if elements[0] != 'm':
        raise ValueError("Path must start with 'm'")
    
    derivation_indices = []
    for el in elements[1:]:
        if not el:
            continue
        hardened = el.endswith("'") or el.endswith('h')
        val = int(el.rstrip("'h"))
        if hardened:
            val += 0x80000000
        derivation_indices.append(val)
        
    return derivation_indices

if __name__ == "__main__":
    test_path = "m/44'/60'/0'/0/0"
    indices = parse_derivation_path(test_path)
    print(f"[*] Local motor initialized in Termux.")
    print(f"[*] Target Path Indices for {test_path}: {indices}")
