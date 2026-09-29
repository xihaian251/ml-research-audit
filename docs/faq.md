# FAQ

The questions a careful reader asks before trusting any of this.

## What is actually being audited — reproducibility?

No. Provenance. The stack records which evidence supports which claim, aggregation, run, and dataset,
and it names what is missing. Reproducing a result requires executing training; nothing here does
that, and the TabM acceptance run executed none. A complete provenance chain and a reproduction are
different accomplishments and this project does not conflate them.

## If a tool says `FAIL`, is the paper wrong?

Not necessarily. `FAIL` means one rule found one inconsistency in the evidence supplied for one
target. In the TabM case study the paper-layer `FAIL` came from a declared link addressing the
`# Train` column while the claim's literal was the `# Test` figure — a mismatch in the audit's own
declaration, in a paper whose table is internally consistent. The dataset-layer `FAIL` came from
identical rows carrying different labels across a split boundary in a widely used public data
preparation. Both are findings about evidence, and neither is a verdict on a paper.

## Why does so much come back `INCONCLUSIVE`?

Because that is the true state of most published ML artifacts. In the TabM run, Experiment Doctor
could not decide three of its rules because no shipped artifact records the effective configuration,
the termination cause, or the runtime environment of a published run. `INCONCLUSIVE` converts a vague
"not reproducible" complaint into three named missing files. A tool that returned `PASS` there would
be guessing.

## Why doesn't the stack just link claims to results automatically?

Because an inferred link puts the tool's guess inside the audit trail, and then "who asserted this?"
has no answer. Every join here is written in a manifest by a person, and the manifest names the basis
(`AUTHOR_REF_IN_SENTENCE`, `AUTHOR_NAMED_FLOAT`, or `AUDITOR_DECLARED`). This costs manual work and buys
accountability. It is the central design decision, not a missing convenience.

## Why four separate tools instead of one CLI?

Different input domains, different dependency graphs, different release cadences, and deliberately
different status vocabularies. Merging them would force one flattened score, and a flattened score is
the output this project has decided not to produce. See `docs/architecture.md` §2.

## Why is there no total score for a paper?

Because averaging unlike evidence produces a number nobody can falsify or trace. A `CRITICAL`
duplicate finding in a dataset and a misaddressed table column in a manuscript are not the same kind
of statement, and no arithmetic makes their mixture meaningful. The stack gives per-rule statuses, per-
target, with reasons naming the evidence.

## Isn't `UNKNOWN` just the tool giving up?

`UNKNOWN` is a recorded property of evidence, not a tool state. The tools distinguish `NOT_APPLICABLE`
(no such relation exists for this target), `INCONCLUSIVE` (the relation exists and the file cannot
decide it), and `NOT_RUN` (you gave me no target of that class). Collapsing those three would hide
exactly the information an auditor needs.

## Can I use this in CI?

For Result Doctor and Paper Doctor: exit code `0` means the audit ran whatever it found, `2` means the
manifest is not a readable contract, `1` means the tool failed. So a `FAIL` does not break your build,
and a broken build always means no findings were produced at all. Dataset Doctor documents non-zero
exit on blocking findings, plus a stricter `--ci` mode. Decide your own policy; do not assume the four
tools share one.

## Do I need all four tools?

No. Most tasks need one. `docs/component-guide.md` maps situations to tools. Auditing whether a
sentence matches a table needs only Paper Doctor.

## Why does Dataset Doctor install under a different name?

`pip install dataset-doctor-audit`. The name `dataset-doctor` on PyPI belongs to an unrelated
MIT-licensed data-cleaning project. The import package is `dataset_doctor_audit`. This is a measured
fact from the PyPI API, recorded in `research/COMPONENT_FACTS.md`.

## Are the four tools' versions meaningful?

They are independent release lines: Experiment Doctor is at 1.0.0, Dataset Doctor at 0.1.2, Result
Doctor and Paper Doctor at 0.1.0. Differences reflect each tool's own freeze history, not a ranking of
maturity across layers. All released tags are frozen and will not be moved.

## Is this project widely used?

No. Four released components, one completed end-to-end acceptance run on a third-party paper, zero
observed independent users, and no real human first-use test — Paper Doctor's was waived for 0.1.0 and
is permanently recorded as NOT OBSERVED. `STACK_STATUS.md` states this without softening it, and it is
the main reason the project's next phase is adoption rather than features.

## Can I ask it to check whether a claim is scientifically sound?

No, and that refusal is the product. The tools answer whether a claim agrees with the evidence it
explicitly points to. Whether that evidence is good science is a question for reviewers with domain
knowledge. A language model judging scientific truth is explicitly out of scope: no rule in any of the
four tools calls a model.

## What is the difference between this repository and the four tools?

This is a portal: identity, architecture, onboarding, the case study, ecosystem metadata, and
community routing. It contains no tool source code, no submodules, no vendored releases, and publishes
no PyPI package. Component bugs belong in the component repositories.
