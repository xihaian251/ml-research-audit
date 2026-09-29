# TabM four-layer chain — artifact index

Companion to [`docs/end-to-end-tabm.md`](../../docs/end-to-end-tabm.md). This directory holds no
inputs and no copies of component source: it is an index of digests, so that anyone can check that
the artifacts a trace refers to are the artifacts they have.

All values are transcribed from the frozen Paper Doctor Phase 3 acceptance ledger
(`phase3/tabm/end_to_end_chain.json` in the
[paper-doctor repository](https://github.com/xihaian251/paper-doctor)). The chain id is
`chain-1-adult-four-layers`.

## Inputs the chain refers to

| Object | Identifier |
| --- | --- |
| Paper | TabM: Advancing Tabular Deep Learning with Parameter-Efficient Ensembling, ICLR 2025, arXiv:2410.24210 |
| Paper source entry point | `main.tex`, 88,033 B |
| Code repository | https://github.com/yandex-research/tabm |
| Code revision | `28e47ae301c92ec37787dde1ce923a0793f405b4` |
| Dataset | Adult, `ds_05c7465f`, train 32,561 rows / test 16,281 rows |
| Reported result | `tabm/adult-seed3/test-score` |
| Experiment run | `exp-cade5bdf7f3f4c4a9964dd0154598210#experiment.run.json` |

## Artifact digests

| Artifact | SHA256 |
| --- | --- |
| `main.tex` | `15663553d04fcbb8b3341df5c0d269c7703d4ba279be557fcd77ea4765ab0a62` |
| Adult `train.csv` | `ceb601e84db1fa01a57ae1e501e7137566297c1bc7e29b5b3605fe562d36ada1` |
| Adult `test.csv` | `23c3baa9db371c20612ec9696aaa95ce6d512d4171669beb97037e430e72a9bd` |
| Dataset Doctor fingerprint | `1f0dd1a5785fafde2627c9e47de94ebf436bbed551e11ac1200ad0804c63c9df` |
| Dataset Doctor `report.json` | `c1456a7bf602d4c3b4cda5f316a1fdb9e04ed15b7149ec2eb393046428c82f5f` |
| Experiment Doctor `experiment.lock.json` | `fb27c5eeada88d7a9d471e09464d7c60e444ea7743c66cd0433bdbc883e51cf8` |
| Experiment Doctor `report.json` | `2de48cc368f13fc3fbd0e9582adc659f712382067d45b142740a6e14ae35e170` |
| Result Doctor `findings.json` | `c56b62623b39ed9a4c311f8bcc6be6de457c1a0f8a4d34d3da99a4b71c7d2774` (12,392 B, `rd_version 0.1.0`) |
| Paper Doctor `pd_findings.json` | `08836ccfe17f3e2dc0750b30a2a3ae5e5022a53787cf93c2f085af932dff9aa0` (32 findings) |

Verify one locally without trusting this page:

```bash
sha256sum phase3/tabm/pd_findings.json
# 08836ccfe17f3e2dc0750b30a2a3ae5e5022a53787cf93c2f085af932dff9aa0
```

> Typo discipline matters here: if a digest on this page ever disagrees with the ledger, the ledger
> is authoritative and this file is the bug. Re-run `sha256sum` before drawing any conclusion.

## Statuses in the chain, per layer

| Layer | Rule | Status | Target |
| --- | --- | --- | --- |
| Paper | PD001 | PASS | C6, C7, C8 |
| Paper | PD002 | INCONCLUSIVE | C7 (seed universe declared `PARTIAL`) |
| Paper | PD003 | PASS | C6 |
| Paper | PD003 | **FAIL** | C8 — claim states 16281, addressed `(# Train, Adult)` cell states 26048, delta 9767 |
| Paper | PD007 | NOT_APPLICABLE | C6, C7, C8 |
| Result | RD002 | PASS | `aggregation:agg:adult-seed-mean` |
| Result | RD001, RD005 | NOT_APPLICABLE | `tabm/adult-seed3/test-score` |
| Experiment | ED002, ED003 | PASS | seed provenance, historical code provenance |
| Experiment | ED004, ED009, ED010 | INCONCLUSIVE | resolved config, termination cause, environment |
| Experiment | ED001 | NOT_APPLICABLE | single run — no family comparison to make |
| Dataset | DD009 | **FAIL CRITICAL** | conflicting labels on identical content, 26 groups across splits |
| Dataset | DD003 | WARNING MEDIUM | within-split exact duplicates in train and in test |
| Dataset | DD001, DD020 | PASS | dataset identified, partial provenance declared |
| Dataset | — | verdict `FORMAL_EVAL_INVALID` | 9 findings, 48,842 samples, 21 rules attempted, 6 `NOT_RUN` |

## Reading this index

Two `FAIL`s in one chain, at opposite ends: one at the paper layer about which column a declared link
addressed, one at the dataset layer about identical rows carrying different labels across a split
boundary. Neither says the paper is wrong. Both say something specific that a reader should not have to
guess, and the eight `UNKNOWN` entries in the ledger name what nobody, including the tools, could
establish.
