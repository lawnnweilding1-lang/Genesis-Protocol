import json
import hashlib

def canonicalize(data):
    """
    Serializes a dictionary deterministically according to Genesis v2.0.0 rules:
    - UTF-8 encoding
    - Sorted keys
    - Minimized whitespace
    """
    return json.dumps(data, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

def compute_hash(data, layer_type):
    """
    Computes SHA-256 integrity hash with the respective hash field omitted.
    """
    clean_data = data.copy()
    if layer_type == "GIR":
        clean_data.pop("provenance_hash", None)
    elif layer_type == "GLIR":
        clean_data.pop("stream_hash", None)
    
    canonical_string = canonicalize(clean_data)
    return hashlib.sha256(canonical_string.encode('utf-8')).hexdigest()

def validate_genesis_payload(payload_json_str):
    """
    Sequential validation pipeline executing error checks GEN-001 through GEN-005.
    """
    try:
        data = json.loads(payload_json_str)
    except Exception as e:
        return {"status": "REJECTED", "error_code": "GEN-005", "message": f"Malformed JSON: {str(e)}"}
    
    # Check Layer
    layer = data.get("layer")
    if layer not in ["GIR", "GLIR"]:
        return {"status": "REJECTED", "error_code": "GEN-004", "message": "Missing or invalid layer identifier."}
    
    # Check Version
    if data.get("spec_version") != "2.0.0":
        return {"status": "REJECTED", "error_code": "GEN-001", "message": "Unsupported or missing spec_version."}
    
    # Check Required Fields based on layer
    if layer == "GIR":
        if not all(k in data for k in ["metadata", "payload", "provenance_hash"]):
            return {"status": "REJECTED", "error_code": "GEN-002", "message": "Missing mandatory GIR fields."}
        expected_hash = compute_hash(data, "GIR")
        if data["provenance_hash"] != expected_hash:
            return {"status": "REJECTED", "error_code": "GEN-003", "message": "GIR cryptographic hash mismatch detected."}
            
    elif layer == "GLIR":
        if not all(k in data for k in ["tensor_stream", "stream_hash"]):
            return {"status": "REJECTED", "error_code": "GEN-002", "message": "Missing mandatory GLIR fields."}
        expected_hash = compute_hash(data, "GLIR")
        if data["stream_hash"] != expected_hash:
            return {"status": "REJECTED", "error_code": "GEN-003", "message": "GLIR cryptographic stream hash mismatch detected."}

    return {"status": "CONFORMANT", "error_count": 0, "errors": []}

if __name__ == "__main__":
    print("Genesis Reference Engine v2.0.0 Initialized.")

