# Contributing

Three sentences on where things belong, then the specifics.

This portal accepts documentation, case studies, onboarding material, architecture clarifications,
metadata corrections, and community content. Behaviour of a tool belongs in that tool's repository.
Nothing in this repository changes what any of the four components does.

## Where your change goes

| You have | Open it in |
| --- | --- |
| a leakage / split / fingerprint / dataset-audit behaviour change or bug | [dataset-doctor](https://github.com/xihaian251/dataset-doctor) |
| a capture / run identity / adapter / provenance change | [experiment-doctor](https://github.com/xihaian251/experiment-doctor) |
| an aggregation / membership / selection / transformation rule change | [result-doctor](https://github.com/xihaian251/result-doctor) |
| a claim / anchor / link / LaTeX parsing change | [paper-doctor](https://github.com/xihaian251/paper-doctor) |
| a new external case study, or an onboarding defect, or a wrong version/link/metadata here | **this repository** |
| a security issue | see `SECURITY.md` — do not open a public issue |

## What a good contribution to this repository looks like

- **A case study** following `examples/tabm-chain/README.md`: pinned revision, exact commands, findings
  digests, every gap listed. The single highest-value contribution available.
- **An onboarding fix**: "step 3 of `docs/quickstart.md` fails because `--version` does not exist for
  Dataset Doctor" is worth more than ten feature requests.
- **A metadata correction**: versions, tags, release commits and CLI names here all trace to
  `research/COMPONENT_FACTS.md`. If you find a published value that disagrees with PyPI or GitHub, that
  is a defect in this repository, and the census is what gets re-measured.
- **A cross-platform report**: Experiment Doctor and Result Doctor have no Windows CI, so a Windows
  run from you is new evidence, not a duplicate.

## What will be closed rather than merged

- A change that adds a rule, adapter, or scientific behaviour to a component **through this repo**.
  Components are frozen at their released tags for this round; the owning repository is the place.
- Anything that introduces a global score, a paper verdict, a misconduct label, or a model-based
  judge. These are not gaps to be filled later; see `ROADMAP.md` §"Not planned without evidence".
- Documentation that softens a limitation. If a limit is real, the correct change is to explain it
  better, not to remove the sentence.
- A claim of adoption, users, validation, or human testing that no artifact supports. `STACK_STATUS.md`
  is a measured document.
- Feature requests with no user behind them. The template asks four questions; the fourth one — "can
  this already be represented as `UNKNOWN` or `INCONCLUSIVE`?" — is the one that usually answers itself.

## Before you open a pull request

1. Read `docs/architecture.md` §3 (responsibility boundaries) and `docs/status-semantics.md`. Most
   proposed "improvements" are boundary violations dressed as features.
2. Keep it small and single-purpose. This repository's history is deliberately readable: documentation,
   community, CI.
3. Run the portal check, which is offline and read-only:

   ```bash
   pip install pyyaml
   python scripts/verify_stack.py
   ```

4. If you changed a version, tag, CLI name, or release statement, re-measure it from PyPI or the
   GitHub API and update `research/COMPONENT_FACTS.md` with the source. Do not copy the number from
   another document, including this one.
5. Quote your evidence: command, output, digest. A sentence that says "I ran it and it worked" is not
   evidence about a machine you did not tell us about.

## Language discipline

This project's credibility rests on saying exactly what it means:

| Say | Do not say |
| --- | --- |
| "audits provenance" | "proves reproducibility" |
| "one rule disagreed with the declared evidence" | "found an error in the paper" |
| "the evidence on file does not decide this" | "the result could not be reproduced" |
| "released" | "validated", "battle-tested", "trusted" |
| "one acceptance run on one third-party paper" | "verified against real-world research" |
| "no human first-use test has been observed" | "onboarding tested" |

An `INCONCLUSIVE` you are tempted to round up to a `PASS` is a finding. Report it.

## Style

Markdown, one idea per sentence, tables over prose for facts. Version numbers, digests, and commit
SHAs are written in full and never paraphrased. Every number in this repository must be traceable to a
command someone ran.
