# Roadmap

This roadmap is deliberately arranged to argue against its own expansion. The scientific design of the
four layers is finished and released; the missing thing is evidence that other people can use it.
Sections are therefore ordered by what has to happen, not by what sounds like progress.

## NOW

Nothing here requires a change to a component's scientific behaviour.

- **External adoption.** One more project traced end to end by someone who did not build the tools.
  The single metric this roadmap cares about.
- **Documentation that survives a stranger.** `docs/quickstart.md` was measured by its author, which is
  the weakest possible evidence for onboarding documentation. Every stumble report is a fix.
- **Independent case studies.** Accepted in `examples/`, formatted like `examples/tabm-chain/`.
- **Real user onboarding.** Paper Doctor's required human first-use test is permanently recorded NOT
  OBSERVED for 0.1.0. This does not become a checkbox; it becomes an observation.
- **Bug fixes in the owning component.** Where a defect is reported and reproduced. Not preemptively.
- **Documentation defects already measured and listed in `STACK_STATUS.md` §4** — including the Result
  Doctor README that says the package is not on PyPI, the Experiment Doctor help string that says
  v0.1, and the Paper Doctor README line that prints the cross-layer bridge command in a form that
  cannot work (`--json` with no value plus a shell redirect). Each belongs to its own repository and
  each needs a release there; the portal has fixed only its own copies.
- **One usage error worth a clearer message.** `experiment-doctor audit --adapter <typo>` exits `1`
  with a bare `KeyError` traceback naming the adapters that exist. The behaviour is recoverable and
  the message is technically correct, so this is polish, not a defect: an unknown adapter name should
  be a `2`-class usage error. Recorded in `research/COMPONENT_FACTS.md` §7.4.

## NEXT — only features that external usage justifies

A candidate enters this section when someone outside the project has demonstrated the need. Not before.

- Additional adapters for public repository layouts, driven by a reported case that could not be
  audited with what ships today.
- Second-platform CI for Experiment Doctor and Result Doctor, if a real Windows or macOS user reports a
  difference — their Windows behaviour is currently unverified, not known-bad.
- `--version` for Dataset Doctor and Experiment Doctor, if a user report shows the absence actually
  blocks a workflow rather than merely surprising someone.
- Cross-repository link from each component README into this portal. A documentation-only change, and
  deliberately not made in this round.

## LATER — possible, evidence permitting

| Idea | What would have to be observed first |
| --- | --- |
| An umbrella PyPI meta-package | repeated reports that installing four packages by name is a real obstacle |
| Machine-readable bundle exchange between tools | at least two independent users needing a join the manifest does not already express |
| Integrations with experiment trackers or model cards | a user showing that provenance captured elsewhere cannot be represented as a declaration here |
| A second end-to-end acceptance target | someone else running one, and it disagreeing with ours somewhere |
| A hosted dashboard over the four reports | demand for reading findings in bulk, plus a privacy answer for datasets under agreement |

## NOT PLANNED WITHOUT EVIDENCE — and mostly not planned at all

| Will not be built | Why this is a position, not a backlog item |
| --- | --- |
| A fifth Doctor | the chain is dataset → experiment → result → paper; a fifth layer would be a scientific claim |
| No global trust score | merging unlike evidence yields a number nobody can falsify or trace |
| A fraud or misconduct detector | requires judging intent and truth; the tools compare declarations to evidence |
| No automatic peer reviewer | reviewing is a scientific act with accountability the tools refuse to take |
| An LLM-as-judge layer | a probabilistic reader cannot be the authority on whether a number matches a number |
| Unbounded PDF understanding | the input contract is the LaTeX source; the tools cannot verify a tree matches a PDF, and pretending otherwise would add a claim, not a feature |
| "Proves reproducibility" wording anywhere | auditing provenance is not reproducing results; see `docs/faq.md` |

## Small follow-up items with no deadline

- **Citation identity.** No `CITATION.cff` exists in any of the four repositories, and author metadata
  disagrees between them (`冯硕` for Dataset Doctor, `beihai` for Experiment Doctor, unset for Result
  Doctor and Paper Doctor). A portal-level citation would require the owner to choose an authoritative
  name; inventing one for the sake of a complete-looking repository is refused. See
  `research/COMPONENT_FACTS.md` §5.
- **Repository descriptions and topics** for the four components, if their owners want them aligned
  with the portal's vocabulary. Documentation-only, owned by each component.
- **A coordination surface** (chat or forum) if and only if someone asks for one with a reason.

## Explicitly not this roadmap

No new scientific phase. No rule additions "for coverage". No performance work without a report of
slowness blocking a real audit. No feature whose justification is that it would look complete.

If a proposal cannot name a person who needs it and an artifact that proves the need, it belongs in
none of these sections.
