# Value destination matrix

The application has no value-bearing flow.

| Instrument | Payer/source | Locked state | Release/refund/forfeit destination | Terminal behavior | Canonical proof |
|---|---|---|---|---|---|
| Application GEN/escrow/bond/fee/reward/credit | N/A — every public write is non-payable | N/A | N/A | No application balance or accounting can be orphaned | contract metadata/AST and tests show no payable entrypoint or transfer |
| Protocol transaction fee | Transaction submitter, outside application accounting | Consensus protocol | Consumed/refunded by protocol policy | Recorded only from sanitized finalized receipt; never presented as contract funds | fee estimate and finalized allowlisted receipt fields |

