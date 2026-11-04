# Genesis Framework Specification (v2.0.0-draft)
**Core Protocol, Schema Definition & Canonical Test Vectors**

## 1. Overview & Scope
The Genesis Framework defines a neutral, hardware-independent intermediate representation and conformance protocol. It separates raw data ingestion and evidence representation from downstream reasoning, ensuring cryptographic integrity verification and traceable provenance across distributed systems.

## 2. Terminology
* **Canonical Representation:** A normalized data structure independent of source implementation.
* **Provenance:** Metadata describing origin, transformation history, and integrity state.
* **Conformance:** Successful validation against required protocol rules.
* **Implementation Profile:** A deployment-specific adaptation that follows the core specification.

## 3. Global Protocol Rules & Serialization Standards
* **Specification Versioning:** All valid Genesis instances MUST declare a `spec_version` field conforming to Semantic Versioning (e.g., `"2.0.0"`). Instances with unrecognized versions MUST be rejected by conformance validators.
* **Canonical Serialization:** JSON structures MUST be serialized strictly using **UTF-8 encoding**, deterministic key sorting (`sort_keys=True`), minimized whitespace, standardized floating-point precision formatting, and preserved array ordering to ensure deterministic cross-implementation hashing.
* **Integrity Hash Exclusion:** Cryptographic integrity hashes (`provenance_hash` for GIR, `stream_hash` for GLIR) MUST be computed over the complete structural object with the respective integrity field explicitly omitted or popped.
* **Timestamp & Event Identity Model:** Timestamps (`ingestion_timestamp`, `normalization_timestamp`) are captured as Unix epoch floats (`float64`). Under the **Event Identity Model**, timestamps *are* included in the canonical object body prior to integrity hashing; two identical streams ingested at different times yield distinct hashes to preserve unique temporal identity tracking.
* **Extension Handling:** Instances may include an optional `"extensions": {}` container for custom namespaces. Older validators MUST ignore unknown extension fields, core schema fields CANNOT be overridden by extensions, and extension namespaces must be governed under version control.
* **Conformance Tiers:**
  * *Core Conformance:* Requires mandatory GIR/GLIR structure, `spec_version` compliance, shape metadata, and valid cryptographic hash verification.
  * *Extended Conformance:* Supports optional extension namespaces, confidence bounds, uncertainty flags, and advanced metadata profiles.

## 4. Genesis Intermediate Representation (GIR) Schema
GIR handles canonical evidence representation, preserving provenance, uncertainty, and contradictions without premature conclusions.

### Structure & Field Definitions
```json
{
  "layer": "GIR",
  "spec_version": "2.0.0",
  "ingestion_timestamp": 1719600000.0,
  "metadata": {
    "source": "string (Required - identifier of original data origin)",
    "type": "string (Required - category of evidence, e.g., 'event_log')",
    "confidence_bounds": "float (Optional - bounds between 0.0 and 1.0, default 1.0)"
  },
  "payload": {
    "content": "string (Required - raw or abstracted evidence content)",
    "uncertainty_flags": "array of strings (Optional - transient spikes or ambiguity markers)",
    "conflicting_assertions": "array of strings (Optional - recorded contradictions or opposing claims)"
  },
  "extensions": "object (Optional - custom namespaced extension data)",
  "provenance_hash": "string (Required - SHA-256 hex digest of the canonicalized instance)"
}

 
# Genesis-Protocol
