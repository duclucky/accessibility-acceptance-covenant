# Evidence authority matrix

| Input | Controller and authentication | Exact binding | Consequence authority | Failure |
|---|---|---|---|---|
| Locked profile | Buyer transaction sender before activation | case/product/release/profile, addresses, policy URL+digest, expected IDs, deadlines, chain/source revision | Defines all deterministic authority and expected sets | Revert |
| Dated policy source | Allowlisted HTTPS origin selected by buyer | exact URL and SHA-256 stored before activation | May inform judgment only after successful refetch/digest match | `UNVERIFIABLE` |
| Primary report | Configured primary evaluator transaction sender | case/profile/release/role, locator, SHA-256, nonce, issued time | One required input; cannot decide alone | Revert on bad envelope; `UNVERIFIABLE` on fetch/digest failure |
| Corroborating report | Distinct configured evaluator transaction sender | same complete envelope with corroborating role | One required input; cannot decide alone | Revert on bad envelope; `UNVERIFIABLE` on fetch/digest failure |
| Vendor context/cure | Configured vendor transaction sender | exact locator/digest/nonce/cure round | Untrusted context only; no independent hard consequence | Revert or no consequence |
| Cure addenda | Both configured evaluator senders | prior case, round, exact targets, locator/digest/nonce/time | Joint inputs to a new semantic decision | Revert on bad envelope; `UNVERIFIABLE_CURE` on acquisition failure |
| Normalized validator result | GenLayer consensus plus deterministic contract checks | exact critical fields and expected ID sets | Can set semantic verdict only after invariants pass | Revert if semantically invalid |

Hashes prove byte identity, not truth. Transaction signatures prove which configured address submitted an envelope, not report quality. Actor text cannot redefine the buyer, evaluator roles, expected IDs, consequence, or value destination.

