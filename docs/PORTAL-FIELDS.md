# Portal fields — publication-blocked draft

These fields are complete except for the public repository and CI URLs. Do not paste them into the Portal until those two links are real and reverified.

## Category

Intelligent Contracts

## Name

Accessibility Acceptance Covenant

## Repository

`PENDING_EXPLICIT_PUBLICATION_AUTHORIZATION`

## Description

Accessibility Acceptance Covenant is a reusable, contract-only GenLayer primitive for a release-specific accessibility evaluation record. A buyer locks the release, policy digest, coverage IDs, two distinct evaluator addresses, and deadlines. Each evaluator transaction-binds exact report bytes. Validators independently refetch the policy and reports, compare the seven consequence-bearing semantic fields, and deterministic code rejects missing, extra, duplicate, or inconsistent IDs before state mutation. Outcomes are ACCEPTED, CURE_REQUIRED, REJECTED, or non-penalizing UNVERIFIABLE. Only ACCEPTED allows the buyer's one-time transition to PROCUREMENT_ACCEPTED; the demo finalized that transition and the canonical eligibility view returned true. The contract does not transfer value, inspect a live product, prove universal/legal compliance, evaluator competence, procurement adoption, or external enforcement.

## Exact counts

- Contracts: 1
- Public contract methods: 18 (11 write, 7 view)
- Tests: 11

## Links

- Primary contract: https://explorer-studio-dev.genlayer.com/address/0x0aBFc2798898783510091344C9B1820205a3DdF1
- Deployment: https://explorer-studio-dev.genlayer.com/transactions/0x6bb85988c37a550ae5aeeadbde2bbf2b19fbdc3025567965d9f8cade8cfe0004
- Semantic adjudication: https://explorer-studio-dev.genlayer.com/transactions/0x24c77c271cc050b52873a93003bb71d08c7d1ce24714fbe557d597b623d775c5
- Final consequence: https://explorer-studio-dev.genlayer.com/transactions/0x5c4061c16fba8335caa6a2f14ccec97fe076510c82b9993a0b64b1edec0e5b70
- Repository: `PENDING_EXPLICIT_PUBLICATION_AUTHORIZATION`
- CI: `PENDING_REPOSITORY_PUBLICATION_AND_SUCCESSFUL_RUN`

## Validator inspection and consequence

Validators fetch the exact locked WCAG policy bytes and both evaluator-report byte strings, recompute each SHA-256 digest, and independently derive the same normalized status and coverage/finding sets. Deterministic invariants run before mutation. In the canonical synthetic lifecycle, consensus finalized `ACCEPTED`; the buyer then finalized `PROCUREMENT_ACCEPTED`, and `is_release_eligible` returned `true`.

## Reuse value

Procurement systems can reuse the primitive as a bounded eligibility signal while retaining their own authorization and external consequence enforcement. The same state machine supports a non-penalizing retry and exact-target cure/addendum round.

## Honest limitations

The demo reports are synthetic exact-byte fixtures. Hashes prove byte identity, evaluator transactions prove which configured address submitted an envelope, and validator consensus proves the bounded semantic decision—not report truth, evaluator competence, live-product accessibility, legal compliance, adoption, or an external award.
