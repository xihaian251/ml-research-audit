# Pull request

The four tools are released and their tags are frozen. Almost every mergeable change in this
repository is a documentation, metadata, routing, or verification change.

## Which repository is this for

| If the change touches… | Open the PR in |
|---|---|
| data-layer behaviour | `xihaian251/dataset-doctor` |
| run capture, adapters, ED rules | `xihaian251/experiment-doctor` |
| result contracts, RD rules | `xihaian251/result-doctor` |
| claim manifests, PD rules | `xihaian251/paper-doctor` |
| this portal: README, docs, `stack.yaml`, `verify_stack.py`, CI, templates | here |

A PR opened here that changes component behaviour will be closed with a link to the owning
repository. Released commits must not be rewritten and frozen tags must not be moved; a component
fix is a new release, not an edit of history.

## What a mergeable portal PR looks like

- **A factual correction.** The old sentence, the new sentence, and the source that decides between
  them. Source authority order is PyPI JSON API, then the published wheel metadata and entry points,
  then the GitHub release and tag, then the tool's own `--help`, then the repository tree, then the
  README. A README never outranks a release artifact.
- **A real onboarding defect.** "I ran this and hit that" beats "the docs could be clearer." If the
  fix is a worked example, run the example before committing it.
- **A recorded external case study**, added to `docs/` or `examples/` with the participant's consent.
- **A metadata update** to `stack.yaml`, which must always arrive with a re-measured
  `research/COMPONENT_FACTS.md` entry, not from memory.

## Before you submit

- [ ] `python scripts/verify_stack.py` exits 0.
- [ ] `python scripts/verify_stack.py --online` exits 0, **or** the mismatch is stated in the PR
      description as a stale-census finding rather than silently corrected.
- [ ] Every new command line in this PR was actually executed, at the released version, in a clean
      environment. Undiscovered commands are not published here.
- [ ] Every new number has a source in the census or a measurement artifact path.
- [ ] No wording was softened to make the project read better. Limitations are documentation.
- [ ] No new vocabulary was invented for a state that already has a name (`UNKNOWN`, `INCONCLUSIVE`,
      `NOT_RUN`, `NOT_APPLICABLE`, `DECLARED_ONLY`, `UNRECOVERABLE`).
- [ ] If a document now states a version, a tag, or a commit, it was re-measured today.
- [ ] Nothing private, unpublished, or named after an anonymous third party appears in the diff.

## One thing the reviewer will check first

Does the change keep certainty flat across layers? If the diff promotes an inferred or declared
relation into a confirmed one, reports an aggregate judgement that the tools do not compute, or
presents one acceptance run as validation, the answer is no — and the PR needs a design discussion
before any edit.

## Description template

```
What changed in one sentence:
Why:
Evidence (command + output, or source URL):
Which surface it fixes (portal file, or the component docs this portal routes to):
What is still unknown after this change:
```
