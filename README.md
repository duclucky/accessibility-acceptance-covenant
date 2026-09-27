# Accessibility Acceptance Covenant

A reusable GenLayer Intelligent Contract for a bounded, release-specific accessibility evaluation covenant. Two distinct configured evaluator addresses bind exact report bytes. Validators refetch those bytes, compare a normalized semantic decision, and deterministic code rejects missing/extra IDs or invalid consequence mappings.

Only a stored `ACCEPTED` verdict lets the buyer execute the one-time transition to `PROCUREMENT_ACCEPTED`. Unavailable evidence, digest mismatch, or malformed semantic output cannot make a release eligible.

## What validators inspect

Validators inspect the exact policy and two evaluator-report resources whose HTTPS locators and SHA-256 digests are locked in contract state. They determine whether the locked samples, complete processes, criteria, and finding IDs are covered consistently enough for `ACCEPTED`, `CURE_REQUIRED`, `REJECTED`, or non-penalizing `UNVERIFIABLE`.

## Integration

Consumers read `get_case`, `get_profile`, `get_evidence`, `get_verdict`, `get_cure`, and `is_release_eligible`. The integration must enforce its own authorization and consequence; this primitive does not transfer value or make an external procurement award.

```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
npm run check
```

## Honest limits

This contract attests a bounded evaluation-record decision. It does not inspect a live product, prove universal WCAG/Section 508 or legal compliance, prove evaluator competence, or guarantee that an external buyer honors the result. Evaluator transaction identity authenticates who submitted an envelope, not whether its claims are true.

Studio Dev deployment and canonical lifecycle links are recorded only after finalized verification in `docs/evidence/studio-dev/`.

## Verified Studio Dev evidence

- Contract: [0x0aBF…DdF1](https://explorer-studio-dev.genlayer.com/address/0x0aBFc2798898783510091344C9B1820205a3DdF1)
- Deployment: [0x6bb8…0004](https://explorer-studio-dev.genlayer.com/transactions/0x6bb85988c37a550ae5aeeadbde2bbf2b19fbdc3025567965d9f8cade8cfe0004)
- Semantic adjudication: [0x24c7…75c5](https://explorer-studio-dev.genlayer.com/transactions/0x24c77c271cc050b52873a93003bb71d08c7d1ce24714fbe557d597b623d775c5)
- Final consequence: [0x5c40…5b70](https://explorer-studio-dev.genlayer.com/transactions/0x5c4061c16fba8335caa6a2f14ccec97fe076510c82b9993a0b64b1edec0e5b70)

The canonical demo case finalized as `PROCUREMENT_ACCEPTED`; `is_release_eligible` returned `true`. The evidence fixture is synthetic and demonstrates the primitive—it is not adoption proof.
