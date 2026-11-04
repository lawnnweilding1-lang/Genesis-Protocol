#!/bin/bash
echo "=== APEX ARCHITECTURES: SYSTEM CHECK ==="
echo "Timestamp: $(date)"
echo ""
echo "[Uptime]"
uptime -p
echo ""
echo "[Network Interfaces (ifconfig / ip route)]"
ifconfig 2>/dev/null || ip route show
echo ""
echo "[Active Connections via netstat]"
netstat -tn 2>/dev/null || ss -tn 2>/dev/null || cat /proc/net/tcp
echo "========================================"
