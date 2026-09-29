# Umbrella launch report

Measured 2026-09-29. This is the record of one round of work: turning four already-released tools
into one navigable project. It is not a scientific result, and it claims none.

Every number below was measured on this machine against public infrastructure, or is copied from a
file that records such a measurement. Where the round changed a position because evidence contradicted
it, that is stated rather than smoothed over.

The authoritative answer to "what is the final commit" is `git log -1 --format=%H` on `main`. This
file is added by the launch round's last commit, so it cannot contain its own SHA; the state that CI
verified before publication was `71836efb`.

## 1. Project identity

| Field | Value | Source |
| --- | --- | --- |
| Display name | ML Research Audit | `stack.yaml project.name`, README first line |
| Repository | `xihaian251/ml-research-audit` | GitHub REST, created 2026-09-29T14:16:35Z |
| URL | https://github.com/xihaian251/ml-research-audit | same |
| Tagline | End-to-end provenance auditing for machine-learning research | README |
| GitHub description | `End-to-end provenance auditing for machine-learning research: dataset → experiment → result → paper claim.` | repository API, read back after the write |
| Default branch | `main` | repository API |
| Visibility | public | repository API |
| Topics | data-quality, machine-learning, open-science, provenance, reproducibility, research-software, scientific-computing | `/topics` API, read back |
| Umbrella PyPI distribution | none, by design | `stack.yaml project.pypi: null`, enforced by `verify_stack.py` |

Two of the nine recommended topics were not used: `mlops` and `experiment-tracking`. Neither describes
what these tools do — they audit declared provenance, they do not operate models or track runs, and
tracker integration sits in `ROADMAP.md` under LATER. §30 of the brief says to use only topics that
accurately describe the project, so the omission is the instruction being followed, not ignored.

## 2. Component facts

All four components are released, published through GitHub Actions OIDC trusted publishing, and frozen.

| Component | Layer | PyPI | Version | CLI | Tag | Release commit |
| --- | --- | --- | --- | --- | --- | --- |
| Dataset Doctor | dataset | `dataset-doctor-audit` | 0.1.2 | `dataset-doctor-audit` | `v0.1.2` | `107504ed…` |
| Experiment Doctor | experiment | `experiment-doctor` | 1.0.0 | `experiment-doctor` | `v1.0.0` | `fb3a2420…` |
| Result Doctor | result | `result-doctor` | 0.1.0 | `result-doctor` | `v0.1.0` | `bec3ab98…` |
| Paper Doctor | paper | `paper-doctor` | 0.1.0 | `paper-doctor` | `v0.1.0` | `2a026986…` |

Verified again at launch, after the audit fix pass: `verify_stack.py --online` returned 0 with all four
versions equal to PyPI, and the four tags still resolve to exactly the commits above
(`/repos/<component>/tags`, read 2026-09-29). Rule counts are DD001–DD021, ED001–ED010, RD001–RD008,
PD001–PD007, each measured from the installed CLI. Full source-authority trail:
[`COMPONENT_FACTS.md`](COMPONENT_FACTS.md).

## 3. Repository structure

33 tracked files, 19 of them Markdown, 9 YAML.

```
README.md  LICENSE  CONTRIBUTING.md  CODE_OF_CONDUCT.md  SECURITY.md
ROADMAP.md  STACK_STATUS.md  stack.yaml
docs/      architecture quickstart component-guide evidence-model
           status-semantics end-to-end-tabm faq community
examples/  tabm-chain/README.md
           minimal-result-manifest/  (added by the audit fix pass)
.github/   ISSUE_TEMPLATE/{bug,documentation,onboarding-case,feature}.yml + config.yml
           PULL_REQUEST_TEMPLATE.md  workflows/portal-checks.yml
scripts/   verify_stack.py
research/  COMPONENT_FACTS.md  FRESH_USER_AUDIT.md  UMBRELLA_LAUNCH_REPORT.md
```

The structure followed §6 as written, with two additions, both consequences of measurement rather than
decoration: `examples/minimal-result-manifest/` (the gap both proxies hit independently) and
`research/FRESH_USER_AUDIT.md` (the §33 deliverable). `CITATION.cff` was deliberately not created: no
authoritative citation identity exists, the four component repositories disagree about author metadata
(`冯硕` / `beihai` / unset / unset), and §24 forbids inventing one to look complete.

## 4. Architecture

The portal is a routing and identity layer. No submodule, no vendored source, no meta-package, no
shared library. Each layer's rules stay in the repository that released them, and the portal's only
executable code is a read-only verifier.

Certainty does not increase across layers, and the architecture document says so in the same breath as
it names the one machine-checked cross-layer link: the Paper Doctor manifest pins the Result Doctor
findings file by path, sha256, size and `rd_version`, and refuses to run if a byte differs. Everything
else in the chain — dataset fingerprint to run, run to reported result, result to claim — is a human
declaration. That asymmetry is stated in `docs/architecture.md` and was independently confirmed during
the audit, not asserted.

## 5. Quickstart validation

`docs/quickstart.md` was executed as written by Proxy B in a clean virtualenv and by the maintainer in
the fix pass: four packages install side by side with no resolver conflict, every documented command
runs, and every documented output matched, including the three quirks the page pre-announces
(`experiment-doctor --help` prints "v0.1" while the distribution is 1.0.0; `python -m paper_doctor`
exits 1; Dataset Doctor and Experiment Doctor have no `--version`).

After the audit the page also states what "quickstart" covers (4–6 minutes to a dataset-layer result,
10–15 minutes to one audit per layer from shipped fixtures) and what it does not (an audit of your own
number, which requires manifest authoring). The Result Doctor section now runs the portal's own minimal
manifest before sending readers to a test fixture.

## 6. TabM case study

`docs/end-to-end-tabm.md` traces claims from TabM (arXiv:2410.24210) through all four layers and
records three genuine inconsistencies plus eight `UNKNOWN` states.

The audit changed two things here, both because measurement demanded it:

- **It was not executable at step 2.** The manifest's `root: ../../../upstream/tabm/paper` resolves to a
  sibling tree that no documented step created; a clean run failed with `rc=2`,
  `E_ROOT … is not a directory`. The page now states the required layout, pins the TabM commit, and
  publishes both findings digests. Steps 1–5 were then re-executed on Windows, Python 3.13, against the
  published wheels on 2026-09-29, reproducing `c56b6262…` (12,392 bytes, 14 findings: 1 PASS,
  6 INCONCLUSIVE, 6 NOT_APPLICABLE, 1 NOT_RUN) and `08836ccfe17f…` (32 claims: 10 PASS, 2 FAIL,
  5 INCONCLUSIVE, 14 NOT_APPLICABLE, 1 NOT_RUN).
- **It undercounted its own findings.** The prose said "the two FAIL findings" while the paper layer
  produced two FAILs of its own (`PD003` on C8, `PD006` on C2) plus `DD009` at the dataset layer. The
  chain has three. `PD006` is now quoted with its measured reason string.

There is no unsupported closure in the case study. Step 5 cannot be repeated by a third party without
supplying their own Adult copy, and the page says so and explains that a different fingerprint means the
Dataset Doctor findings are about *their* copy — which is what the fingerprint is for.

## 7. Community surface

`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `docs/community.md`,
`PULL_REQUEST_TEMPLATE.md`, and four issue forms. The forms cover bug, documentation, feature, and the
type this project values most: an external onboarding report / case study, which asks for the commands
run in order, the moments of hesitation, the status mix returned, what was initially misread, and
whether the report may be published. The feature form asks the four mandated questions and states which
categories of request will be closed with a link to the design docs.

Contact links route each component's issues to its own repository; `portal-checks.yml` fails if any of
the four names disappears from `.github/`.

Three issues were opened at launch, all real backlog rather than decoration:

1. second independent end-to-end acceptance, on a project none of us authored;
2. real first-time human onboarding, still NOT OBSERVED;
3. Paper Doctor ships no copyable minimal manifest for your own paper (the Result Doctor gap closed in
   this round; the paper layer's is still open, with the wheel contents measured).

Two labels were created to match the `onboarding-case` form, which references `onboarding` and
`case study`.

## 8. CI

`.github/workflows/portal-checks.yml`, five jobs, all measured rather than assumed:

| Job | Checks |
| --- | --- |
| stack metadata × Python 3.11 / 3.12 / 3.13 | `verify_stack.py` (structure, invariants, file set, publication wording), every YAML parses and issue forms are well-formed, all four components appear in `.github/` |
| versions still match PyPI | offline gate, then `--online` against the PyPI JSON API |

First run on the pushed default branch: `36581488894`, completed, `success`, every step in all five
jobs green, read job by job rather than by the run conclusion. The workflow is offline by default so a
PyPI outage cannot make the portal look broken, and a daily scheduled run re-measures versions; drift
there means the census is stale, and the script says exactly that instead of guessing.

## 9. Fresh-user audit

Two independent agent simulations in clean virtualenvs, recorded in [`FRESH_USER_AUDIT.md`](FRESH_USER_AUDIT.md).

Proxy A worked from the landing page plus the four public repositories before the portal existed and
reached a real four-layer trace containing a `PD003 FAIL` in about 11 minutes across ~41 commands.
Proxy B read the portal as it will appear publicly, reproduced the Paper Doctor trace byte-for-byte,
and dead-ended at step 2 of the flagship case study.

Result: 13 accepted defects (5 P1, 5 P2, 3 P3), 3 claims disproved by measurement and kept in the
record, 0 P0. Every accepted claim carries the maintainer's own command and output. All portal-side
fixes shipped in this round; nothing was edited in a component repository.

## 10. Known limitations

- **Adoption is zero.** One author, no external user observed. The portal's honest description of
  itself is four released tools, one documented trace, and nobody else seen using them.
- **One acceptance run**, on one project, chosen by the person who built the tools.
- **Result Doctor and Paper Doctor determinism** is measured complete for Paper Doctor (its TabM digest
  reproduced on seven independent routes); Result Doctor's contribution to the same trace is digest-pinned
  inside the Paper Doctor manifest, not independently re-measured seven ways.
- **Windows coverage asymmetry**: Dataset Doctor and Paper Doctor are CI-verified on Windows; Experiment
  Doctor and Result Doctor are not, though every path this round documented was executed successfully on
  Windows. "Unverified by CI" is not "known-bad", and the docs now say it that way.
- **Four defects cannot be fixed in this repository** (STACK_STATUS rows 1, 2, 7, 9): they live in frozen
  child READMEs and CLIs and need a release there.
- **Manifest authoring cost remains real.** The portal now quantifies it and ships one minimal example at
  the result layer; the paper layer still has none (issue #3).

## 11. Current external-adoption status

| Axis | State |
| --- | --- |
| Independent external users | 0 observed |
| Issues or PRs from anyone other than the author | 0 (all three open issues were filed by the author at launch) |
| Downloads / stars / citations | not reported; no baseline exists |
| Real human first-use test | **NOT OBSERVED**, for all four components |
| Agent-driven onboarding simulation | OBSERVED twice, 2026-09-29, and recorded as a simulation |
| `human_onboarding_observed` in `stack.yaml` | `false`, enforced by `verify_stack.py` |

Paper Doctor's waived human-test requirement is a documented risk acceptance, not a passed gate, and the
portal says so in `STACK_STATUS.md` §3. An agent that reaches a verdict in eleven minutes is a
defect-finding instrument; it is not a user study, and nothing in this round converts one into the other.

## 12. Child repository write count: exactly zero

Evidence, read 2026-09-29 after publication:

| Repository | Remote HEAD | Last push | Tag SHAs | Local clone |
| --- | --- | --- | --- | --- |
| dataset-doctor | `3241a7cb` | 2026-09-25T16:24:23Z | v0.1.0/v0.1.1/v0.1.2 | none on this machine |
| experiment-doctor | `3d1adc2e` | 2026-09-27T15:15:55Z | v0.1.0→`7c9e5506`, v1.0.0→`fb3a2420` | not a git checkout here |
| result-doctor | `1a7bc184` | 2026-09-28T13:54:04Z | v0.1.0→`bec3ab98` | tracked files: 0 modified; 7 untracked files, all dated 2026-09-28 (pre-existing release notes, left untouched) |
| paper-doctor | `ad733893` | 2026-09-29T10:50:10Z | v0.1.0→`2a026986` | working tree clean, 0 modified |

Every last-push timestamp precedes this round's start (~2026-09-29 11:54Z), and every frozen tag still
resolves to the census release commit. `v0.1.0` was never moved. Cross-links from child READMEs into
this portal are recorded as a future docs-only action for each component's owner, and were not made.

## 13. Remaining P0

None. No blocking defect was found in the portal, and none of the accepted defects was P0.

## 14. Remaining P1

Two, both outside this repository's authority, both recorded rather than patched:

| # | Defect | Owner |
| --- | --- | --- |
| 1 | Paper Doctor `README.md:380` documents the RD bridge as `result-doctor audit <run-dir> --json > findings.json`. `--json` takes a value, so the documented command exits 2 and leaves a 0-byte file. Identical at `v0.1.0` and at `HEAD`. Census entry S4, `STACK_STATUS.md` §4 row 7. | a Paper Doctor release |
| 2 | Result Doctor `README.md` states the package is not published to PyPI. It has been since 2026-09-28, and `pip install result-doctor` installs 0.1.0. Census entry S1, `STACK_STATUS.md` §4 row 1. | a Result Doctor release |

The portal's own copies of both statements are correct, and the quickstart now shows the working bridge
command with its measured `rc`.

## 15. Accepted P2 and P3

All shipped in this round unless marked recorded.

| Sev | Defect | Disposition |
| --- | --- | --- |
| P2 | `demo` exits 0 while `audit` exits 1 on identical blocking content; the reader who learns the contract from the demo learns it wrong | measured three-surface table in quickstart and `status-semantics.md` §5 |
| P2 | `PD006 FAIL` on C2 missing from the case study prose, which said "two FAIL findings" where the chain has three | chain table, new subsection with the measured reason string, FAQ corrected |
| P2 | version story inconsistent across surfaces; two tools refuse `--version` | README routes verification through `pip show`; underlying flags are STACK_STATUS row 4 |
| P2 | no instruction to isolate the install | venv plus `which` check in README and quickstart (a global `dataset-doctor-audit` was observed shadowing a fresh venv on this machine) |
| P2 | manifest-authoring cost never stated | quantified, and a copyable example now exists at the result layer |
| P3 | `component-guide.md` command list omitted `split` | corrected to the 11 commands the tool prints |
| P3 | `--dataset <placeholder>` unfilled; a nonexistent path exits 0 with `fingerprints=UNKNOWN` | placeholder expanded, silent degradation documented |
| P3 | `experiment-doctor --adapter <unknown>` raises a bare `KeyError` traceback | recorded (STACK_STATUS row 9, ROADMAP follow-up); no component code changed |

## 16. What the round cost, and what it did not do

Eight commits on `main`, history linear: four built the portal (census and metadata, documentation and
the TabM trace, community surface, CI), then the census addendum, the documentation fix pass, the audit
record, and this report. No force push, no rewrite, no micro-commit per file.

The round added no rule, no adapter, no fifth tool, no global score, no paper verdict, no misconduct
detector, no language model acting as a judge of evidence, and no claim that the stack proves a paper
true. It also did not start a development phase; §43's list of what comes next is community work, not
engineering work.

## 17. Next step, uniquely

Post the launch where the tools are actually used, then wait for the first report from someone who did
not build them. Specifically: ask one external researcher to run one four-layer trace on a project none
of us authored and to file it through the `onboarding-case` form — because the only metric this roadmap
cares about is external adoption, and no further portal work can produce it.
