from __future__ import annotations
import copy, hashlib, json, time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

SCHEMA_VERSION = 4
REPRO_TS = 1795478400
ALLOWED_DISPOSITIONS = {"PENDING_HUMAN_RUN", "ACCEPTED_FOR_TEST_COPY", "REJECTED", "ESCALATED"}
ALLOWED_LIFECYCLE_TRANSITIONS = {("STAGED", "COMMITTED_PENDING_FINALIZE"), ("STAGED", "QUARANTINED"), ("COMMITTED_PENDING_FINALIZE", "FINALIZED"), ("COMMITTED_PENDING_FINALIZE", "RECOVERY_REQUIRED"), ("FINALIZED", "QUARANTINED"), ("QUARANTINED", "RECOVERY_REQUIRED")}

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")

def sha256_of(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def reconcile_abc(input_a: Dict[str, Any], input_b_items: List[Dict[str, Any]]) -> Dict[str, Any]:
    base_facts = {k: v for k, v in input_a.items() if k != "claims"}
    a_claims: List[Any] = list(input_a.get("claims") or [])
    resolved_facts: Dict[str, Any] = dict(base_facts)
    unresolved: List[Dict[str, Any]] = []
    a_seen: Dict[str, Tuple[int, Any]] = {}
    for i, claim in enumerate(a_claims):
        d = sha256_of(claim)
        if not isinstance(claim, dict) or "key" not in claim or "value" not in claim:
            unresolved.append({"source": "A", "source_index": i, "reason": "CORRUPTED_OR_MISSING_FIELDS", "digest": d, "raw_preserved": claim})
            continue
        k, v = claim["key"], claim["value"]
        conflict = None
        if k in a_seen and a_seen[k][1] != v:
            conflict = ("CONTRADICTS_PRIOR_A_CLAIM", a_seen[k][0], a_seen[k][1])
        elif k in base_facts and base_facts[k] != v:
            conflict = ("CONTRADICTS_A_BASE_FACT", None, base_facts[k])
        if conflict:
            kind, prior_idx, prior_val = conflict
            unresolved.append({"source": "A", "source_index": i, "reason": "INTERNAL_CONTRADICTION_IN_A", "key": k, "conflict_kind": kind, "prior_index": prior_idx, "prior_value": prior_val, "conflicting_value_in_a": v, "digest": d, "raw_preserved": claim})
        else:
            a_seen[k] = (i, v)
            resolved_facts.setdefault(k, v)
    seen_digests = set()
    for idx, item in enumerate(input_b_items):
        item_digest = sha256_of(item)
        if item_digest in seen_digests:
            unresolved.append({"source": "B", "source_index": idx, "reason": "DUPLICATE_INPUT", "digest": item_digest, "raw_preserved": item})
            continue
        seen_digests.add(item_digest)
        if not isinstance(item, dict) or item.get("corrupted") is True or "key" not in item or "value" not in item:
            unresolved.append({"source": "B", "source_index": idx, "reason": "CORRUPTED_OR_MISSING_FIELDS", "digest": item_digest, "raw_preserved": item})
            continue
        k, v = item["key"], item["value"]
        if k in resolved_facts and resolved_facts[k] != v:
            unresolved.append({"source": "B", "source_index": idx, "reason": "CONTRADICTION_WITH_A", "key": k, "value_in_a": resolved_facts[k], "conflicting_value_in_b": v, "digest": item_digest, "raw_preserved": item})
        else:
            resolved_facts[k] = v
    status = "PARTIAL_WITH_OPEN_UNRESOLVED" if unresolved else "RECONCILED_CLOSED"
    return {"equation": "A + B = C (OPEN_CONTAINER_PRESERVED)", "a_digest": sha256_of(input_a), "b_digest": sha256_of(input_b_items), "b_total_count": len(input_b_items), "c_state": {"closure_status": status, "resolved_facts": resolved_facts, "unresolved_open_container": unresolved, "unresolved_count": len(unresolved)}, "c_digest": sha256_of({"resolved": resolved_facts, "unresolved": unresolved})}

def verify_unresolved_preservation(input_a: Dict[str, Any], input_b_items: List[Dict[str, Any]], unresolved: List[Dict[str, Any]]) -> List[str]:
    errors: List[str] = []
    a_claims = list(input_a.get("claims") or [])
    for r in unresolved:
        src, idx = r.get("source"), r.get("source_index")
        container = a_claims if src == "A" else input_b_items if src == "B" else None
        if container is None:
            errors.append(f"unknown source {src!r}")
            continue
        if not isinstance(idx, int) or not (0 <= idx < len(container)):
            errors.append(f"bad source_index {idx!r}")
            continue
        if container[idx] != r.get("raw_preserved"):
            errors.append(f"raw_preserved mismatch at {src}[{idx}]")
        if sha256_of(r.get("raw_preserved")) != r.get("digest"):
            errors.append(f"digest mismatch at {src}[{idx}]")
    return errors

def record_collaboration_event(*, artifact_id: str, source_hash: str, participant_alias: str, task: str, returned_summary: str, unresolved_items: List[str], human_disposition: str, state_before: Optional[str], state_after: str, lifecycle_state: str, seq: int, prev_event: Optional[Dict[str, Any]] = None, now_utc: Optional[int] = None) -> Dict[str, Any]:
    if human_disposition not in ALLOWED_DISPOSITIONS: raise ValueError(f"bad disp {human_disposition!r}")
    if prev_event is None:
        if seq != 0 or state_before is not None: raise ValueError("bad first event")
        prev_hash = None
    else:
        if prev_event.get("seq") != seq - 1 or prev_event.get("artifact_id") != artifact_id or state_before != prev_event.get("state_after"): raise ValueError("bad link")
        if (prev_event.get("lifecycle_state"), lifecycle_state) not in ALLOWED_LIFECYCLE_TRANSITIONS: raise ValueError("bad transition")
        prev_hash = prev_event.get("event_sha256")
    ev = {"schema_version": SCHEMA_VERSION, "seq": seq, "prev_event_sha256": prev_hash, "timestamp_utc": int(now_utc if now_utc is not None else time.time()), "artifact_id": artifact_id, "source_hash": source_hash, "participant": participant_alias, "task": task, "returned_summary": returned_summary, "unresolved_items": list(unresolved_items), "human_disposition": human_disposition, "state_before": state_before, "state_after": state_after, "lifecycle_state": lifecycle_state}
    ev["event_sha256"] = sha256_of(ev)
    return ev

def verify_chain(events: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
    errs: List[str] = []
    for i, ev in enumerate(events):
        body = {k: v for k, v in ev.items() if k != "event_sha256"}
        if ev.get("event_sha256") != sha256_of(body): errs.append(f"[{i}] hash")
        if ev.get("seq") != i: errs.append(f"[{i}] seq")
        if ev.get("human_disposition") not in ALLOWED_DISPOSITIONS: errs.append(f"[{i}] disp")
        if i == 0:
            if ev.get("prev_event_sha256") is not None or ev.get("state_before") is not None: errs.append(f"[{i}] gen")
        else:
            p = events[i - 1]
            if ev.get("prev_event_sha256") != p.get("event_sha256") or ev.get("state_before") != p.get("state_after") or ev.get("artifact_id") != p.get("artifact_id"): errs.append(f"[{i}] link")
            if (p.get("lifecycle_state"), ev.get("lifecycle_state")) not in ALLOWED_LIFECYCLE_TRANSITIONS: errs.append(f"[{i}] tr")
    return (len(errs) == 0), errs

def main() -> int:
    a = {
        "parcel_id": "DL-001",
        "declared_status": "DELIVERED",
        "weight_kg": 12.5,
        "claims": [
            {"key": "declared_status", "value": "DELIVERED"},
            {"key": "declared_status", "value": "IN_TRANSIT"},
        ],
    }
    b = [
        {"key": "receiver_confirmed", "value": True},
        {"key": "declared_status", "value": "RETURNED_TO_SENDER"},
        {"key": "receiver_confirmed", "value": True},
        {"key": "missing_value_field"},
        {"key": "weight_kg", "value": 99.9, "corrupted": True},
    ]
    res = reconcile_abc(a, b)
    unres = res["c_state"]["unresolved_open_container"]
    perrs = verify_unresolved_preservation(a, b, unres)
    cdig = res["c_digest"]
    art = "GENESIS_SUBSTRATE_ADC02"
    sh = "adcdae38ee4590e4a0d3d968e87e09d2bf205a434808caead3e6b66a576ece02"
    e0 = record_collaboration_event(
        artifact_id=art,
        source_hash=sh,
        participant_alias="ChatGPT_Reviewer",
        task="v4 A+B=C audit",
        returned_summary="Open container + chain",
        unresolved_items=["T01-T11 pending"],
        human_disposition="ACCEPTED_FOR_TEST_COPY",
        state_before=None,
        state_after=cdig,
        lifecycle_state="STAGED",
        seq=0,
        now_utc=REPRO_TS,
    )
    e1 = record_collaboration_event(
        artifact_id=art,
        source_hash=sh,
        participant_alias="Gemini_Reviewer",
        task="v4 verify",
        returned_summary="Chain verified",
        unresolved_items=["T09/T11 pending"],
        human_disposition="PENDING_HUMAN_RUN",
        state_before=cdig,
        state_after=cdig,
        lifecycle_state="COMMITTED_PENDING_FINALIZE",
        seq=1,
        prev_event=e0,
        now_utc=REPRO_TS,
    )
    e2 = record_collaboration_event(
        artifact_id=art,
        source_hash=sh,
        participant_alias="Human_Operator",
        task="v4 finalize",
        returned_summary="Ready for isolated test",
        unresolved_items=["head anchor pending"],
        human_disposition="ACCEPTED_FOR_TEST_COPY",
        state_before=cdig,
        state_after=cdig,
        lifecycle_state="FINALIZED",
        seq=2,
        prev_event=e1,
        now_utc=REPRO_TS,
    )
    chain = [e0, e1, e2]
    ok, errs = verify_chain(chain)
    neg = []
    m1 = copy.deepcopy(chain); m1[1]["returned_summary"] = "TAMPERED"
    neg.append(not verify_chain(m1)[0])
    m2 = copy.deepcopy(chain); m2[1]["returned_summary"] = "TAMPERED_REHASHED"
    m2[1]["event_sha256"] = sha256_of({k: v for k, v in m2[1].items() if k != "event_sha256"})
    neg.append(not verify_chain(m2)[0])
    m3 = copy.deepcopy(chain); del m3[1]
    neg.append(not verify_chain(m3)[0])
    m4 = copy.deepcopy(chain); m4[1], m4[2] = m4[2], m4[1]
    neg.append(not verify_chain(m4)[0])
    try:
        record_collaboration_event(
            artifact_id=art,
            source_hash=sh,
            participant_alias="Rogue",
            task="skip",
            returned_summary="skip",
            unresolved_items=[],
            human_disposition="ACCEPTED_FOR_TEST_COPY",
            state_before=cdig,
            state_after=cdig,
            lifecycle_state="FINALIZED",
            seq=1,
            prev_event=e0,
            now_utc=REPRO_TS,
        )
        neg.append(False)
    except ValueError:
        neg.append(True)
    try:
        record_collaboration_event(
            artifact_id=art,
            source_hash=sh,
            participant_alias="Rogue",
            task="disp",
            returned_summary="disp",
            unresolved_items=[],
            human_disposition="BOGUS",
            state_before=None,
            state_after=cdig,
            lifecycle_state="STAGED",
            seq=0,
            now_utc=REPRO_TS,
        )
        neg.append(False)
    except ValueError:
        neg.append(True)
    proof = {
        "schema_version": SCHEMA_VERSION,
        "repro_ts": REPRO_TS,
        "abc_result": res,
        "preservation_errors": perrs,
        "chain_valid": ok,
        "chain_errors": errs,
        "collaboration_chain": chain,
        "negative_tests_all_expected": all(neg),
    }
    Path("GENESIS/test_copy/abc_audit_v4_proof.json").write_text(
        json.dumps(proof, indent=2, sort_keys=True), encoding="utf-8"
    )
    print("CLOSURE:", res["c_state"]["closure_status"], "UNRESOLVED:", res["c_state"]["unresolved_count"])
    print("PRESERVATION_OK:", len(perrs) == 0, "CHAIN_OK:", ok, "NEG_OK:", all(neg))
    print("PROOF_SHA256:", sha256_of(proof))
    return 0 if (not perrs and ok and all(neg)) else 1

if __name__ == "__main__":
    raise SystemExit(main())
