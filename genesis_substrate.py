import hashlib
import hmac
import json
import os
import time
from typing import Any, Dict, Optional


FILE_FORMAT_PLACEHOLDERS: Dict[str, Dict[str, Any]] = {
    "documents_text": {
        "formats": [".pdf", ".docx", ".txt", ".md"],
        "slots": {f: {"status": "PLACEHOLDER_READY", "sha256": None, "path": None} for f in [".pdf", ".docx", ".txt", ".md"]},
    },
    "spreadsheets_tables": {
        "formats": [".csv", ".xlsx", ".ods"],
        "slots": {f: {"status": "PLACEHOLDER_READY", "sha256": None, "path": None} for f in [".csv", ".xlsx", ".ods"]},
    },
    "structured_data_manifests": {
        "formats": [".json", ".jsonl", ".yaml", ".xml", ".toml"],
        "slots": {f: {"status": "PLACEHOLDER_READY", "sha256": None, "path": None} for f in [".json", ".jsonl", ".yaml", ".xml", ".toml"]},
    },
    "databases_ledgers": {
        "formats": [".sqlite", ".sql", ".parquet"],
        "slots": {f: {"status": "PLACEHOLDER_READY", "sha256": None, "path": None} for f in [".sqlite", ".sql", ".parquet"]},
    },
    "images_optical": {
        "formats": [".png", ".jpg", ".webp", ".svg", ".tiff"],
        "slots": {f: {"status": "PLACEHOLDER_READY", "sha256": None, "path": None} for f in [".png", ".jpg", ".webp", ".svg", ".tiff"]},
    },
    "audio_sensor_media": {
        "formats": [".wav", ".mp3", ".mp4", ".bin"],
        "slots": {f: {"status": "PLACEHOLDER_READY", "sha256": None, "path": None} for f in [".wav", ".mp3", ".mp4", ".bin"]},
    },
    "code_scripts_wasm": {
        "formats": [".py", ".rs", ".go", ".wasm"],
        "slots": {f: {"status": "PLACEHOLDER_READY", "sha256": None, "path": None} for f in [".py", ".rs", ".go", ".wasm"]},
    },
    "archives_crypto_cad": {
        "formats": [".zip", ".tar.gz", ".pem", ".stl"],
        "slots": {f: {"status": "PLACEHOLDER_READY", "sha256": None, "path": None} for f in [".zip", ".tar.gz", ".pem", ".stl"]},
    },
}


class GenesisMasterSubstrate:
    def __init__(self, pre_shared_key: bytes, gatekeeper_pass: str):
        self._psk = pre_shared_key
        self._gatekeeper_pass = gatekeeper_pass
        self.format_registry = json.loads(json.dumps(FILE_FORMAT_PLACEHOLDERS))

    @staticmethod
    def canonical_serialize(payload: Dict[str, Any]) -> bytes:
        return json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
        ).encode("utf-8")

    @staticmethod
    def compute_file_sha256(file_path: str) -> str:
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                h.update(chunk)
        return h.hexdigest()

    def set_format_placeholder(
        self,
        family: str,
        ext: str,
        sha256_digest: Optional[str] = None,
        source_path: Optional[str] = None,
        status_label: str = "PLACEHOLDER_READY",
    ) -> None:
        if family not in self.format_registry:
            raise KeyError(f"Unknown format family: {family}")
        if ext not in self.format_registry[family]["slots"]:
            raise KeyError(f"Extension {ext} not registered in {family}")
        self.format_registry[family]["slots"][ext] = {
            "status": "BOUND" if sha256_digest else status_label,
            "sha256": sha256_digest,
            "path": source_path,
        }

    def bind_local_file(self, family: str, ext: str, file_path: str) -> str:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Target file not found: {file_path}")
        digest = self.compute_file_sha256(file_path)
        self.set_format_placeholder(family, ext, sha256_digest=digest, source_path=file_path)
        return digest

    def registry_summary(self) -> Dict[str, Any]:
        total_slots = 0
        bound_slots = 0
        ready_slots = 0
        for fam in self.format_registry.values():
            for slot in fam["slots"].values():
                total_slots += 1
                if slot["status"] == "BOUND":
                    bound_slots += 1
                else:
                    ready_slots += 1
        return {
            "families": len(self.format_registry),
            "total_slots": total_slots,
            "bound_slots": bound_slots,
            "placeholder_ready_slots": ready_slots,
        }

    @staticmethod
    def build_qr_channel_matrix(
        red_restricted_pointer: str,
        cyan_telemetry_stream: str,
        yellow_routing_nonce: str,
        black_root_anchor: str,
    ) -> Dict[str, str]:
        return {
            "matrix_mode": "OPTICAL_QUAD_CHANNEL_2FA",
            "red_channel_gated_lane": red_restricted_pointer,
            "cyan_channel_signal_lane": cyan_telemetry_stream,
            "yellow_channel_nonce_lane": yellow_routing_nonce,
            "black_channel_root_anchor": black_root_anchor,
        }

    def seal_master_block(
        self,
        nonce: str,
        binary_stream_hex: str,
        acoustic_signature: Dict[str, Any],
        sphere_3d_grid: Dict[str, Any],
        json_manifest: Dict[str, Any],
        optical_qr_channels: Dict[str, str],
        restricted_math_layer: Dict[str, Any],
    ) -> Dict[str, Any]:
        public_patterns = {
            "01_binary_stream": binary_stream_hex,
            "02_acoustic_waveform": acoustic_signature,
            "03_spatial_3d_topology": sphere_3d_grid,
            "04_json_manifest": json_manifest,
            "05_optical_qr_channels": optical_qr_channels,
            "06_file_format_placeholders": self.format_registry,
            "07_registry_summary": self.registry_summary(),
        }

        restricted_bytes = self.canonical_serialize(restricted_math_layer)
        restricted_digest = hashlib.sha256(restricted_bytes).hexdigest()

        master_state = {
            "artifact_id": "GENESIS_CANONICAL_ROOT",
            "nonce": nonce,
            "timestamp_utc": int(time.time()),
            "public_fork": public_patterns,
            "restricted_fork_commitment": restricted_digest,
        }

        canonical_bytes = self.canonical_serialize(master_state)
        canonical_root_hash = hashlib.sha256(canonical_bytes).hexdigest()

        psk_mac = hmac.new(
            self._psk,
            canonical_bytes + self._gatekeeper_pass.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()

        return {
            "master_state": master_state,
            "canonical_root_hash": canonical_root_hash,
            "display_alias": f"{canonical_root_hash[:3].upper()}...{canonical_root_hash[-2:].upper()}",
            "factor_2_psk_seal": psk_mac,
            "_restricted_payload_bytes": restricted_bytes,
        }

    def verify_and_project(
        self,
        sealed_record: Dict[str, Any],
        view_role: str,
        provided_passphrase: str = "",
    ) -> Dict[str, Any]:
        canonical_bytes = self.canonical_serialize(sealed_record["master_state"])
        recomputed_hash = hashlib.sha256(canonical_bytes).hexdigest()

        if not hmac.compare_digest(recomputed_hash, sealed_record["canonical_root_hash"]):
            raise ValueError("INTEGRITY FAILURE: Canonical root hash mismatch.")

        expected_mac = hmac.new(
            self._psk,
            canonical_bytes + self._gatekeeper_pass.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(expected_mac, sealed_record["factor_2_psk_seal"]):
            raise PermissionError("AUTH FAILURE: Out-of-band PSK seal invalid.")

        if view_role == "EXECUTIVE":
            return {
                "projection": "EXECUTIVE_VIEW",
                "status": "SEALED / VERIFIED",
                "display_alias": sealed_record["display_alias"],
                "nonce": sealed_record["master_state"]["nonce"],
                "registry": sealed_record["master_state"]["public_fork"]["07_registry_summary"],
            }
        elif view_role == "AUDIT_FULL":
            return {
                "projection": "AUDIT_FULL_VIEW",
                "canonical_root_hash": recomputed_hash,
                "public_patterns": sealed_record["master_state"]["public_fork"],
            }
        elif view_role == "RESTRICTED":
            if not hmac.compare_digest(provided_passphrase, self._gatekeeper_pass):
                raise PermissionError("LOCKED: Awaiting valid CEO Gatekeeper passphrase.")
            return {
                "projection": "RESTRICTED_VIEW",
                "canonical_root_hash": recomputed_hash,
                "restricted_layer": json.loads(
                    sealed_record["_restricted_payload_bytes"].decode("utf-8")
                ),
            }
        else:
            raise ValueError(f"Unknown projection role: {view_role}")


if __name__ == "__main__":
    engine = GenesisMasterSubstrate(
        pre_shared_key=b"tetrahedron-star-psk-test-key",
        gatekeeper_pass="GATEKEEPER_V4_TEST_OVERRIDE",
    )

    # Bind this script itself into code_scripts_wasm[.py] if present
    if os.path.isfile("genesis_substrate.py"):
        engine.bind_local_file("code_scripts_wasm", ".py", "genesis_substrate.py")

    # Example placeholder binding for .pdf
    engine.set_format_placeholder(
        "documents_text", ".pdf", sha256_digest="sample_pdf_digest_placeholder", status_label="PLACEHOLDER_READY"
    )

    qr_matrix = engine.build_qr_channel_matrix(
        red_restricted_pointer="LOCKED_FORK_02_RED_LANE",
        cyan_telemetry_stream="ARRAY_1_TO_4_384KHZ_32F",
        yellow_routing_nonce="NONCE_F6",
        black_root_anchor="GENESIS_CANONICAL_ROOT",
    )

    sealed = engine.seal_master_block(
        nonce="F6",
        binary_stream_hex="0101110000110000000001011110",
        acoustic_signature={
            "sensor_config": "4-Pt Tetrahedron (Star) PSK",
            "sample_rate_khz": 384.0,
            "bit_depth": "32-Bit Float",
            "resonant_heart_anchor": "Verified Bedrock Connect",
        },
        sphere_3d_grid={
            "grid_type": "HIGH-DENSITY 3D_SPHERE_GRID",
            "density": "MAX",
            "rgb_mapping": "0x01/0x02",
        },
        json_manifest={
            "manifest_id": "GENESIS_MASTER_BLOCK_v2.3",
            "assertion": "We do not try; we do.",
        },
        optical_qr_channels=qr_matrix,
        restricted_math_layer={
            "restricted_scope": "DEEP_BLOCK_RESTRICTED_VIEW",
            "mode": "CHESS_STRATEGIC",
        },
    )

    print("EXECUTIVE:", engine.verify_and_project(sealed, "EXECUTIVE"))
    try:
        engine.verify_and_project(sealed, "RESTRICTED", provided_passphrase="WRONG")
    except PermissionError as err:
        print("RESTRICTED_BLOCKED:", err)
    print(
        "RESTRICTED_UNLOCKED:",
        engine.verify_and_project(
            sealed, "RESTRICTED", provided_passphrase="GATEKEEPER_V4_TEST_OVERRIDE"
        ),
    )
