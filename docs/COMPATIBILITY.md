# Locked compatibility matrix

Observed and frozen on 2026-09-27 UTC. A changed row requires a new compatibility check and deployment fingerprint.

| Component | Locked value | Authority/proof | Build check |
|---|---|---|---|
| Target | Studio development preview | official Networks and Consensus v0.6 migration docs | chain/RPC preflight |
| GenLayer RPC | `https://studio-dev.genlayer.com/api` | official Networks page | read-only RPC identity probe |
| Chain ID | `61997` | official Networks page | SDK/CLI network info and RPC result |
| Explorer | `https://explorer-studio-dev.genlayer.com` | official Networks page | verify generated address/tx routes |
| GenVM runner | `py-genlayer:5jycge4q8k23462jtb0b9fyey1s9qz928sz2nbrd9mg4sxqg2qng` | current `genvm-linter` runner inventory; isolated v0.3 API probe | first-line check, lint, direct probe, target schema, bounded network smoke |
| Contract API | v0.3: `import genlayer as gl`; `gl.contract.Contract` | current official `genlayer-test` suite and installed RC family | isolated import/lint/direct/schema probe |
| Python | 3.12.13 | Forge Windows policy and local `py` inventory | project `.venv` version |
| `genvm-linter` | `0.11.1rc2` | installed package and PyPI prerelease inventory | `genvm-lint --version` |
| `genlayer-test` | `0.30.0rc2` | installed package and PyPI prerelease inventory | package metadata and direct tests |
| `genlayer-py` | `0.19.0rc2` | Consensus v0.6 family plus installed/PyPI observation | package metadata and schema/RPC probe |
| GenLayer CLI | `0.40.0-rc.3` | Consensus v0.6 family plus installed global package | `genlayer --version`; requires `studio-dev` preset |
| Contract schema | generated from final source | local linter plus target `gen_getContractSchemaForCode` equivalent | canonical JSON comparison |
| Receipt parser | project parser accepts raw and normalized v0.6 shapes | official finality requirements | parser unit tests |

Studio-dev is ephemeral and may reset. Stable `studionet` (61999) must never be relabeled or mixed with this evidence set.

## Resolved documentation drift

The public First Contract page observed on 2026-09-27 still showed the older
`1jb...` runner and v0.2 import/class form. That combination cannot load through
the locked `genlayer-test==0.30.0rc2` direct-mode loader because the old SDK does
not expose the current calldata module. The replacement row above was admitted
only after an isolated v0.3 probe passed current lint, direct execution, and the
Studio-dev read-only code-schema endpoint. Production source remains blocked
until the same probe completes a bounded finalized Studio-dev deployment.
