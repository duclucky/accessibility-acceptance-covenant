# Implementation plan

## Outcome and constraints

Build one contract-only GenLayer repository from the immutable Forge handoff. Preserve the bounded evaluation-record claim, exact evidence binding, non-penalizing unavailable path, no-value design, Studio-dev identity, and final Portal-submit prohibition.

## Ordered work

1. **Project and compatibility setup**
   - Create Python 3.12 `.venv`; pin `genvm-linter==0.11.1rc2`, `genlayer-test==0.30.0rc2`, and `genlayer-py==0.19.0rc2`.
   - Add aggregate `npm run check`, public-tree/metadata validators, and network/schema preflight scripts.
   - Expected checks: exact interpreter/package versions and runner header.

2. **RED: deterministic lifecycle boundary**
   - Add direct tests for creation, profile locking, role isolation, evidence envelopes, all temporal boundaries, retries, cure, close, and one-time finalization before contract source exists.
   - Confirm failures arise from the missing contract/behavior, not fixture or dependency errors.

3. **GREEN: structured state and deterministic writes/views**
   - Implement one `AccessibilityAcceptanceCovenant` class with `@allow_storage` dataclasses and `TreeMap` state.
   - Run lint before focused direct tests; keep mutation after checks.

4. **RED/GREEN: semantic adjudication**
   - Add named p01–p04, n01–n04, b01–b02, u01–u02, i01, and m01 tests plus validator-agreement/disagreement and commitment-mismatch cases.
   - Implement exact web-byte digest checks, independent comparative derivation, canonical output normalization, and deterministic settlement invariants.

5. **Cure adjudication and parser/preflight tooling**
   - Test and implement exact cure-target binding and two-addendum readjudication.
   - Add raw/normalized receipt parser tests, schema generation/comparison, ABI argument fixtures, fee-profile placeholder generation, and resumable deployment checkpoints.

6. **Fresh local verification**
   - Run `genvm-lint check`, strict typecheck, schema emission, full direct tests, script tests, public-tree checks, and `npm run check` in Python 3.12.
   - Record exact contract/test counts and sanitized local evidence; advance only on fresh success.

7. **Target-network preflight and resumable deployment**
   - Verify official network identity/status, target read-only code schema, ABI round trips, live fee estimate, and capability response format.
   - Deploy/write only through checkpoints; recover existing finalized hashes before retry; require FINALIZED plus FINISHED_WITH_RETURN and canonical state reads.
   - Sanitize all evidence through an explicit allowlist. If credentials, network, or authority are unavailable, record the blocker and exact resume condition without fabricating evidence.

8. **Repository and submission packet**
   - Audit Git root/status/staged/tracked allowlist and secret/history hygiene.
   - Prepare README, exact counts, links, validator inspection, consequence, reuse value, and honest limitations. Publish/push only if authorized and possible.
   - Stop at `SUBMISSION_READY`; never click final Portal Submit.

## Acceptance commands

Expected, not yet evidence:

```powershell
$env:PYTHONUTF8='1'
.\.venv\Scripts\python.exe -m pytest tests\direct tests\unit -v
.\.venv\Scripts\genvm-lint.exe check contracts\accessibility_acceptance_covenant.py --json
.\.venv\Scripts\genvm-lint.exe typecheck contracts\accessibility_acceptance_covenant.py --strict
npm run check
```

