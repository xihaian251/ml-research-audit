# Quickstart

Ten minutes, assuming you are a competent ML researcher who has never seen this project. Every
command below was run and measured on 2026-09-29 with the published packages, on Windows with
Python 3.13. Nothing here is a plan or an aspiration.

## 1. Install all four

```bash
pip install dataset-doctor-audit experiment-doctor result-doctor paper-doctor
```

They coexist in one environment; there is no dependency conflict between them.

One naming trap, and it is a real one: **Dataset Doctor's PyPI name is `dataset-doctor-audit`**, not
`dataset-doctor`. The name `dataset-doctor` on PyPI belongs to an unrelated MIT-licensed data
cleaning project. `pip install dataset-doctor` does not install this tool.

| Tool | PyPI name | Command | Version measured |
| --- | --- | --- | --- |
| Dataset Doctor | `dataset-doctor-audit` | `dataset-doctor-audit` | 0.1.2 |
| Experiment Doctor | `experiment-doctor` | `experiment-doctor` | 1.0.0 |
| Result Doctor | `result-doctor` | `result-doctor` | 0.1.0 |
| Paper Doctor | `paper-doctor` | `paper-doctor` | 0.1.0 |

## 2. Verify the CLI is available

```bash
dataset-doctor-audit --help
experiment-doctor  --help
result-doctor      --help
paper-doctor       --help
```

All four print a command list. Two of them also answer `--version`:

```bash
result-doctor --version    # result-doctor 0.1.0
paper-doctor  --version    # paper-doctor 0.1.0
```

`dataset-doctor-audit --version` and `experiment-doctor --version` do **not** exist; they print a
usage error. That is a measured difference between the tools, not a broken install. To read those
two versions, ask pip:

```bash
pip show dataset-doctor-audit experiment-doctor
```

Two further measured quirks worth knowing before they confuse you:

- `experiment-doctor --help` says "Experiment Doctor v0.1". The published distribution is 1.0.0.
  The help string is stale; the package is not.
- Use the console scripts. `python -m paper_doctor` is not a supported entry point: measured on the
  published 0.1.0 wheel it exits 1 with `No module named paper_doctor.__main__`.

## 3. Smallest run per layer

Two tools ship a self-contained demo, and two need an example manifest from their own repository.
That difference is real, so it is stated rather than smoothed over.

### Dataset Doctor — built-in demo, no files needed

```bash
mkdir demo && cd demo
dataset-doctor-audit demo
```

This generates small datasets with deliberately planted faults and audits them. Expect a report that
names the planted cross-split duplicates and conflicting labels, and a verdict line such as
`FORMAL_EVAL_INVALID`. Exit code 0 — the audit ran; the finding is a scientific statement, not a tool
error.

### Experiment Doctor — capture, then audit

```bash
mkdir my-experiment && cd my-experiment
git init -q && printf 'lr: 0.1\n' > config.yaml && printf 'print("hi")\n' > train.py
git add -A && git commit -qm start

experiment-doctor init --seed 42 --config config.yaml
experiment-doctor audit . -o ./doctor-report
```

`init` writes `experiment.lock.json` and prints the evidence grade of every field it recorded. On a
toy project it prints a lot of `UNKNOWN`, and that is the point:

```text
code.commit=CONFIRMED, configuration.config_hash=CONFIRMED, environment.python_version=CONFIRMED,
dataset.fingerprints=UNKNOWN, execution.command=UNKNOWN, start_time=UNKNOWN
```

The tool records what the declaration establishes and refuses to guess the rest. Open
`doctor-report/report.md` to see the same asymmetry in the rule results.

### Result Doctor — audit a shipped example

Result Doctor reads a manifest you declare; there is no built-in demo, so use the one in its
repository:

```bash
git clone --depth 1 -b v0.1.0 https://github.com/xihaian251/result-doctor.git
result-doctor audit result-doctor/tests/generic_fixtures/example_b/result-doctor.yml
```

The example is designed to show contrast, and it does:

```text
RD001   FAIL    acc/x    members, aggregation and transforms are all determined yet the cell differs
RD001   PASS    acc/y    recomputed rendering equals the reported cell
```

### Paper Doctor — audit a shipped example

```bash
git clone --depth 1 -b v0.1.0 https://github.com/xihaian251/paper-doctor.git
paper-doctor audit paper-doctor/examples/quickstart/paper-doctor.yml
```

```text
PD001   PASS           C1   declared link(s) with basis AUTHOR_REF_IN_SENTENCE resolve to evidence on file
PD001   INCONCLUSIVE   C3   the claim carries no declared support link; untraceable is not false
PD003   FAIL           C2   the claim states 0.92 but the printed cell at (column=Accuracy, row=B) states 0.88
```

Read `PD001 INCONCLUSIVE` as: this claim has no declared support, so nothing is known about its
relation to evidence. It is not a criticism of the sentence.

## 4. How the layers connect

Each tool answers one question about one kind of object:

```text
dataset  →  experiment run  →  reported result  →  paper claim
DD            ED                 RD                 PD
```

They do not talk to each other automatically. A cross-layer trace exists because someone wrote down
the join — which run belongs to which aggregation, which aggregation backs which printed cell, which
cell backs which sentence. Paper Doctor can carry a Result Doctor findings file as declared evidence
by pinning its SHA256 and version in its own manifest; that is the only formal connection between
the layers, and it is a declaration with a digest, not a live link.

`docs/architecture.md` explains why this was chosen. The short version: an inferred link would put
the tool's guess inside your audit trail, and then nobody could trace who asserted it.

To see a complete four-layer trace of one real number in a real published paper, read
`docs/end-to-end-tabm.md`. It is five commands and one table, and it ends with eight things that
remained UNKNOWN.

## 5. Where to go next

| You want to | Go to |
| --- | --- |
| pick the right tool for your situation | `docs/component-guide.md` |
| understand PASS / FAIL / INCONCLUSIVE / UNKNOWN | `docs/status-semantics.md` |
| read a full four-layer audit of a published paper | `docs/end-to-end-tabm.md` |
| contribute a case study from your own project | `docs/community.md` |
| report a bug | the component's own repository — routing table in `README.md` |
