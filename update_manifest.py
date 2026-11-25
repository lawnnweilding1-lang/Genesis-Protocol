import json

with open("genesis_spec_sealed.json", "r") as f:
    data = json.load(f)

data["ip_ownership"] = {
    "entity": "Genesis Enterprise LLC",
    "assignee": "Joshua Anthony Harry",
    "rights": "All commercial, structural, and intellectual property rights reserved."
}

with open("genesis_spec_sealed.json", "w") as f:
    json.dump(data, f, indent=2, sort_keys=True)

print("[+] IP Ownership & Licensing Metadata Injected.")
