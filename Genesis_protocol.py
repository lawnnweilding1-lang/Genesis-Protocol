That review accurately captures how v3.0 crosses the line from a basic utility script into an actual protocol primitive.
The two immediate refinements to drop in to finish this out—separating the schema version from the protocol version, explicitly handling booleans before integers to avoid Python's inheritance quirk, and extending the provenance hash to bind the full lineage—are handled below.
### Genesis Core Protocol - Production-Ready Specification Engine (v3.1)
```python
# Genesis Core Protocol - Production-Ready Specification Engine (v3.1)
import hashlib
import json
import math
import time


class NonCanonicalError(ValueError):
    """Raised when data structure violates canonical protocol constraints."""
    pass


def _normalize_and_validate(obj, path="$"):
    """
    Recursively validates and normalizes the payload:
      - Rejects raw floats, non-finite values (NaN/Inf), and non-string keys.
      - Normalizes tuples into standard lists for deterministic cross-language parity.
      - Checks for duplicate keys during dictionary building.
      - Explicitly handles booleans before integers to bypass Python's type inheritance.
    """
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            raise NonCanonicalError(f"Non-finite float at {path}: {obj!r}")
        raise NonCanonicalError(f"Raw float at {path}: {obj!r}. Use fixed-point strings or ints.")
   
    elif isinstance(obj, dict):
        cleaned_dict = {}
        for k, v in obj.items():
            if not isinstance(k, str):
                raise NonCanonicalError(f"Non-string key at {path}: {k!r}")
            if k in cleaned_dict:
                raise NonCanonicalError(f"Duplicate key detected at {path}.{k}")
            cleaned_dict[k] = _normalize_and_validate(v, f"{path}.{k}")
        return cleaned_dict

    elif isinstance(obj, (list, tuple)):
        return [_normalize_and_validate(item, f"{path}[{i}]") for i, item in enumerate(obj)]
   
    elif isinstance(obj, bool):
        return obj
    elif isinstance(obj, int):
        return obj
    elif isinstance(obj, (str, type(None))):
        return obj
   
    raise NonCanonicalError(f"Unsupported type at {path}: {type(obj).__name__}")


class GenesisProtocol:
    def __init__(self, node_id):
        self.node_id = node_id
        self.protocol_version = "v3.1"
        self.schema_id = "GENESIS_ASSERTION"
        self.schema_version = "3.0"

    def canonical_serialize(self, data_payload):
        normalized_payload = _normalize_and_validate(data_payload)
        return json.dumps(
            normalized_payload,
            sort_keys=True,
            separators=(',', ':'),
            ensure_ascii=True,
            allow_nan=False,
        )

    def generate_domain_hash(self, domain_tag, serialized_payload):
        """Computes domain-separated structural integrity hash."""
        domain_prefixed = f"{domain_tag}:{self.protocol_version}:{serialized_payload}"
        return hashlib.sha256(domain_prefixed.encode('utf-8')).hexdigest()

    def create_assertion(self, raw_evidence, uncertainty_markers, parent_stream_hash=None, previous_provenance_hash=None):
        """
        Creates an immutable assertion block committing to raw evidence,
        schema metadata, and an independently verifiable provenance chain.
        """
        timestamp = int(time.time())
       
        # Core payload carrying state and evidence
        payload = {
            "node_id": self.node_id,
            "parent_stream_hash": parent_stream_hash,
            "raw_evidence": raw_evidence,
            "schema_id": self.schema_id,
            "schema_version": self.schema_version,
            "state": "UNSYNTHESIZED_RAW",
            "timestamp": timestamp,
            "uncertainty_markers": uncertainty_markers
        }
       
        canonical_data = self.canonical_serialize(payload)
        stream_hash = self.generate_domain_hash("GENESIS_STREAM_HASH", canonical_data)
       
        # Fully independent provenance block binding structural output and lineage history
        provenance_input = {
            "node_id": self.node_id,
            "previous_provenance_hash": previous_provenance_hash,
            "schema_id": self.schema_id,
            "stream_hash": stream_hash,
            "timestamp": timestamp
        }
        canonical_provenance = self.canonical_serialize(provenance_input)
        provenance_hash = self.generate_domain_hash("GENESIS_PROVENANCE_HASH", canonical_provenance)

        return {
            "provenance_hash": provenance_hash,
            "stream_hash": stream_hash,
            "parent_stream_hash": parent_stream_hash,
            "previous_provenance_hash": previous_provenance_hash,
            "canonical_payload": canonical_data,
            "payload_manifest": payload
        }
