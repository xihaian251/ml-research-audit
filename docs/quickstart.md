# Quickstart

Assuming you are a competent ML researcher who has never seen this project. Every command below was
run and measured on 2026-09-29 with the published packages, on Windows with Python 3.13. Nothing here
is a plan or an aspiration.

**What "quickstart" covers, and what it does not.** Sections 1-3 get you to a real finding from other
people's fixtures, and two fresh-user audits measured that at roughly 4-6 minutes to a `FAIL` at the
dataset layer and 10-15 minutes to reach one per layer. What it does not promise is a ten-minute
audit of *your own* number: Result Doctor and Paper Doctor have no demo, so a first audit of your own
project means writing a manifest, and that is a schema-reading exercise whose cost has never been
measured by this project. `examples/minimal-result-manifest/` is the fastest honest route into that,
and `docs/faq.md` states the cost rather than hiding it.

## 1. Install all four

```bash
pip install dataset-doctor-audit experiment-doctor result-doctor paper-doctor
```

They coexist in one environment; there is no dependency conflict between them. Install them into a
virtual environment you control (`python -m venv .venv`, then activate it) rather than into your
training environment: these are audit tools, and a stray dependency change in the environment that
produces your results would be an awkward way to find out.

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

This generates three small datasets with deliberately planted faults and audits each one:
`leaky_tabular`, `clean_tabular` (a control), and `leaky_images`. Expect a report that names the
planted cross-split duplicates and conflicting labels, and a verdict line such as
`FORMAL_EVAL_INVALID`.

Then audit the generated fixtures directly, because that is where the exit-code difference lives:

```bash
dataset-doctor-audit audit dataset-doctor-demo/leaky_tabular -o rep_leaky; echo $?
dataset-doctor-audit audit dataset-doctor-demo/clean_tabular -o rep_clean; echo $?
```

Measured on the published 0.1.2 wheel, both commands above, on the same three fixtures the demo had
just produced:

| Command | Verdict line | Exit code |
| --- | --- | --- |
| `demo` (audits all three fixtures internally) | prints `FORMAL_EVAL_INVALID` for `leaky_tabular` | `0` |
| `audit …/leaky_tabular` | `FORMAL_EVAL_INVALID 316 samples / 21 rules` | `1` |
| `audit …/clean_tabular` | `FORMAL_EVAL_SAFE 300 samples / 21 rules` | `0` |

Read that table carefully; it is the sharpest edge in this stack. Dataset Doctor is the one tool
whose exit code **does** react to findings — `audit` exits `1` when a finding blocks formal
evaluation, unlike Result Doctor and Paper Doctor which exit `0` whatever they conclude. And `demo`
exits `0` even though it just audited a leaking dataset, because the demo's job is to show you
output, not to gate your build. If you script the gate, script `audit`.
`docs/status-semantics.md` §5 has the full exit-code contract per tool.

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

Result Doctor reads a manifest you declare; there is no built-in demo. This portal ships the
smallest manifest that produces a decision, so you can run it without cloning anything:

```bash
cd examples/minimal-result-manifest
result-doctor audit result-doctor.yml            # PASS: 3, FAIL: 0, NOT_APPLICABLE: 2, NOT_RUN: 3
result-doctor audit result-doctor.noscale.yml    # RD001 FAIL - a scale step is missing from steps
```

[`examples/minimal-result-manifest/README.md`](../examples/minimal-result-manifest/README.md) walks
through why the passing run is only three rules out of eight. If you would rather see an example
authored by the component itself:

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

To build that bridge, note the one flag whose shape is easy to get wrong: `--json` takes the output
path as its **value**.

```bash
result-doctor audit manifest.yml --json rd-findings.json    # correct
result-doctor audit manifest.yml --json > rd-findings.json  # usage error, exit 2
```

The second form is not hypothetical. It is the form printed in the released Paper Doctor README, and
it fails: `--json` takes the redirect target as nothing at all (it gets no value), `result-doctor`
exits `2` with `argument --json: expected one argument`, and the shell has already created
`rd-findings.json` as a 0-byte file. Paper Doctor treats "a digest that does not match the bytes" as
a `2`-class contract error, so a manifest pinned to that empty artifact fails in the next step with
what reads like a tampering problem and is actually a shell problem. This portal uses the value form
everywhere, including in `docs/end-to-end-tabm.md`, and records the upstream README line in
[`research/COMPONENT_FACTS.md`](../research/COMPONENT_FACTS.md) §4.

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
