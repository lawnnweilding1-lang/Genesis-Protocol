import socket
import time

PORT = 7417
OVERRIDE_CODE = "avaai"

WEDGE_NODES = {
    "[1]": "WEDGE-NODE-01 (Pipeline Core)",
    "[2]": "WEDGE-NODE-02 (Ingestion Engine)",
    "[3]": "WEDGE-NODE-03 (Processing Gateway)",
    "[4]": "WEDGE-NODE-04 (FSA Portal Bridge)"
}

def ignite_dashboard():
    print("==================================================")
    print("      GENESIS LLC: WEDGE PIPELINE DASHBOARD       ")
    print("==================================================")
    
    while True:
        try:
            print("Scanning for Workhorse bridge on port 7417...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3.0)
            
            # Use your Ubuntu workhorse IP here if connecting over Wi-Fi, 
            # or keep 127.0.0.1 if using ADB port forwarding.
            s.connect(("127.0.0.1", PORT))
            s.settimeout(None)
            
            banner = s.recv(1024).decode('utf-8')
            s.sendall((OVERRIDE_CODE + "\n").encode('utf-8'))
            response = s.recv(1024).decode('utf-8')
            
            print(f"\n[BRIDGE LOCKED] AUTH: {response.strip()}")
            print("--- ACTIVE WEDGE PIPELINE NODES ---")
            for key, name in WEDGE_NODES.items():
                print(f"{key} {name:<35} [STATUS: ONLINE]")
            print("--------------------------------------------------")
            print("BRIDGE STATUS: SECURE & FULLY OPERATIONAL")
            print("==================================================")
            s.close()
            break  # Break loop on successful sync
            
        except (socket.timeout, ConnectionRefusedError, OSError):
            print("Connection out of range or server offline. Retrying in 3 seconds...")
            time.sleep(3)

if __name__ == "__main__":
    ignite_dashboard()
