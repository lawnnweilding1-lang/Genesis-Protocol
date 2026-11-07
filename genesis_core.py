import json
import hashlib
import os
import subprocess

def canonical_hash_gir(data: dict) -> str:
    target = data.copy()
    target.pop("provenance_hash", None)
    target.pop("stream_hash", None)
    canonical_json = json.dumps(target, sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    return hashlib.sha256(canonical_json.encode('utf-8')).hexdigest()

# Define Master Spec Payload
payload = {
    "layer": "GIR",
    "spec_version": "2.0.0",
    "ingestion_timestamp": 1719600000.0,
    "metadata": {
        "source": "apex_architectures_terminal",
        "type": "event_log",
        "confidence_bounds": 1.0
    },
    "payload": {
        "content": "Genesis Framework Sovereign State Integrity Protocol",
        "uncertainty_flags": [],
        "conflicting_assertions": []
    },
    "extensions": {}
}

# Compute Hash
payload["provenance_hash"] = canonical_hash_gir(payload)

# Write out file
with open("genesis_spec_sealed.json", "w") as f:
    json.dump(payload, f, indent=2, sort_keys=True)

print("[+] Sealed Genesis Protocol Specification Generated.")
print(f"[+] Provenance Hash: {payload['provenance_hash']}")
