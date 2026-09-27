# Accessibility Acceptance Covenant — locked specification

Status: `SPEC_LOCKED`  
Track: `INTELLIGENT_CONTRACTS`  
Bound Forge record: `fc6377f4a1377bde78a8a487f4aeed18eb72f05a46cf2b7e8d23b403a83da438`

## Outcome and scope

`AccessibilityAcceptanceCovenant` is one standalone Intelligent Contract. It decides whether two exact, transaction-authorized evaluator reports cover one locked ICT release and accessibility-evaluation profile well enough to yield `ACCEPTED`, `CURE_REQUIRED`, `REJECTED`, or non-penalizing `UNVERIFIABLE`. Only stored `ACCEPTED` gives the configured buyer a one-time right to transition the case to `PROCUREMENT_ACCEPTED`.

The contract attests a bounded evaluation-record decision. It does not inspect the live product, prove universal WCAG/Section 508 or legal compliance, prove evaluator competence, make a procurement award, transfer value, or force an external consumer to honor its view.

There is no frontend, hosted app, escrow, bond, fee purse, reward, credit, refund, or application-level GEN transfer.

## Roles and authority

- Buyer: creates a unique case, locks the profile by activation, starts adjudication, retries only unverifiable work, finalizes an accepted case, or closes an expired unresolved case.
- Vendor: may submit exact-byte context and a bounded cure package. Its prose is untrusted and never independently changes verdict or eligibility.
- Primary evaluator: transaction-signs the primary report digest/locator envelope for the exact case/profile/release.
- Corroborating evaluator: a distinct address transaction-signs the corroborating report envelope.
- Validators: independently fetch the exact locator bytes, recompute SHA-256 digests, assess the same locked coverage/materiality question, compare meaning-bearing fields, and reject invalid normalized output.

The transaction signature authenticates evaluator authorship of the stored envelope. It does not prove the report is true or the evaluator competent.

## Canonical identifiers

All identifiers are non-empty printable ASCII, bounded in length, and cannot contain the `|` separator. ID sets are passed as `|`-delimited strings and normalized into sorted, unique canonical form. Expected sample, complete-process, criterion, finding, and cure-target sets are contract state; evidence prose cannot redefine them.

## State machine

```text
ABSENT -> DRAFT -> ACTIVE -> EVIDENCE_PENDING -> EVIDENCE_READY
EVIDENCE_READY -> ACCEPTED | CURE_REQUIRED | REJECTED | UNVERIFIABLE
UNVERIFIABLE -> EVIDENCE_READY (fresh bounded retry)
CURE_REQUIRED -> CURE_EVIDENCE_PENDING -> CURE_EVIDENCE_READY
CURE_EVIDENCE_READY -> ACCEPTED | CURE_REQUIRED | REJECTED | UNVERIFIABLE_CURE
UNVERIFIABLE_CURE -> CURE_EVIDENCE_READY (fresh cure attempt)
ACCEPTED -> PROCUREMENT_ACCEPTED
expired unresolved states -> CLOSED_UNRESOLVED
```

`PROCUREMENT_ACCEPTED`, `REJECTED`, and `CLOSED_UNRESOLVED` are terminal. `release_eligible` is true only in `PROCUREMENT_ACCEPTED`.

## Public writes

1. `create_case`: creates `DRAFT` with immutable role, product/release, profile, policy, expected-ID, and deadline fields.
2. `activate_case`: buyer locks the profile and enters `ACTIVE` before the evidence deadline.
3. `submit_vendor_context`: vendor stores an untrusted locator/digest envelope without changing eligibility.
4. `submit_evaluator_report`: the configured role address binds its exact report locator/digest/nonce/issued time; two distinct roles produce `EVIDENCE_READY`.
5. `adjudicate`: buyer runs exact-byte fetch plus comparative semantic consensus, then deterministic settlement checks before mutation.
6. `retry_unverifiable`: buyer opens one fresh attempt before retry deadline; it does not itself change eligibility.
7. `submit_cure`: vendor binds one cure package for the exact stored cure targets.
8. `submit_cure_addendum`: each configured evaluator binds an exact addendum for the same cure round and targets.
9. `readjudicate_cure`: buyer repeats exact-byte semantic consensus over the two addenda and exact target set.
10. `finalize_procurement_acceptance`: buyer-only, one-time `ACCEPTED -> PROCUREMENT_ACCEPTED`; no independent time gate because accepted semantic authority is already final for this case revision.
11. `close_expired`: buyer closes only unresolved states at or after their applicable final deadline.

All time-dependent writes read the transaction datetime and apply their own bound. Equality is late for submission/adjudication/retry/cure and is allowed for `close_expired`.

## Semantic result schema

The nondeterministic block returns exactly these consequence-bearing fields:

- `status`: `ACCEPTED`, `CURE_REQUIRED`, `REJECTED`, or `UNVERIFIABLE`;
- canonical `sample_ids`, `process_ids`, and `criterion_ids`;
- canonical `unresolved_ids` and `cure_target_ids`;
- canonical `authority_failures`.

The leader and each validator independently fetch and derive the result. Validators compare the normalized critical fields, not prose. Deterministic code then enforces:

- all expected evaluator roles are already bound exactly once;
- required sample/process/criterion sets match exactly;
- no extra, missing, or duplicate IDs;
- `ACCEPTED` has no unresolved/cure/authority failures;
- `CURE_REQUIRED` has non-empty unresolved IDs and the same exact cure-target set;
- `REJECTED` has non-empty unresolved IDs and no cure targets;
- `UNVERIFIABLE` is non-penalizing and cannot enable finalization;
- invalid normalized output reverts before state mutation.

## Evidence acquisition

The initial adjudication fetches three exact resources: the dated/locked policy source and both evaluator report locators. The cure adjudication fetches both evaluator addenda. HTTP failure, oversized content, decode failure, or digest mismatch normalizes to `UNVERIFIABLE`. Vendor content is delimited as untrusted context and cannot define roles, IDs, status, or consequence.

## Canonical views

- `get_case(case_id)` — role, identity, state, deadlines, attempt and terminal status.
- `get_profile(case_id)` — immutable profile/policy/expected-ID bindings.
- `get_evidence(case_id)` — stored non-secret locator/digest/nonce envelopes.
- `get_verdict(case_id)` — semantic verdict and exact normalized ID sets.
- `get_cure(case_id)` — cure round, exact targets, and addendum envelopes.
- `is_release_eligible(case_id)` — true only for `PROCUREMENT_ACCEPTED`.
- `get_case_count()` — number of unique cases.

## Acceptance criteria

- Exactly one recognized `gl.Contract` subclass and a concrete pinned runner hash.
- `genvm-lint check`, strict typecheck, schema emission, direct tests, metadata/AST checks, and aggregate `npm run check` pass.
- Every named Forge proof case and every safety-card negative/boundary case is represented by a test.
- Digest A with fetched bytes B never reaches a consequential verdict.
- Direct tests distinguish leader-only evidence from validator-consensus evidence.
- Studio-dev preflight proves network/schema/ABI compatibility before deployment.
- Deployment evidence, if authorized and available, distinguishes finalization, execution success, semantic result, and canonical consequence.

