# Component guide

Which Doctor your situation actually needs. You do not need all four for most tasks.

## Decision table

| Your situation | Start with | Then |
| --- | --- | --- |
| "I am about to train and want to know whether my splits leak" | Dataset Doctor `audit` | if it says `FORMAL_EVAL_INVALID`, fix the split and re-fingerprint before you trust any number |
| "I have data and want a stable identity for it, so a later audit can say which data" | Dataset Doctor `fingerprint` / `snapshot` | `diff` after any change |
| "I want my future runs to carry config, seed and environment evidence" | Experiment Doctor `init` + `run` around your existing command | `verify` the bundle, `audit` the project |
| "I inherited a results directory and want to know what is actually recorded in it" | Experiment Doctor `scan` (read-only, no manifest needed) | the inventory names every provenance gap it can see |
| "I know which runs are in my reported mean, and want to know if that is traceable" | Result Doctor — write the manifest that enumerates them | `audit`; read which rules came back `INCONCLUSIVE` because evidence is missing |
| "A paper table cell was produced and I cannot reconstruct how from the artifacts" | Result Doctor | its findings say which link in the chain is unrecorded |
| "I want to check whether a manuscript sentence matches the results it points at" | Paper Doctor — declare claims and links | `audit`; a `FAIL` is a question for the author |
| "I want end-to-end provenance for one reported number" | Start at the bottom: Dataset → Experiment → Result → Paper | write the joins yourself; see `docs/end-to-end-tabm.md` for what that looks like |
| "I only want to know whether a claim's number is printed the same way everywhere in the paper" | Paper Doctor alone | it needs no other tool |

## Per-component detail

### Dataset Doctor — `dataset-doctor-audit` (PyPI name `dataset-doctor-audit`, 0.1.2)

Owns: cross-split and entity leakage, duplicates, target and identifier leakage, label conflicts,
schema and distribution drift, dataset fingerprinting and diffing, split construction.

Commands measured from `--help`: `init`, `scan`, `audit`, `fingerprint`, `snapshot`, `diff`,
`report`, `rules`, `split`, `demo`, `show`. Rules DD001–DD021.

Use it when the evaluation boundary is the question. Do not use it to clean data: it reports and
fingerprints, and `split` is the only command that writes anything, into a new directory you name.

Its output vocabulary differs from the other three on purpose — verdicts like
`FORMAL_EVAL_SAFE / RISKY / INVALID` plus severity and impact class. See
`docs/status-semantics.md` before comparing its results with another tool's.

### Experiment Doctor — `experiment-doctor` (1.0.0)

Owns: run identity, seed provenance, resolved configuration, code revision, environment, metric and
checkpoint selection provenance, aggregation membership, termination cause.

Commands: `scan`, `audit`, `rules`, `adapters`, `init`, `run`, `verify`. Rules ED001–ED010, each
evaluated against a `family`, a `run`, or an `aggregation`.

Two distinct uses, and mixing them up causes confusion:

- **Read-only audit of artifacts that already exist.** `scan` then `audit`. Bundled adapters cover
  specific public layouts (measured: `generic`, `gmmvi-exp3`, `torchssl`, `crda`, `captured`); the
  generic adapter inventories without claiming metric semantics.
- **Capture while the experiment runs.** `init` writes `experiment.lock.json` recording code commit,
  config hashes, environment and seed with an explicit grade per field; `run` executes your command
  and wraps it in the evidence chain.

It does not compute metrics and does not schedule anything. If your runs already happened and
recorded nothing, most fields will be `UNKNOWN` — correctly.

### Result Doctor — `result-doctor` (0.1.0)

Owns: how runs become a reported number. Aggregation, membership, selection events, candidate sets,
transformations, comparison sets, and the printed cell itself.

Input is a manifest you write: `result-doctor audit path/to/result-doctor.yml`, or a project
directory containing `result-doctor.yml`. Rules RD001–RD008 over an eight-object bundle.

The contract that matters: it reads **only** the artifacts the manifest quotes, resolved relative to
the manifest's own `root:`. It never searches for a manifest and never infers anything from a file,
directory, run or group name. That is why two people on different machines get the same findings.

It never reads a claim. Bring Paper Doctor for that.

### Paper Doctor — `paper-doctor` (0.1.0)

Owns: whether a manuscript claim faithfully represents the reported evidence it explicitly points to.

Input is a manifest declaring claims, anchors and links: `paper-doctor audit path/to/paper-doctor.yml`.
Rules PD001–PD007 over `Claim` / `FloatAnchor` / `EvidenceLink`. A Result Doctor findings file may be
registered by digest as declared evidence.

Three things it will never do: infer a link from a name or a number, re-audit Result Doctor's
reasoning, or tell you the paper is correct. A `FAIL` means one declared relation does not agree with
the evidence on file — which includes the case where the author's own table is right and the audit
inputs were misaligned.

## Combining them

The stack's real product is a trace, and a trace is written by a person:

```text
paper-doctor.yml claim C8
   → declared link to a printed cell
      → result-doctor.yml reported result + enumerated members
         → experiment.lock.json / run artifact for one member
            → dataset-doctor report + fingerprint for the data that run read
```

Each arrow is a declaration in a manifest. Nothing computes them. When the chain is complete you can
answer "where did this number come from?" by citing four artifacts and four hashes, and you can also
see exactly where the chain stops being evidenced — which is the other half of the value. See
`docs/end-to-end-tabm.md` for a real one, gaps included.

## When not to use this stack

| Situation | Use instead |
| --- | --- |
| you want a quality score for a paper | nothing here; the stack refuses to produce one |
| you want automated peer review | out of scope by design |
| you want to detect fraud or misconduct | out of scope: a `FAIL` is one rule disagreeing with declared evidence |
| you want to check whether a cited external fact is true | Paper Doctor does not touch references' truth |
| you want data cleaning or augmentation | Dataset Doctor is read-only reporting plus `split` |
| you want experiment orchestration or tracking | Experiment Doctor is deliberately not that |
