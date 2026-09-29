# Community

What contribution looks like here, and what does not. The project's bottleneck is not features — it is
evidence that these tools work for people who did not build them.

## Contribution classes that are genuinely useful right now

| Class | What you send | Why it matters |
| --- | --- | --- |
| **Run one Doctor on a new public project** | the command, the version, the findings file, and a short note on what surprised you | every component has been accepted on exactly one third-party project; one more is a real increase in coverage |
| **A new external provenance case study** | a `docs/` entry or an `examples/` directory, in the shape of `examples/tabm-chain/` | the stack's claim is that four layers compose; that claim needs traces we did not write |
| **A reproducible parser failure** | the smallest input that fails, what you expected, and the version | Paper Doctor's LaTeX parser is the most likely place to meet a corpus it has not seen |
| **A Windows or Linux compatibility report** | OS, Python version, command, output | Experiment Doctor and Result Doctor have **never** run in Windows CI; their Windows behaviour is unverified rather than known-good |
| **An onboarding defect** | the point in `docs/quickstart.md` where you got stuck, with what you typed | the quickstart was measured by its author; that is the weakest possible evidence for onboarding documentation |
| **A provenance gap you found in your own project** | what you could not trace, and why the artifacts do not record it | gaps are the output this stack is designed to produce; more gaps from more contexts is the point |
| **A real human first-use test** | your own verbatim notes while using a tool for the first time, unassisted | Paper Doctor's required human test is permanently recorded NOT OBSERVED; a genuine one would close a real gap, and a failure would be just as valuable |

## What this repository does not want

| Not wanted | Why |
| --- | --- |
| A fifth Doctor | the chain is four layers; adding a fifth is a scientific claim, not a feature request |
| A global score, a paper verdict, or a misconduct detector | the project's position is that it will not produce these |
| "Make it detect fabrication" | that requires judging scientific truth; these tools compare declarations to evidence |
| A PDF-image or OCR reading pipeline | out of scope; the input contract is the LaTeX source a project actually compiled from |
| A feature request with no user | the issue template asks which real person needs it; if nobody does, it does not get built |
| Low-value "good first issue" filler | an issue created to look welcoming costs a maintainer time and buys nothing |
| A new rule added to a component to fix a documentation gap | if the problem is wording, fix the wording in the owning repository |

## How to make a contribution land

1. **Pick the right repository.** Component behaviour goes to that component; portal documentation,
   case studies, metadata and onboarding go here. The routing table is in `README.md`.
2. **Bring the artifact, not the anecdote.** A findings file, a report JSON, or a command transcript is
   worth more than a description of what happened.
3. **Do not change a declaration to make a finding disappear.** If an audit reports `FAIL` on your
   project, the honest contribution is the `FAIL` plus what you learned — not a re-declared link.
4. **Expect `INCONCLUSIVE`.** It is a normal outcome, and reporting one is a contribution.
5. **Keep private data private.** Manifests quote file paths and digests; digests are usually enough to
   reproduce a finding without shipping the dataset. See `SECURITY.md`.

## Case study format

Use `examples/tabm-chain/README.md` as the template. A case study needs:

- the project, its repository, and the pinned revision;
- the tool versions, from `pip show` or `--version`, not from memory;
- the exact commands;
- the findings digests, so a reader can check that your artifacts and your claims match;
- every `UNKNOWN` and `INCONCLUSIVE`, unsorted and unreduced;
- one sentence on what the trace does **not** establish.

A case study that reports only `PASS` results is not a case study, and will be asked to include the
gaps.

## Talk to us

Open an issue here for anything spanning layers, and in the component repository for anything inside
one. There is no chat channel, mailing list, or discourse — that is a fact about the project's size,
not a policy. If you want one, say so in an issue with a reason; a coordination surface people actually
use is worth more than one that looks professional.
