import urllib.request
import json

# Replace with the address output from your previous script
target_address = "14T259V4v133j2x45e2K4s3R6T5h7y2w8"
endpoint = f"http://127.0.0.1:7417/address/{target_address}"

print(f"[*] Querying local mesh broker on port 7417 for: {target_address}")
try:
    req = urllib.request.Request(endpoint, headers={'User-Agent': 'Genesis-Motor/1.1'})
    with urllib.request.urlopen(req, timeout=3) as response:
        data = json.loads(response.read().decode())
        print(json.dumps(data, indent=2))
except Exception as e:
    print(f"[*] Local socket stream response: {e}")
