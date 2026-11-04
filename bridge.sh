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
