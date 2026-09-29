# Stack status

Measured 2026-09-29. Three different axes are reported separately, because conflating them is
exactly the failure mode this project exists to avoid.

## 1. Component release status

| Component | PyPI | Version | Tag | Release commit | Cross-platform CI |
| --- | --- | --- | --- | --- | --- |
| Dataset Doctor | `dataset-doctor-audit` | 0.1.2 | `v0.1.2` | `107504ed7d2f0caffea9dbc28ec25225a532fdb0` | ubuntu + windows × 3.11/3.12/3.13 |
| Experiment Doctor | `experiment-doctor` | 1.0.0 | `v1.0.0` | `fb3a24200a56724816906018a60c4a54b6149ab1` | Linux only × 3.11/3.13 |
| Result Doctor | `result-doctor` | 0.1.0 | `v0.1.0` | `bec3ab98e5289d4739d57c34413a7a4d2b687da0` | Linux only × 3.11/3.13 |
| Paper Doctor | `paper-doctor` | 0.1.0 | `v0.1.0` | `2a02698637f35bd3fec28d98a8b6e272b8e1fc9a` | ubuntu + windows × 3.11/3.13 |

All four published through GitHub Actions OIDC trusted publishing. No long-lived PyPI token exists
for any of them. Sources: `research/COMPONENT_FACTS.md`, which cites the PyPI JSON API, the GitHub
tags and releases APIs, and the workflow files in each repository.

**The four tags are frozen.** `v0.1.0`, `v0.1.2` and `v1.0.0` are not moved, and this portal has no
authority to move them.

## 2. Scientific core status

| Axis | State | Evidence |
| --- | --- | --- |
| Layer boundaries and rule sets | COMPLETE | DD001–DD021, ED001–ED010, RD001–RD008, PD001–PD007, each measured from the installed CLI |
| Determinism of the outputs | Measured complete for Paper Doctor: byte-identical canonical JSON output, and its frozen TabM findings digest `08836ccfe17f3e2d…` reproduced on seven independent routes, including a PyPI-installed package. Result Doctor's contribution to the same trace is digest-pinned inside the Paper Doctor manifest rather than independently re-measured seven ways. | Paper Doctor `release/RELEASE_FREEZE.md`, `release/ML_RESEARCH_FINAL_STATE.md` |
| Cross-layer joins | DECLARED, NOT INFERRED — by design | `docs/architecture.md`, `docs/evidence-model.md` |
| End-to-end acceptance on a third-party project | COMPLETE once | TabM (arXiv:2410.24210), `docs/end-to-end-tabm.md` |
| Coverage of the acceptance | Three chains, one of them four layers deep | the frozen chain ledger in the Paper Doctor repository |
| Independent replications of that acceptance by others | NOT OBSERVED | none reported |

One acceptance run on one public project is a demonstration, not a validation programme. The stack's
claim is "we traced one real paper claim to one real dataset and recorded every gap", and that is
precisely what the case study shows.

## 3. Community and adoption status

| Axis | State |
| --- | --- |
| Independent external users | **0 observed** |
| Issues or PRs from anyone other than the author | 0 (measured: `open_issues_count = 0` on all four repositories) |
| Downloads, stars, citations | deliberately not reported — no baseline exists yet |
| Real human first-use test of Paper Doctor | **NOT OBSERVED** |
| Real human first-use test of the other three | NOT OBSERVED |
| Agent-driven onboarding simulation | OBSERVED, and it is not the same thing as a human test |
| Fresh-user proxy audit of this portal | OBSERVED twice, 2026-09-29, in clean environments — see `research/FRESH_USER_AUDIT.md`. Both agents were instructed to use only public documentation; the portal itself was still unpublished at that moment, so neither read the documents under test. The findings that survived re-measurement are documentation fixes, not evidence about humans. |

An agent reading a README cold is a defect-finding instrument, not a user study. It does not carry
the prior context this project's author unavoidably carries, which is the only reason the run is
worth anything. It also gets things wrong in ways a human would not: three of its reported defects
were disproofed by direct measurement before publication
(`research/COMPONENT_FACTS.md` §7.3). `human_onboarding_observed` stays `false` in `stack.yaml`, and
no amount of agent onboarding changes that field.

### The Paper Doctor §15 fact, stated exactly

Paper Doctor's Phase 3 brief required a real human first-use test before release. No human tester
took one. The owner waived that requirement for 0.1.0 on 2026-09-29. The consequence of the waiver
is a documented risk acceptance, not a passed gate:

- the record reads **NOT OBSERVED**, with all thirteen measured quantities `UNKNOWN`;
- no release document claims a human test anywhere;
- an automated agent onboarding simulation was run, and it is recorded as an agent simulation;
- the requirement stays open for the 0.1.x line.

This paragraph exists because "waived" is easily misread as "satisfied". It was not.

### What this project will not claim

No mature adoption. No user base. No "trusted by". The honest description of the current state is:
four released tools, one documented end-to-end trace, and nobody outside the author has been
observed using them.

## 4. Known defects carried into this round

Nothing in this list was fixed, because the four component repositories are read-only for this round.
None of them is a scientific defect; all of them are documentation or metadata drift.

| # | Component | Defect | Class |
| --- | --- | --- | --- |
| 1 | Result Doctor | README states the package is not on PyPI. It has been since 2026-09-28. | P2 documentation |
| 2 | Experiment Doctor | Shipped `--help` says "v0.1" while the distribution is 1.0.0. | P3 cosmetic |
| 3 | Experiment Doctor, Result Doctor | CI does not run on Windows, so Windows behaviour is unverified rather than known-bad. | P2 coverage |
| 4 | Dataset Doctor, Experiment Doctor | No `--version` flag. | P3 usability |
| 5 | All four | No `CITATION.cff`; author metadata disagrees (`冯硕` / `beihai` / unset / unset). | P2 governance |
| 6 | Experiment Doctor, Result Doctor, Paper Doctor | No `CONTRIBUTING.md`, `SECURITY.md`, or `ROADMAP.md` in the component repositories. | P2 community |
| 7 | Paper Doctor | `README.md:380` prints the cross-layer bridge as `result-doctor audit <run-dir> --json > findings.json`. `--json` takes a value, so the command exits `2` and the redirect leaves a **0-byte** `findings.json`. Present identically at tag `v0.1.0` and at `HEAD`, and contradicted by the same README's own line 139, which uses `--json report.json`. | **P1 documentation** — it breaks the only documented path from layer 2 to layer 4 |
| 8 | Dataset Doctor | Three exit-code surfaces disagree with each other: `audit` on a leaking fixture returns `1`, `audit` on the control returns `0`, and `demo` returns `0` while printing `FORMAL_EVAL_INVALID` for that same leaking fixture. A reader who learns the contract from the demo learns it wrong. | P2 documentation (the behaviour itself is defensible; the discoverability is not) |
| 9 | Experiment Doctor | `audit --adapter <unknown>` exits `1` with a bare `KeyError` traceback instead of a `2`-class usage error. The message does name the five valid adapters, so it is recoverable. | P3 usability |

Row 3 deserves a correction from this round's own measurements, because "unverified" is now too weak
a word. Every CLI command quoted in `docs/quickstart.md` and `docs/end-to-end-tabm.md` was executed
on Windows 10 with Python 3.13 on 2026-09-29, including `result-doctor audit`, `paper-doctor audit`,
`experiment-doctor audit`, and both Dataset Doctor exit-code branches in row 8. So Windows behaviour
is **observed and working for those paths** while still being **unverified by CI** — which is a
different gap: the components' own test suites do not run there, so a future release could regress
without anything catching it. That is a coverage gap, not a known-bad.

Rows 1, 2, 7 and 9 are the four items that belong in a component release and cannot be fixed here.
Each is owned by the corresponding component repository. This portal reports them; it does not patch
them.

## 5. What would change this page

| New state | Requires |
| --- | --- |
| adoption "early" → "used" | an issue, PR, or case study from someone outside the author |
| human onboarding observed | a real person, unassisted, completing an audit, with their record kept verbatim |
| a defect closed | a commit and release in the owning component repository |
| a second end-to-end acceptance | a trace through all four layers on a project none of us authored |
