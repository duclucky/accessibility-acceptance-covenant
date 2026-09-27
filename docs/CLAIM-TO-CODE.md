# Claim-to-code and evidence matrix

| ID | Bounded public claim | State/code target | Canonical view | Required tests | Required evidence |
|---|---|---|---|---|---|
| C1 | One immutable release-specific acceptance profile | `create_case`, `activate_case`, `CaseRecord` | `get_profile`, `get_case` | identity isolation, duplicate ID, role collision, deadline ordering, locked configuration | schema plus direct lifecycle result |
| C2 | Two distinct evaluator transaction identities bind exact report bytes | `submit_evaluator_report`, stored locator/digest/nonce/time/role | `get_evidence` | wrong sender, same key, replay, stale/future time, wrong case/profile/release, digest mismatch | direct tests and finalized report-submission reads |
| C3 | Validators reconcile semantic accessibility-evaluation coverage | `adjudicate`, independent fetch/prompt/critical-field comparison | `get_verdict` | p01–p04, n01–n04, unavailable, injection, validator disagreement | consensus transaction plus normalized stored verdict |
| C4 | Deterministic settlement invariants guard every hard state change | post-consensus `_validate_result` before assignment | `get_verdict`, `get_case` | missing/extra/duplicate IDs, invalid enum, accepted-with-findings, mutation unchanged | failing direct cases plus finalized canonical reads |
| C5 | Accepted verdict alone enables one-time procurement acceptance | `finalize_procurement_acceptance` | `is_release_eligible`, `get_case` | wrong caller/state, duplicate, CURE/REJECTED/UNVERIFIABLE blocked | finalized successful transaction and post-state read |
| C6 | Retry, cure, expiry, and closure are bounded | retry/cure/addendum/readjudication/close methods | all case/verdict/cure views | each temporal write at boundary -1/exact/+1 with stale phase, duplicate and wrong caller | direct suite and sanitized lifecycle trace |
| C7 | The repository is a reusable contract-only primitive | one contract, tests, scripts, docs; no frontend | emitted schema | public-tree allowlist, exact count audit, aggregate check | repository URL/CI only after publication |

Claims outside this table are not permitted in README or Portal text. In particular, do not claim live-product testing, universal compliance, legal advice, evaluator competence, procurement award, adoption, savings, or unavoidable external enforcement.

