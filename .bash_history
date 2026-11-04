        
        banner = s.recv(1024).decode('utf-8')
        s.sendall((OVERRIDE_CODE + "\n").encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
        
        print(f"AUTHENTICATION: {response.strip()}")
        print("\n--- ACTIVE INFRASTRUCTURE PIPELINE ---")
        for key, name in INFRASTRUCTURE_NODES.items():
            print(f"[{key}] {name:<30} [STATUS: ACTIVE]")
        print("--------------------------------------------------")
        print("BRIDGE STATUS: SECURE & FULLY OPERATIONAL")
        print("==================================================")
        s.close()
    except Exception as e:
        print(f"Bridge connection error: {e}")

if __name__ == "__main__":
    ignite_dashboard()
EOF

python3 genesis_dashboard.py
cat << 'EOF' > genesis_dashboard.py
import socket

PORT = 7417
OVERRIDE_CODE = "avaai"

# Wedge Infrastructure Nodes [1] through [4]
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
    print("Connecting to Workhorse Node on port 7417...")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", PORT))
        
        banner = s.recv(1024).decode('utf-8')
        s.sendall((OVERRIDE_CODE + "\n").encode('utf-8'))
        response = s.recv(1024).decode('utf-8')
        
        print(f"AUTHENTICATION: {response.strip()}")
        print("\n--- ACTIVE WEDGE PIPELINE NODES ---")
        for key, name in WEDGE_NODES.items():
            print(f"{key} {name:<35} [STATUS: ONLINE]")
        print("--------------------------------------------------")
        print("BRIDGE STATUS: SECURE & FULLY OPERATIONAL")
        print("==================================================")
        s.close()
    except Exception as e:
        print(f"Bridge connection error: {e}")

if __name__ == "__main__":
    ignite_dashboard()
EOF

python3 genesis_dashboard.py
cat << 'EOF' > genesis_dashboard.py
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
EOF

genesis_orchestrator.py
cat << 'EOF' > genesis_orchestrator.py
import hashlib, os, sys, socket, time, logging

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [GENESIS-CORE] %(message)s")
MASTER_OVERRIDE_HASH = hashlib.sha256(b"avaai").hexdigest()
PORT = 7417

def run_workhorse():
    logging.info("INITIALIZING GENESIS LLC INFRASTRUCTURE ON PORT %d...", PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    while True:
        try:
            s.bind(("0.0.0.0", PORT))
            s.listen(5)
            logging.info("WORKHORSE NODE ONLINE. Awaiting Master Controller...")
            
            while True:
                conn, addr = s.accept()
                logging.info("Incoming connection from: %s", addr)
                conn.sendall(b"GENESIS LLC SECURE ROOM 7417 - ENTER OVERRIDE CODE:\n")
                data = conn.recv(1024).decode('utf-8').strip()
                
                if hashlib.sha256(data.lower().encode('utf-8')).hexdigest() == MASTER_OVERRIDE_HASH:
                    conn.sendall(b"ACCESS GRANTED: WELCOME BACK, BOSS.\n")
                    logging.info("MASTER OVERRIDE ACCEPTED FROM %s.", addr)
                else:
                    conn.sendall(b"ACCESS DENIED.\n")
                conn.close()
        except Exception as e:
            logging.error("Socket error: %s. Restarting bind in 3s...", e)
            time.sleep(3)

if __name__ == "__main__":
    run_workhorse()
EOF

python3 genesis_orchestrator.py
# 1. List available models on disk to ensure paths and directories align
lms ls
# 2. Load your primary GGUF model into memory 
# (Replace with your exact model identifier or file path shown from 'lms ls')
lms load qwen --gpu max
# 3. Start the server daemon bound to 0.0.0.0 (all interfaces) with CORS enabled
lms server start --bind 0.0.0.0 --cors true
# 4. Run the local sanity check endpoint
curl http://localhost:1234/v1/models
cat << 'EOF' > bridge.sh
#!/bin/bash

# Configuration (Change these to match your Beelink machine)
HOST_USER="your_username"
HOST_IP="192.168.1.X"
MODEL_ID="qwen" # Or your exact model identifier

echo "[-] Establishing SSH bridge to Beelink ($HOST_IP)..."

# This opens the SSH tunnel (-N keeps it open), forwards port 1234, 
# and triggers the remote lms startup commands in the background
ssh -N -L 1234:localhost:1234 "$HOST_USER@HOST_IP" &
SSH_PID=$!

echo "[-] Loading model ($MODEL_ID) and starting server on host..."
ssh "$HOST_USER@HOST_IP" "lms load $MODEL_ID --gpu max && lms server start --bind 0.0.0.0 --cors true"

echo "[+] Bridge active! Local endpoint ready at http://localhost:1234"
echo "[-] Press Ctrl+C to tear down the bridge."

# Keep script alive until you kill it, then cleanup the background tunnel
trap "kill $SSH_PID; echo '[-] Bridge closed.';" EXIT
wait $SSH_PID
EOF

chmod +x bridge.sh
./bridge.sh
pkg install -y openssh
./bridge.sh
cat << 'EOF' > bridge.sh
#!/bin/bash

# --- PUT YOUR ACTUAL DETAILS HERE ---
HOST_USER="YOUR_USER"
HOST_IP="YOUR_BEELINK_IP"
MODEL_ID="qwen"
# ------------------------------------

echo "[-] Establishing SSH tunnel to Beelink ($HOST_IP)..."
ssh -N -L 1234:localhost:1234 "$HOST_USER@$HOST_IP" &
SSH_PID=$!

echo "[-] Loading model ($MODEL_ID) and starting server on host..."
ssh "$HOST_USER@$HOST_IP" "lms load $MODEL_ID --gpu max && lms server start --bind 0.0.0.0 --cors true"

echo "[+] Bridge active! Local endpoint ready at http://localhost:1234"
echo "[-] Press Ctrl+C to tear down the bridge."

trap "kill $SSH_PID 2>/dev/null; echo '[-] Bridge closed.';" EXIT
wait $SSH_PID
EOF

cat << 'EOF' > bridge.sh
#!/bin/bash

# --- AUTO-CONFIGURED ---
HOST_USER="joshua-harry"
HOSTNAME_TARGET="joshua-harry-SER"
MODEL_ID="qwen"
# -----------------------

echo "[-] Searching local network for $HOSTNAME_TARGET..."

# Try resolving via mDNS (.local) or hostname lookup
HOST_IP=$(ping -c 1 "$HOSTNAME_TARGET.local" 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | head -n 1)
if [ -z "$HOST_IP" ]; then
    HOST_IP=$(ping -c 1 "$HOSTNAME_TARGET" 2>/dev/null | grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | head -n 1)
fi

# Fallback: scan local subnet if direct resolution misses
if [ -z "$HOST_IP" ]; then
    echo "[-] Direct lookup failed, scanning local subnet..."
    SUBNET=$(ip route | grep -oE 'src [0-9]+\.[0-9]+\.[0-9]+\.' | head -n 1 | awk '{print $2}')
    if [ -z "$SUBNET" ]; then
        SUBNET="192.168.1."
    fi
    for i in {1..254}; do
        IP="${SUBNET}${i}"
        if nc -z -w 1 "$IP" 22 2>/dev/null; then
            if ssh -o ConnectTimeout=1 -o BatchMode=yes "$HOST_USER@$IP" exit 2>/dev/null; then
                HOST_IP="$IP"
                break
            fi
        fi
    done
fi

if [ -z "$HOST_IP" ]; then
    echo "[X] Could not automatically locate $HOSTNAME_TARGET. Ensure both devices are on the same Wi-Fi."
    exit 1
fi

echo "[+] Located Beelink at: $HOST_IP"
echo "[-] Establishing SSH tunnel..."
ssh -N -L 1234:localhost:1234 "$HOST_USER@$HOST_IP" &
SSH_PID=$!

echo "[-] Loading model ($MODEL_ID) and starting server on host..."
ssh "$HOST_USER@$HOST_IP" "lms load $MODEL_ID --gpu max && lms server start --bind 0.0.0.0 --cors true"

echo "[+] Bridge active! Local endpoint ready at http://localhost:1234"
echo "[-] Press Ctrl+C to tear down the bridge."

trap "kill $SSH_PID 2>/dev/null; echo '[-] Bridge closed.';" EXIT
wait $SSH_PID
EOF

chmod +x bridge.sh
./bridge.sh
ssh -o StrictHostKeyChecking=no -N -L 1234:localhost:1234 joshua-harry@192.168.1.83
ssh -o StrictHostKeyChecking=no joshua-harry@192.168.1.83 "lms load qwen --gpu max && lms server start --bind 0.0.0.0 --cors true"
ping -c 3 192.168.1.83
echo "=== SYSTEM & KERNEL ===" && uname -r && lsb_release -a && echo -e "\n=== CPU & HARDWARE ===" && lscpu | grep -E "Model name|Architecture|CPU\(s\):" && echo -e "\n=== MEMORY USAGE ===" && free -h && echo -e "\n=== DISK SPACE ===" && df -h /
python3 master_orchestrator.py
import requests
import json
import socket
# Genesis Framework: Custom Gateway Configuration
GATEWAY_PORT = 7417
LOCAL_ENDPOINT = f"http://localhost:{GATEWAY_PORT}/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}
def verify_and_build_gate(port):
class MasterAgentController:
if __name__ == "__main__":
    verify_and_build_gate(GATEWAY_PORT)
import requests
import json
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler
# Genesis Framework: Secure Hardware-Bound Gateway (Port 7417)
GATEWAY_PORT = 7417
# This token must match the auth signature generated/held by your main B-Link node
BLINK_AUTHORIZED_TOKEN = "blink-root-auth-7417-x99"
class SecureGateHandler(BaseHTTPRequestHandler):
def run_secure_gateway():
cat << 'EOF' > secure_gate.py
import requests
import json
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

GATEWAY_PORT = 7417
BLINK_AUTHORIZED_TOKEN = "blink-root-auth-7417-x99"

class SecureGateHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        auth_header = self.headers.get("Authorization")
        expected_bearer = f"Bearer {BLINK_AUTHORIZED_TOKEN}"
        
        if not auth_header or auth_header != expected_bearer:
            print(f"[!] ACCESS DENIED: Unauthorized payload attempt on port {GATEWAY_PORT}.")
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response_data = {"error": "Unauthorized: B-Link hardware token validation failed."}
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return

        print(f"[✔] B-Link Auth Verified: Channel open on port {GATEWAY_PORT}.")
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        reply = {"status": "success", "message": "Gate open. Command executed via B-Link authorization."}
        self.wfile.write(json.dumps(reply).encode("utf-8"))

def run_secure_gateway():
    server_address = ('127.0.0.1', GATEWAY_PORT)
    httpd = HTTPServer(server_address, SecureGateHandler)
    print(f"[+] Secure Genesis Gate listening on port {GATEWAY_PORT}...")
    print(f"[+] Locked to B-Link Node Authorization Token.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down secure gate.")
        httpd.server_close()

if __name__ == "__main__":
    run_secure_gateway()
EOF

cat << 'EOF' > secure_gate.py
import requests
import json
import socket
from http.server import HTTPServer, BaseHTTPRequestHandler

GATEWAY_PORT = 7417
BLINK_AUTHORIZED_TOKEN = "blink-root-auth-7417-x99"

class SecureGateHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        auth_header = self.headers.get("Authorization")
        expected_bearer = f"Bearer {BLINK_AUTHORIZED_TOKEN}"
        
        if not auth_header or auth_header != expected_bearer:
            print(f"[!] ACCESS DENIED: Unauthorized payload attempt on port {GATEWAY_PORT}.")
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response_data = {"error": "Unauthorized: B-Link hardware token validation failed."}
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
            return

        print(f"[✔] B-Link Auth Verified: Channel open on port {GATEWAY_PORT}.")
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        reply = {"status": "success", "message": "Gate open. Command executed via B-Link authorization."}
        self.wfile.write(json.dumps(reply).encode("utf-8"))

def run_secure_gateway():
    server_address = ('127.0.0.1', GATEWAY_PORT)
    httpd = HTTPServer(server_address, SecureGateHandler)
    print(f"[+] Secure Genesis Gate listening on port {GATEWAY_PORT}...")
    print(f"[+] Locked to B-Link Node Authorization Token.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down secure gate.")
        httpd.server_close()

if __name__ == "__main__":
    run_secure_gateway()
EOF

python3 secure_gate.py
y
pkg update && pkg install python python-pip -y
ollama list
y
hostname -I
python3 -c "import socket; s = socket.socket(); s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1); s.bind(('0.0.0.0', 7417)); s.listen(1); print('WORKHORSE ONLINE: Bound to port 7417. Awaiting Master Orchestrator...'); conn, addr = s.accept(); print('Connected to Master Orchestrator:', addr)"
#!/usr/bin/env python3
import os, sys, socket, subprocess, json, logging
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [ORCHESTRATOR] %(message)s")
PORT = 7417
MODELS = {"qwen": "Qwen2.5-VL", "deepseek": "DeepSeek-R1", "chatgpt_mimic": "GPT-Proxy", "orchestrator": "Genesis-Core"}
def verify_environment():
def spin_listener():
if __name__ == "__main__":;     verify_environment()
curl --request GET   --url 'https://api.etherscan.io/v2/api?chainid=1&module=account&action=balance&address=0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045&tag=latest&apikey=YourApiKey'
pkg update && pkg upgrade -y
pkg install netcat-openbsd openssh net-tools -y
# Listen on TCP port 8080
nc -lvp 8080
nc -zv 192.168.1.103 7417
termux-wake-lock
nc -zv 127.0.0.1 7417
ip route | grep default
node audit-hasher.js ./your-document.pdf
const fs = require('node:fs');
const { createHash } = require('node:crypto');
const path = require('node:path');
// Pass your file path as an argument, e.g.: node audit-hasher.js ./documents/genesis-blueprint.pdf
const targetFile = process.argv[2];
}
try {
} catch (error) {
}
node audit-hasher.js ./your-document.pdf
pkg update && pkg install -y curl jq
#!/data/data/com.termux/files/usr/sh
# Usage:
#   ./lookup.sh token <TOKEN_CONTRACT_ADDRESS>
#   ./lookup.sh balance <WALLET_ADDRESS>
COMMAND=$1
TARGET=$2
if [ -z "$COMMAND" ] || [ -z "$TARGET" ]; then   echo "Usage:";   echo "  $0 token <0xTokenContractAddress>";   echo "  $0 balance <0xWalletAddress>";   exit 1; fi
pkg update && pkg install -y curl jq
#!/data/data/com.termux/files/usr/sh
# Usage:
#   ./lookup.sh token <TOKEN_CONTRACT_ADDRESS>
#   ./lookup.sh balance <WALLET_ADDRESS>
COMMAND=$1
TARGET=$2
if [ -z "$COMMAND" ] || [ -z "$TARGET" ]; then   echo "Usage:";   echo "  $0 token <0xTokenContractAddress>";   echo "  $0 balance <0xWalletAddress>";   exit 1; fi
your_secret_value
your_secret_valuepip install bip-utils
from bip_utils import Bip39MnemonicGenerator, Bip39EntropyGenerator
# Option A: Convert raw hex entropy directly into a 12/24 word recovery phrase
raw_hex = "YOUR_RAW_HEX_STRING_HERE"  # Replace with your raw hex/bits
mnemonic = Bip39MnemonicGenerator().FromEntropy(bytes.fromhex(raw_hex))
print("Your Recovery Phrase:")
print(mnemonic)
cp -r ~/storage/shared/Download/* ~/crypto_inventory/drive_dump/
cd ~/crypto_inventory/drive_dump
python3 vault_auditor.py
nano storage_check.py
[200~nano storage_check.py
~import os
import shutil
def check_and_sync_storage():
if __name__ == "__main__":;     check_and_sync_storage() exit
exit
nano vault_auditor.py
python3 vault_auditor.py
# Move any newly shared files into your drive dump directory
mv ~/*Coinbase* ~/crypto_inventory/drive_dump/ 2>/dev/null
mv ~/*Trust* ~/crypto_inventory/drive_dump/ 2>/dev/null
# Jump into your directory and run the audit
cd ~/crypto_inventory/drive_dump
python3 vault_auditor.py
ls -la ~
# Move any backup folders or files from your home directory into your drive_dump folder
mv ~/CoinbaseWalletBackups ~/crypto_inventory/drive_dump/ 2>/dev/null
mv ~/TrustWalletBackup ~/crypto_inventory/drive_dump/ 2>/dev/null
cd ~/crypto_inventory/drive_dump
python3 vault_auditor.py
nano vault_auditor.py
python3 vault_auditor.py
exit
print("Your Recovery Phrase:")nano vault_auditor.py
import os
import glob
import json
def audit_vault_folder(base_dir="."):
if __name__ == "__main__":;     audit_vault_folder() security or missing dependencies.  
​Right now, your terminal is throwing bash syntax errors because some Python code accidentally got pasted straight into the command line prompt instead of inside the text editor (nano).  
​Let's clean that up right now with these quick steps:
​1. Close this terminal session
​Type exit
security or missing dependencies.  
​Right now, your terminal is throwing bash syntax errors because some Python code accidentally got pasted straight into the command line prompt instead of inside the text editor (nano).  
​Let's clean that up right now with these quick steps:
​1. Close this terminal session
​Type exit
exit
