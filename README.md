# Curriculum Drift Sentinel

An evidence-bound **pause gate** for a published syllabus. It does not build a course graph, grade learners, or issue a credential. Anyone may trigger an audit. If independently fetched current requirements materially differ from the hash-pinned baseline, the contract pauses the policy. An inconclusive fetch never marks a policy safe.

## Why GenLayer

A normal database can compare document hashes but cannot decide whether changed text changes a learner-facing requirement. GenLayer validators each fetch the baseline and live source, check full-body hashes/status/size, independently classify every named objective, and require exact equality of the complete decision report. The semantic classification affects the onchain ACTIVE/PAUSED gate.

```text
register baseline + live URL → permissionless audit → fetch both complete bodies
→ verify baseline SHA-256 → semantic per-objective comparison
→ exact validator report equality → ACTIVE / PAUSED / unchanged-on-INCONCLUSIVE
```

Each `(policy_id,audit_id)` report is immutable and bound to a monotonically increasing round. A repeated audit ID reverts. The live source hash is observed by validators, never supplied as a claimed result. The baseline must be a stable, content-addressed URL in production. The current URL should point to the publisher's live syllabus. A publisher controlling both sources can still misrepresent reality; this contract only judges the two observed documents.

## API

`register_policy(policy_id, objectives_csv, baseline_url, baseline_hash, live_url)`, `audit(policy_id, audit_id)`, `get_policy`, `get_audit`.

## Verify and deploy

```powershell
genvm-lint check contracts/CurriculumDriftSentinel.py --json
pytest tests/direct -q
genlayer network set studionet
genlayer deploy --contract contracts/CurriculumDriftSentinel.py
```

StudioNet is gasless. Inspect `genlayer receipt <hash>` for FINALIZED **and successful execution**. See `LIVE_PROOFS.md` once filled; no deployment is claimed by this README alone.

## Security boundaries

- Objective IDs: 1–5, immutable after registration. Audit IDs are unique per policy.
- HTTPS sources only; complete response size ≤8 KiB. HTTP failures, invalid UTF-8, or baseline mismatch yield INCONCLUSIVE.
- The LLM cannot choose final state directly: `MATERIAL`/`REMOVED` pauses, all `UNCHANGED` continues, any other vector is inconclusive.
- Validators reproduce source hashes, classification vector, decision, and report root exactly. Disagreement prevents a write.
- Fetched documents are untrusted prompt data. Semantic ambiguity remains possible; do not treat this as accreditation or a warranty.

## Demo fixtures

`examples/baseline.txt`, `examples/unchanged.txt`, and `examples/changed.txt` are synthetic syllabus excerpts. They illustrate PAUSE versus CONTINUE; they do not claim a real school changed its requirements.
