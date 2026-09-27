# Write-method safety cards

Every method is non-payable and has no application accounting effect.

| Method | Caller | Allowed state | Time rule | Duplicate/idempotency | Mutation and required negatives |
|---|---|---|---|---|---|
| `create_case` | any; caller becomes buyer | absent | N/A; supplied deadlines strictly future/ordered | duplicate ID reverts | creates DRAFT; test malformed IDs, role collision, deadline order |
| `activate_case` | buyer | DRAFT | `now < evidence_deadline`; equality late | second call reverts | locks ACTIVE; test wrong caller/state and -1/exact/+1 |
| `submit_vendor_context` | vendor | ACTIVE/EVIDENCE_PENDING/CURE_REQUIRED | before applicable deadline; equality late | nonce/digest replay reverts | stores untrusted envelope only; test no verdict/eligibility change |
| `submit_evaluator_report` | matching configured evaluator | ACTIVE/EVIDENCE_PENDING | created ≤ issued ≤ now and `now < evidence_deadline` | role and nonce once | second role makes EVIDENCE_READY; test wrong/same key, replay, stale/future, bindings, boundary |
| `adjudicate` | buyer | EVIDENCE_READY | `now < adjudication_deadline`; equality late | fresh attempt nonce | mutation only after exact fetch, consensus, invariants; test injection/digest/unavailable/invalid output |
| `retry_unverifiable` | buyer | UNVERIFIABLE | `now < retry_deadline`; equality late | fresh attempt nonce | returns to EVIDENCE_READY without eligibility change; test wrong caller/state/late/duplicate |
| `submit_cure` | vendor | CURE_REQUIRED | `now < cure_deadline`; equality late | one nonce per round | exact cure target set only; test extra/missing/duplicate |
| `submit_cure_addendum` | matching evaluator | CURE_EVIDENCE_PENDING | created ≤ issued ≤ now and `now < cure_deadline` | role/round/nonce once | two roles make CURE_EVIDENCE_READY; test bindings/replay/time |
| `readjudicate_cure` | buyer | CURE_EVIDENCE_READY/UNVERIFIABLE_CURE | `now < cure_deadline`; equality late | fresh cure attempt | mutation only after exact target coverage and invariants |
| `finalize_procurement_acceptance` | buyer | ACCEPTED | N/A: stored accepted verdict already supplies semantic authority | one-time; duplicate reverts | PROCUREMENT_ACCEPTED and eligible true; test every other state/wrong caller |
| `close_expired` | buyer | unresolved non-terminal states | `now >=` applicable deadline | one-time | CLOSED_UNRESOLVED, eligible false; test -1/exact/+1, wrong caller/state |

Rejected calls must leave canonical state and the absent application accounting unchanged.

