# End-to-end: one reported number traced through all four layers

This is the stack's one completed four-layer acceptance run. It is published here because it is the
evidence that the four tools are one ecosystem rather than four unrelated CLIs — and equally because
of what it could not close.

Everything in this page comes from the frozen Paper Doctor Phase 3 acceptance artifacts
(`phase3/tabm/` in the [paper-doctor repository](https://github.com/xihaian251/paper-doctor)), plus
the corresponding Result Doctor, Experiment Doctor and Dataset Doctor reports in that same
directory. Versions used: `paper-doctor 0.1.0`, `result-doctor 0.1.0`, `experiment-doctor 1.0.0`,
`dataset-doctor-audit 0.1.2`.

## What was audited

**TabM: Advancing Tabular Deep Learning with Parameter-Efficient Ensembling**, ICLR 2025,
arXiv:2410.24210. Code: [`yandex-research/tabm`](https://github.com/yandex-research/tabm) at commit
`28e47ae301c92ec37787dde1ce923a0793f405b4`. Paper source entry point `main.tex`, 88,033 bytes,
SHA256 `15663553d04fcbb8b3341df5c0d269c7703d4ba279be557fcd77ea4765ab0a62`.

No component code was modified for this run, no adapter was written specifically for TabM, and no
rule was added. Every layer was invoked through its public CLI on artifacts the project already
shipped.

## The chain, in one table

| Layer | Object traced | Command shape | Result |
| --- | --- | --- | --- |
| Paper | claim **C8** — the literal `$16\,281$` at `tables/app-rtdl-datasets.tex:8` | `paper-doctor audit phase3/tabm` | `PD001 PASS`, **`PD003 FAIL`**, `PD007 NOT_APPLICABLE` |
| Paper | claim **C6** — the literal `$26\,048$` on the same row | same | `PD001 PASS`, `PD003 PASS`, `PD007 NOT_APPLICABLE` |
| Paper | claim **C7** — `main.tex:981`, "…under 15 different random seeds." | same | `PD001 PASS`, `PD002 INCONCLUSIVE`, `PD007 NOT_APPLICABLE` |
| Result | reported result `tabm/adult-seed3/test-score`; aggregation `agg:adult-seed-mean` | `result-doctor audit phase3/tabm/result-doctor.yml` | `RD002 PASS` on the aggregation; `RD001 NOT_APPLICABLE`, `RD005 NOT_APPLICABLE` on the cell. 14 findings total: 1 `PASS`, 6 `INCONCLUSIVE`, 6 `NOT_APPLICABLE`, 1 `NOT_RUN` |
| Experiment | run `exp-cade5bdf7f3f4c4a9964dd0154598210` (seed 3) | `experiment-doctor init` / `audit` on a fresh clone at the pinned commit | `ED002 PASS`, `ED003 PASS`; `ED004`, `ED009`, `ED010` `INCONCLUSIVE`; `ED001 NOT_APPLICABLE` |
| Dataset | dataset `ds_05c7465f` — Adult, train 32,561 / test 16,281 rows | `dataset-doctor-audit audit <prepared adult directory>` | verdict **`FORMAL_EVAL_INVALID`**, 9 findings, `DD009` `CRITICAL FAIL` |

The joins between these rows are declarations, not computations. That is what makes them traceable —
and it is where the interesting failures happen.

## The two `FAIL` findings, stated exactly

### 1. `PD003` on C8 — a number the audit could not address

Claim C8 states `16281`. The evidence link declared for it resolves to
`(column=# Train, row=Adult)` of `table:4`, whose printed cell states `26048`. The finding:

```text
PD003  FAIL  C8
  reason: the claim states 16281 but the printed cell at (column=# Train, row=Adult,
          block=b1 [midrule at tables/app-rtdl-datasets.tex:4], unit=reported_cell)
          of table:4 states 26048; both declare 'number of datasets, # Train'
  measurements: claim_value 16281, cell_value 26048, delta 9767.0
```

The source row is `Adult & $26\,048$ & $6\,513$ & $16\,281$ & …`. The paper is internally consistent:
26,048 and 6,513 and 16,281 are different columns of one row, and PD003 compares a claim only to the
cell the link addresses — it never scans the row for a number that matches.

So what does this `FAIL` mean? It means one declared relation disagrees with the evidence: the claim's
literal was linked to the `# Train` column. Either the link was misdeclared, or the claim addresses a
column whose semantics differ from what the link says. **The tool does not decide which**, and neither
does this page. What it does is refuse to let the mismatch pass silently, and name the exact
declaration to go and re-read.

This is not a statement that the TabM paper is wrong. A `FAIL` is a question for an author, and here
the question was answerable locally by re-declaring the link. It was left as `FAIL` because changing a
declared link to make a finding disappear is exactly the kind of quiet repair this stack exists to
prevent.

### 2. `DD009` at the dataset layer — `CRITICAL`, and the paper inherits it

Dataset Doctor on the prepared Adult copy — verdict `FORMAL_EVAL_INVALID`, 2 blocking findings out of
9, 48,842 samples hashed, 21 rules attempted (6 `NOT_RUN`):

```text
DD009 FAIL CRITICAL  Conflicting labels on identical content (26 group(s), across splits)
DD009 FAIL HIGH      Conflicting labels on identical content (1 group(s) inside one split)
DD003 WARNING MEDIUM Within-split exact duplicates in 'train'
DD003 WARNING MEDIUM Within-split exact duplicates in 'test'
DD013 WARNING HIGH   Label distribution shift: train vs test
DD014 WARNING MEDIUM Unseen categories in test
```

Twenty-six groups of identical feature rows carry different labels across the train/test boundary.
Dataset Doctor's verdict is about the *evaluation boundary*, not about the dataset's quality: formal
evaluation on these splits cannot be trusted, because an identical input appears on both sides with
different targets.

This finding sits at the bottom of the chain that ends in a published table cell. It is reported by
the tool, not inferred by us, and it concerns a third-party dataset preparation that the TabM paper
consumes. Whether the paper's authors used this exact preparation is itself one of the `UNKNOWN`s
below.

## Where the chain stops being evidenced

Eight `UNKNOWN` states were recorded in the acceptance ledger. The four that matter most for reading
this case study honestly:

| Gap | Layer | Why it stays open |
| --- | --- | --- |
| No run-side bundle exists for the published runs: no effective configuration, no termination cause, no runtime environment in any shipped artifact | Experiment | `ED004`, `ED009`, `ED010` are `INCONCLUSIVE`. The repository ships `paper/environment.yaml`, which states a requirement, not a fact about what executed |
| The paper's `# Train` column prints 26,048 while Dataset Doctor measures the official files as train 32,561 / test 16,281; 26,048 + 6,513 = 32,561, i.e. the printed figure is a hold-out of the official training file | Dataset ↔ Paper | Dataset Doctor's numbers describe the files it read. Nothing on file states which preparation the paper used |
| The seed universe for the reported 15-seed mean is declared `PARTIAL` | Result ↔ Paper | `PD002` stays `INCONCLUSIVE`: an unlisted universe cannot be passed |
| The published per-dataset accuracies live in longtables whose source gives no reference name for the printed cell | Paper | No claim can address that mean, so the value `0.8575` was never turned into a claim at all |

Two further searches came back empty and are recorded as `SEARCHED / NOT OBSERVED`: no TabM table both
names its float in a sentence and prints a value the shipped artifacts reconstruct, and no run-side
artifact inside `exp/` records the environment a published run executed under.

## What this run does and does not establish

**It establishes:** four independently released tools can be pointed at one real third-party paper,
in one dependency graph, and produce findings that name their own evidence; the joins were written
down by a person and stayed auditable; two genuine inconsistencies and eight gaps survived the whole
pipeline instead of being smoothed into a score.

**It does not establish:** that the TabM results are correct or incorrect; that the stack reproduces
TabM's numbers (no TabM training was executed — the Experiment Doctor capture recorded provenance
around a configuration, not a completed run with a metric); that any author made an error; that this
counts as a real human first-use test of the tools (it does not — see `STACK_STATUS.md` §3); or that
one acceptance run on one paper is a validation programme.

The single most useful number on this page is `8`. A tool that reports eight unresolved gaps on a
major published paper, at a layer where the paper's own authors did not record the evidence, is doing
something. A tool that reported `PASS` there would be lying.

## Reproducing the trace

```bash
# 1. Paper source, pinned by the acceptance input fetcher
git clone https://github.com/xihaian251/paper-doctor.git && cd paper-doctor
python scripts/fetch_acceptance_inputs.py tabm

# 2. Result Doctor over the TabM bundle
pip install result-doctor
result-doctor audit phase3/tabm/result-doctor.yml --json > /tmp/rd-findings.json

# 3. Paper Doctor over the claims, with the RD findings pinned by digest in the manifest
pip install paper-doctor
paper-doctor audit phase3/tabm --json /tmp/pd-findings.json
# expected findings digest: 08836ccfe17f3e2dc0750b30a2a3ae5e5022a53787cf93c2f085af932dff9aa0
# expected counts: 32 findings - 10 PASS, 2 FAIL, 5 INCONCLUSIVE, 14 NOT_APPLICABLE, 1 NOT_RUN

# 4. Experiment Doctor: capture the declared surface, then audit it
pip install experiment-doctor
git clone https://github.com/yandex-research/tabm.git
git -C tabm checkout 28e47ae301c92ec37787dde1ce923a0793f405b4
experiment-doctor init tabm/paper \
  --command 'python bin/model.py exp/tabm/adult/0-evaluation/3.toml --force' \
  --seed 3 --config exp/tabm/adult/0-evaluation/3.toml \
  --dataset <your official adult copies>
experiment-doctor audit tabm/paper --adapter captured -o /tmp/ed-report

# 5. Dataset Doctor on your own copy of the Adult preparation
pip install dataset-doctor-audit
dataset-doctor-audit audit path/to/adult/prepared
```

Step 4 needs the `captured` adapter explicitly: the generic adapter, pointed at the same tree, found
**0 runs** and that empty inventory is kept as a separate report in the acceptance directory. That
difference is the honest state of Experiment Doctor on this project — its useful output here comes
from a declaration written at capture time, not from discovery.

Step 5 is the one a third party must supply: the acceptance run used a locally prepared Adult copy
identified by fingerprint `ds_05c7465f` (report SHA256
`c1456a7bf602d4c3b4cda5f316a1fdb9e04ed15b7149ec2eb393046428c82f5f`). No dataset was vendored into any
repository. If your Adult copy has a different fingerprint, your Dataset Doctor findings are about
**your** copy, not about the chain above — which is exactly the distinction the fingerprint exists to
make.

The Experiment Doctor reproduction also differs from the acceptance run in one disclosed way: the
captured bundle in `phase3/tabm/ed-captured/` was produced by `experiment-doctor init` on the audit
machine's clone, so its environment fields describe that machine, and the clone was deleted after
capture — only its three emitted artifacts are kept. `code.dirty=False` was true of the cloned tree at
capture time, and the lock file itself was its one untracked file.

Artifact digests for the whole chain are listed in
[`examples/tabm-chain/README.md`](../examples/tabm-chain/README.md).
