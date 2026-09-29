# Status semantics

Five statuses look the same across three tools and do not mean the same thing. This page explains
the shared concept without pretending the schemas are identical — because flattening them into one
scale is precisely the output this project refuses to produce.

## 1. The shared conceptual rule set

Result Doctor (RD001–RD008) and Paper Doctor (PD001–PD007) print exactly this vocabulary, taken from
their own `--help` output:

| Status | Conceptual meaning | Result Doctor's wording | Paper Doctor's wording |
| --- | --- | --- | --- |
| `PASS` | the evidence on file decides this narrow target in favour of the report | "the evidence the manifest supplies decides this target in favour of the report" | "this narrow relation agrees with the evidence on file - nothing more" |
| `FAIL` | one rule found an inconsistency in the evidence for this target | "one rule found an inconsistency in the evidence for this target - not a failed experiment or paper" | "one rule found the claim disagree with the evidence for this target - not a failed experiment or paper" |
| `INCONCLUSIVE` | evidence on file is insufficient to decide | same wording | same wording |
| `NOT_APPLICABLE` | this target has no such dependency / relation to check | same wording | same wording |
| `NOT_RUN` | no target of the class this rule reads was supplied | same wording | same wording |

Experiment Doctor's rules use the same five values (measured: its `Status` enum for rules is
`PASS, FAIL, INCONCLUSIVE, NOT_APPLICABLE, NOT_RUN`), while its *provenance* fields use a different
scale — see §3.

Three reading rules that apply everywhere:

- **`FAIL` is a finding, not a verdict.** It names one rule and one target. It is a question to ask an
  author. Nothing in this stack concludes that a paper is unreliable, and nothing concludes that one
  is reliable.
- **`INCONCLUSIVE` is not a failure of the tool and not a failure of the science.** It is a report of
  missing evidence, and it is the most actionable status on the page: it tells you which artifact to
  go and record.
- **`NOT_APPLICABLE` is not `INCONCLUSIVE`.** The first means the relation does not exist for this
  target; the second means it exists and the file cannot decide it.

## 2. `UNKNOWN`

`UNKNOWN` is not one of the five rule statuses. It is a property of **evidence**, and it appears in
the grade fields of three tools under their own spellings (`docs/evidence-model.md`):

| Tool | Field | Values |
| --- | --- | --- |
| Result Doctor, Paper Doctor | evidence grade | `DIRECT`, `DERIVED`, `DECLARED`, `INFERRED`, `UNKNOWN` |
| Result Doctor, Paper Doctor | enumeration completeness | `UNKNOWN`, `RECOVERED`, `PARTIAL`, `DECLARED_ONLY`, `UNRECOVERABLE` |
| Experiment Doctor | provenance status per field | `CONFIRMED`, `SUPPORTED`, `INFERRED`, `UNKNOWN`, `CONFLICTING` |
| Dataset Doctor | formal evaluation verdict | `FORMAL_EVAL_SAFE`, `FORMAL_EVAL_RISKY`, `FORMAL_EVAL_INVALID`, `INCONCLUSIVE` |

A rule whose evidence is `UNKNOWN` normally outputs `INCONCLUSIVE`. The chain of reasoning is
therefore explicit and inspectable: missing evidence → inconclusive rule → a named gap in the trace.

## 3. Experiment Doctor's two vocabularies

Experiment Doctor reports two different things and does not merge them:

- **Provenance per field** (`experiment-doctor init` prints it, measured):
  `code.commit=CONFIRMED`, `randomness.seed=CONFIRMED`, `dataset.fingerprints=UNKNOWN`,
  `execution.command=UNKNOWN`. This is a statement about what an artifact records.
- **Rule outcomes** (`audit`): the same five statuses as RD/PD, e.g.
  `ED004 INCONCLUSIVE`, `ED002 PASS`.

The reason both exist: ED004 asks whether a *resolved configuration* is recorded, which is a
provenance question, while ED007 asks whether a published mean can be recomputed from the runs,
which is a decision rule with a pass/fail answer.

## 4. Dataset Doctor's own semantics, kept separate

Dataset Doctor audits data, not claims, and its vocabulary reflects that. Measured from the
enumerations inside the installed 0.1.2 package:

| Axis | Values | What it answers |
| --- | --- | --- |
| `AuditStatus` | `PASS`, `FAIL`, `WARNING`, `INCONCLUSIVE`, `NOT_RUN`, `UNSUPPORTED`, `SUPPRESSED` | did this rule decide, and how strongly |
| `Severity` | `INFO`, `LOW`, `MEDIUM`, `HIGH`, `CRITICAL` | how much this finding matters to the evaluation |
| `FormalImpact` | `NONE`, `POTENTIAL`, `BLOCKING` | whether formal evaluation on these splits is affected |
| `EvidenceType` | `DETERMINISTIC`, `HEURISTIC`, `STATISTICAL` | how the finding was established |
| `EvalSafety` | `FORMAL_EVAL_SAFE`, `FORMAL_EVAL_RISKY`, `FORMAL_EVAL_INVALID`, `INCONCLUSIVE` | the aggregate statement about the evaluation boundary |

Two things a Dataset Doctor verdict does **not** mean:

- `FORMAL_EVAL_INVALID` does not mean the dataset is bad or the model is wrong. It means formal
  evaluation on these splits cannot be trusted — the boundary itself is compromised. In the TabM
  case study it fired on `DD009` conflicting labels for identical content across splits, which is a
  statement about the published Adult preparation.
- `FORMAL_EVAL_SAFE` does not mean the data is good. Its own report wording says so: *"SAFE here
  means no blocking issue found by the rules that could run."*

Its coverage line is also worth reading literally: a report lists rules that were `NOT_RUN` or
`UNSUPPORTED`, so a passing audit is explicitly a passing audit *of the subset that could execute*.

## 5. Exit codes are a separate axis from findings

This is the contract that stops a scientific result from being mistaken for a crash.

| Tool | Exit code | Meaning |
| --- | --- | --- |
| Result Doctor | `0` | the audit ran, whatever it found — including `FAIL` |
| | `2` | the manifest is not a readable contract |
| | `1` | the tool failed unexpectedly |
| Paper Doctor | `0` / `2` / `1` | the same contract, printed in its own `--help` |

Both tools state this in their own `--help` output. A `FAIL` in a CI pipeline therefore does not
break the build, and a broken build always means the audit did not produce findings at all. Do not
wire these CLIs to fail on findings unless you have decided that a provenance finding is a build
error — which is a policy choice about your own pipeline, not a property of the tools.

Dataset Doctor and Experiment Doctor expose no `--version` flag and have their own CLI behaviour;
Dataset Doctor documents `audit` exiting non-zero on blocking findings, and a stricter `--ci` mode.
Read the component's own README before scripting it.

## 6. What never happens

| Forbidden | Why it is on this list |
| --- | --- |
| Averaging statuses across rules or layers | unlike evidence merged into one number is unreadable and unfalsifiable |
| Promoting `INCONCLUSIVE` upward into a `PASS` | certainty must not silently increase across layers |
| Treating `NOT_RUN` as `NOT_APPLICABLE` | one means "you did not give me a target", the other means "no such relation exists" |
| Reporting an `INFERRED` grade as support | an inference is the tool's guess, and a guess cannot be traced to an author |
| A single trust score for a paper | the stack has no semantics for it and refuses to invent one |
