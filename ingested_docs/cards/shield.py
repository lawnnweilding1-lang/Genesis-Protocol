import requests

def inspect_account(rpc_url: str, target_address: str):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getCode",
        "params": [target_address, "latest"],
        "id": 1
    }
    res = requests.post(rpc_url, json=payload).json()
    code = res.get("result", "0x")
    
    if code.startswith("0xef0100"):
        impl_address = "0x" + code[8:48]
        return {
            "status": "delegated",
            "stub": code[:48],
            "implementation": impl_address
        }
    return {"status": "standard_eoa", "code": code}

def build_reset_tuple(rpc_url: str, target_address: str, chain_id: int):
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_getTransactionCount",
        "params": [target_address, "latest"],
        "id": 1
    }
    res = requests.post(rpc_url, json=payload).json()
    current_nonce = res.get("result", "0x1")
    
    return {
        "chainId": hex(chain_id),
        "address": "0x0000000000000000000000000000000000000000",
        "nonce": current_nonce,
        "yParity": "0x0",
        "r": "0x0",
        "s": "0x0"
    }

if __name__ == "__main__":
    rpc = "https://mainnet.base.org"
    target = "0xF32Af3c9c612A9339D94D2c60c8651172e1be8A4"
    
    print("[+] Inspecting target account on Base...")
    status = inspect_account(rpc, target)
    print("Inspection Result:", status)
    
    reset_tuple = build_reset_tuple(rpc, target, 8453)
    print("Reset Tuple Prepared:", reset_tuple)
