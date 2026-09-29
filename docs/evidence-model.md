# Evidence model

Four kinds of evidence appear in this stack, and the distinction between them is the content of the
audit. Each tool uses its own vocabulary, taken from its own published code rather than invented
here. There is deliberately no single evidence scale that all four share.

## 1. The four kinds

| Kind | Meaning | Who can assert it |
| --- | --- | --- |
| **Observed / direct** | the tool read it from an artifact or from the data itself | only the tool, and only for a path it was given |
| **Declared** | a person stated it in a manifest, lock file, or report | the author or the auditor, named in the field |
| **Derived** | the tool computed it from observed inputs by a documented rule | the tool, and reproducible by anyone |
| **Unknown** | nothing on file decides it | nobody — and this is a recorded state, not a failure |

The invariant that governs all four:

> A provenance link may be explicit, and explicit linkage still does not imply scientific truth.

Declaration establishes **who said what**, not whether it is the case.

## 2. Each tool's own vocabulary

Measured from the installed distributions on 2026-09-29 (enum definitions inside each package).

### Result Doctor and Paper Doctor — shared grades

```
DIRECT  DERIVED  DECLARED  INFERRED  UNKNOWN
```

`INFERRED` exists in the type system and is the grade the project most deliberately avoids using:
an inference is the tool's own guess, and a guess inside an audit trail cannot be traced back to an
author. Where a rule cannot decide, output is `INCONCLUSIVE` and the underlying grade stays
`UNKNOWN`.

Manifest fields in these two tools are literally authored as one of the three usable kinds:

```yaml
value:    {declared: {value: "91.4", by: author, statement: "the paper prints 91.4"}}
universe_evidence: {observed: {path: train.py, line: 88, text: "for epoch in range(30)"}}
tie_break: {unknown: "no tie rule is recorded"}
```

Note the shape: `declared` carries `by:`. A declaration without an attributed author is not a
provenance statement.

Both tools also carry a `UniverseStatus` for enumeration completeness:

```
UNKNOWN  RECOVERED  PARTIAL  DECLARED_ONLY  UNRECOVERABLE
```

This is where "did you list all the runs?" is answered honestly. `PARTIAL` blocks a `PASS` on
membership rules, because an unlisted universe cannot be certified — the mechanism behind one of the
`INCONCLUSIVE` results in the TabM case study.

Paper Doctor additionally records **why a claim and an anchor were paired**:

```
LinkBasis:   AUTHOR_REF_IN_SENTENCE | AUTHOR_NAMED_FLOAT | AUDITOR_DECLARED
PairingBasis: DECLARED | SUGGESTED
```

These three are the only bases that exist. A tool never adds a fourth by noticing that a number
appears nearby.

### Experiment Doctor — provenance status per field

```
CONFIRMED  SUPPORTED  INFERRED  UNKNOWN  CONFLICTING
```

`experiment-doctor init` prints a grade for every field it writes, so the asymmetry is visible at
capture time rather than discovered later:

```
code.commit=CONFIRMED   configuration.config_hash=CONFIRMED   environment.python_version=CONFIRMED
dataset.fingerprints=UNKNOWN   execution.command=UNKNOWN
```

`CONFLICTING` is the state where two artifacts disagree, and it is reported instead of resolved.

### Dataset Doctor — evidence class, severity, formal impact, verdict

Dataset Doctor does not use these words at all. Its axes are:

```
EvidenceType: DETERMINISTIC | HEURISTIC | STATISTICAL
Severity:     INFO | LOW | MEDIUM | HIGH | CRITICAL
FormalImpact: NONE | POTENTIAL | BLOCKING
EvalSafety:   FORMAL_EVAL_SAFE | FORMAL_EVAL_RISKY | FORMAL_EVAL_INVALID | INCONCLUSIVE
```

The distinction that matters is between the last two lines. `DETERMINISTIC` evidence means a rule
found an exact structural condition (cross-split duplicate rows); `STATISTICAL` means a distribution
test; `HEURISTIC` means a similarity heuristic with tunable thresholds. The verdict describes
whether a *formal evaluation* on those splits can be trusted — it is not an evidence grade, and it is
not a statement about the quality of the data or the science built on it.

## 3. What crosses a layer, and what does not

| Case | Status |
| --- | --- |
| A Paper Doctor manifest pins a Result Doctor findings file by SHA256, size and `rd_version` | the **only** formal cross-tool evidence interface in the stack; verified as the manifest parses |
| A Result Doctor manifest enumerates the runs in an aggregation | declared, attributed, auditable — not observed |
| An Experiment Doctor run names a dataset path | declared, unless a Dataset Doctor fingerprint is recorded in it |
| A paper sentence and a table cell that "look related" | nothing. Not represented, not scored, not mentioned |

What never crosses: a grade. `UNKNOWN` at the run layer is still `UNKNOWN` at the paper layer. If
the paper claim is about that run's metric, Paper Doctor's own rule output is limited by the evidence
it was given, and it says so in its `reason` string. This is the concrete form of "certainty must not
silently increase across layers".

## 4. How to read a `reason` string

Every finding in Result Doctor and Paper Doctor carries a sentence naming the evidence it used, in a
fixed pattern:

```text
PD001  PASS  C1
  reason: declared link(s) with basis AUTHOR_REF_IN_SENTENCE resolve to evidence on file
          (paper.tex [column=Accuracy,row=A], tab-results)

RD003  INCONCLUSIVE  selection:sel:0
  reason: criterion fields not all direct:
          {'metric': 'DIRECT', 'split': 'DECLARED', 'direction': 'DECLARED',
           'scope': 'DECLARED', 'tie_break': 'UNKNOWN', 'timing': 'DIRECT'}
```

Read the second one as a checklist of what to go and record: the split and the direction are
author statements, and no tie rule exists on file. That is the practical value of an evidence-graded
tool — it converts "the audit was inconclusive" into five named missing artifacts.

## 5. Declared evidence is not weak evidence — it is different evidence

A common objection: "if a human wrote the manifest, the audit only checks the human's honesty." True,
and that is the design's honest boundary. What a declaration buys is not truth but **traceability**:
when the reported number turns out to be wrong, the stack tells you which declaration was wrong, who
made it, and which layer's evidence stopped being sufficient. An inferred link would have hidden all
three of those facts inside a model's guess.
