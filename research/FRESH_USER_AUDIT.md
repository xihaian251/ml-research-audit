# Fresh-User Proxy Audit (§33)

Measured 2026-09-29, before the portal was published.

## What this method is, and what it is not

Two independent agent simulations of a first-time external user were run in clean temporary
workspaces. Each installed the four packages from PyPI into its own virtualenv and worked only from
the public documentation.

**This is not a human onboarding test.** The distinction is not cosmetic: an agent does not carry
prior context, does not get tired, does not feel the social cost of filing an issue, and does not
have to justify the time spent to a colleague. A simulation measures whether the documentation is
sufficient; it cannot measure whether a person will find it usable.

`status_model.human_onboarding_observed` therefore stays `false`, and
`STACK_STATUS.md` §3 still reads NOT OBSERVED. Nothing in this file changes that.

| | Proxy A | Proxy B |
| --- | --- | --- |
| Starting material | `README.md` only, plus the four public component repos and PyPI | the whole portal as it will appear publicly |
| Question answered | can a stranger reach a first audit from the landing page alone | does the documentation set survive being read as a contract |
| Environment | clean venv, Windows, Python 3.13, no GPU | clean venv, same machine |
| Independence | not shown B's brief or report | not shown A's report |

Every claim below was re-verified by the maintainer before being accepted. Rejected claims are kept
in the record with the measurement that rejected them, because a proxy report is evidence about the
proxy's experience, not about the software.

One provenance caveat about B: its agent process ended with "The connection to the model service was
interrupted" after writing `PROXY_REPORT.md`, so B's whole session was never re-run as a unit. Its
report was treated as a set of claims to measure, not as a transcript to trust, and B2 and B4 were
reproduced individually by the maintainer before anything was edited.

## Proxy A result in one line

From the landing page alone, A installed all four tools, built a 300-row synthetic dataset with a
planted entity leak, a toy training script with a seed, a hand-written Result Doctor manifest, and a
one-table LaTeX paper, and reached a real four-layer trace containing a `PD003 FAIL` — in about 11
minutes and roughly 41 commands. A could not reach a single portal document, because the portal
repository did not exist publicly yet.

## Maintainer re-verification of A's claims

| A-ID | A's claim | Maintainer measurement | Status |
| --- | --- | --- | --- |
| A1 | the portal repo and every document it links are 404 | true at audit time; the repository was unpublished. Addressed by publishing (§35), not by editing | RESOLVED BY LAUNCH |
| A2 | no public document gives a minimal `result-doctor.yml` a stranger can copy for their own project | confirmed. `result-doctor` README:134 ("Writing a manifest") states the three-door contract in prose and then points elsewhere: `src/result_doctor/manifest.py` docstring for the six authoring notes, `phase4/rtdl-revisiting-models/` for a real one, `phase2/...DESIGN.md` for the reasoning. The smallest copyable whole file in public is `tests/generic_fixtures/example_b/result-doctor.yml` (a test fixture) or the 105-line real manifest | ACCEPTED, P1, fixed portal-side |
| A3 | Paper Doctor's documented RD bridge cannot run | confirmed. `paper-doctor` README:380 prints `result-doctor audit <run-dir> --json > findings.json`. `result-doctor audit --help` declares `--json REPORT_JSON` (it takes a value), so the redirect strips the value: reproduced `rc=2`, `error: argument --json: expected one argument`, and the shell left a **0-byte** `findings.json`. The working form is `result-doctor audit <dir> --json findings.json` (`rc=0`, 10,783-byte canonical JSON from the same fixture). `result-doctor` README:115 already uses the correct form | ACCEPTED, P1. The defect is in a frozen child README — recorded, not edited. The portal's own copy of the same broken line was fixed |
| A4 | `result-doctor` README says the package is not on PyPI | confirmed; already census entry **S1**. `pip install result-doctor` installed 0.1.0. A is the first evidence that the stale sentence actively misleads a newcomer rather than merely being wrong | ACCEPTED, P1 (already recorded, severity upgraded by observed impact) |
| A5 | the issue forms A wanted to use do not exist | same cause as A1: unpublished repository | RESOLVED BY LAUNCH |
| A6 | version story is inconsistent across surfaces | confirmed: `experiment-doctor --help` banner reads "Experiment Doctor v0.1" while the distribution is 1.0.0 (census **S2**), and `dataset-doctor-audit` / `experiment-doctor` have no `--version` (rc=2 usage error). A's contribution is that the README table invites verification by `--version`, which two of four tools refuse | ACCEPTED, P2 — portal wording changed to route version checks through `pip show` |
| A7 | the landing page's "it does not produce a verdict for a dataset" conflicts with Dataset Doctor's behaviour | confirmed as a wording defect **in the portal, not in the tool**. Measured: on a synthetic set with 40 shared `patient_id` values, `dataset-doctor-audit audit` printed `FORMAL_EVAL_INVALID` with `1 CRITICAL` (`DD005 Entity leakage … 80 samples`) and exited **1**. Dataset Doctor's own README documents that gate (`audit ./data` fails on a blocking/CRITICAL assertive finding or an `INVALID` verdict; `--ci`, `--strict`, `--fail-on` tighten it). So "no verdict of any kind for a dataset" is too broad; the accurate statement is that no tool emits a *number* that merges findings, and the one categorical gate that exists is about the evaluation boundary, not about data quality | ACCEPTED, P1 (portal overclaim) — README row corrected |
| A8 | the README never tells you to isolate the install | reproduced on this machine: a pre-existing global `dataset-doctor-audit` shadowed the fresh venv, so the first `--help` checked the wrong install. A venv plus `which` check is now in both README and quickstart | ACCEPTED, P2 |
| A9 | "ten-minute onboarding" understates the cost of authoring a Result Doctor manifest | partly accepted. The manifest-authoring cost was not stated anywhere in the portal; it is now quantified (the smallest public whole manifest is 105 lines; the reference real one is 98 content lines). A's supporting comparison (RD's internal report counting 110 logical lines) is a different counting rule, not a contradiction | ACCEPTED, P2 (portal wording) |
| A10 | `dataset-doctor-audit init` hides `--force` from its usage | **rejected.** `dataset-doctor-audit init --help` shows `--force  Overwrite an existing config file.` in the Options panel. A read the one-line `Usage:` header, which never lists options. The re-`init` behaviour it hit (`rc=2`, "already exists (use --force to overwrite)") is correct and self-describing | REJECTED |
| — | A9's "98-line manifest" is wrong (the file is 105 lines) | **rejected as a defect.** Measured on `phase4/rtdl-revisiting-models/result-doctor.yml`: 105 raw lines, 98 non-blank non-comment lines. Both figures are correct under their own counting rule | REJECTED (recorded as a measured nuance) |
| — | `experiment-doctor init --config` cares about the file extension | **rejected.** A `.toml` path was accepted: `configuration.config_files=CONFIRMED` in the produced lock. The tool fingerprints bytes; the extension carries no meaning. (`configuration.config_hash=UNKNOWN` — a config *parser* is a separate matter, and ED does not claim one.) | REJECTED (portal now states it) |
| — | A's step 13 numbers (`rules=6 rule_fail=0 rule_inconclusive=3` for a toy ED project) | consistent with a six-rule subset firing on a lock with no aggregation targets; not published as a portal claim | NOT USED |

## What A got right without being told

Recorded because it is the strongest evidence in this audit: A reached `FORMAL_EVAL_INVALID` on its
own planted leak, reached a `PD003 FAIL` by writing a wrong number into its own `.tex`, and
independently confirmed that `UNKNOWN` stays `UNKNOWN` (`code.commit=UNKNOWN`,
`dataset.fingerprints=UNKNOWN`) rather than being filled in. It also concluded, unprompted, that the
README's line "Independent external users: 0 observed" was "the README's most useful line".

A's own adoption verdict, verbatim in spirit: adopt Dataset Doctor and Experiment Doctor now, use
Result/Paper Doctor for one careful audit, do not cite them in a reproducibility appendix while the
cross-layer contract lives only in test fixtures and a source docstring.

## Proxy B result in one line

B read the portal as it will appear publicly — README plus all nine `docs/` pages plus the two
example directories — and ran the documented commands in its own clean venv. It reached a
`FORMAL_EVAL_INVALID` in about 4–6 minutes, reproduced the Paper Doctor TabM trace byte-for-byte
(its own run emitted digest `08836ccfe17f…`, identical to the shipped file and to the number in
`docs/end-to-end-tabm.md`), and dead-ended at step 2 of that same flagship case study with `rc=2`.
B reported 20 doc statements as verified TRUE and seven defects.

The two proxies are not redundant. A could only see the landing page, because the portal did not
exist publicly when A ran; B could only see the portal, because it was built after A. So A's defects
are mostly component- and landing-page defects and B's are portal defects. Where they converge
independently — the `--json` bridge line (A3 ≡ B1) and the absent minimal manifest (A2 ∩ B3) — the
evidence is stronger than either report alone.

## Maintainer re-verification of B's claims

Every defect below was re-measured directly on this machine; B's version, `--version`, rule-count and
file-size claims were already recorded in `COMPONENT_FACTS.md` §1–§6 before B reported them, and B's
numbers agree with those measurements.

| B-ID | B's claim | Maintainer measurement | Status |
| --- | --- | --- | --- |
| B1 | `end-to-end-tabm.md` step 2 prints `result-doctor audit … --json > /tmp/rd.json`, which is invalid because `--json` takes a value | reproduced `rc=2`, `error: argument --json: expected one argument`, and the redirect leaves a 0-byte file. Same defect A found independently from the Paper Doctor README (A3, census **S4**) | ACCEPTED, P1 — fixed portal-side; the frozen child README line is recorded, not edited |
| B2 | step 2 cannot run in a fresh checkout: the manifest's `root: ../../../upstream/tabm/paper` points at a tree no documented step creates (step 4 cloned TabM to `./tabm`) | reproduced failure-first on a clean clone: `rc=2`, `E_ROOT at root: …\upstream\tabm\paper is not a directory`. After cloning TabM to the sibling `upstream/tabm` at the pinned commit, `result-doctor` exited 0 with 14 findings and digest `c56b6262…` (12,392 B), and Paper Doctor exited 0 with digest `08836ccfe17f…` and counts 10/2/5/14/1 — both exactly the published numbers | ACCEPTED, P1 — the single highest-value finding of this audit. Case study rewritten with the layout stated, an ASCII tree, and the commit pinned |
| B3 | the only runnable Result Doctor manifest in public is a test fixture; RD ships no `examples/`, no `demo`, no `init` | confirmed. Same gap as A2, reached from the other direction. Fixed by `examples/minimal-result-manifest/`, which the quickstart now runs before pointing readers at the fixture | ACCEPTED, P1 (portal) |
| B4 | the case study's prose says "the two FAIL findings" while its own step-3 report contains two **paper-layer** FAILs — `PD003 C8` and `PD006 C2` — so one FAIL is silently dropped | confirmed from the findings JSON of my own run: `PD006` fails on C2 with `the reference resolves to table:5, which does not print 8; it is printed in table:4, table:7, table:9, table:11, table:14, table:15, table:16, table:17`. The chain has three FAILs, not two | ACCEPTED, P2 — heading, chain table, a new PD006 subsection and the FAQ answer corrected |
| B5 | the quickstart trains the reader that a scientific FAIL yields exit 0, but `dataset-doctor-audit audit` exits 1 on blocking findings; the demo-vs-audit difference is never stated | reproduced: `audit` on the leaky fixture `rc=1`, on the clean fixture `rc=0`, while `demo` prints the same `FORMAL_EVAL_INVALID` and exits `0` | ACCEPTED, P2 — three-row measured table now in the quickstart and in `status-semantics.md` §5 |
| B6 | `component-guide.md` says "commands measured from `--help`" and lists 10, omitting `split` | confirmed against the tool's own `--help` (11 commands). My list had been wrong in exactly the way the portal criticises | ACCEPTED, P3 — corrected |
| B7 | step 4's `--dataset <your official adult copies>` is an unfilled placeholder, and a nonexistent `--dataset` path exits 0 with `dataset.fingerprints=UNKNOWN` rather than erroring | confirmed: `experiment-doctor init` with a bogus path exited 0; the failure is silent by design (see `COMPONENT_FACTS.md` §7.4) | ACCEPTED, P3 — placeholder expanded and the silent-degradation warning added to the case study |

### What B contributed that A did not

Two things. The `E_ROOT` layout gap (B2) is only findable by someone who actually runs the case study
top to bottom on a clean machine, and it is the defect that made the portal's flagship document
non-executable at its second command. And B ran the negative test on the cross-layer contract: it
corrupted one byte of the shipped `phase3/tabm/findings.json`, re-ran `paper-doctor audit`, and got
`rc=2` with `P_UNRESOLVED_REF … declared sha256 c56b6262… does not match observed e15d56…`. That is
the first external confirmation that `architecture.md`'s claim — the Paper Doctor manifest verifies
the Result Doctor digest as it parses — is machine-enforced rather than descriptive. The file was
restored and re-verified.

B also recorded, unprompted, the same anti-overclaim judgement A reached: it searched for a sentence
asserting more than the shown evidence and reported that it could not find one, while naming
under-communication as the real weakness.

## Merged defect register

Thirteen defects accepted (five P1, five P2, three P3), three claims rejected, zero P0.

| Defect | Found by | Sev | Disposition |
| --- | --- | --- | --- |
| `--json > file` bridge line | A3, B1 independently | P1 | **Recorded, not fixed here** (frozen child README, census S4 / STACK_STATUS row 7); portal's own copies of the line fixed |
| Undocumented `upstream/tabm/paper` layout | B2 | P1 | **Fixed** — case study steps renumbered, layout stated, commit pinned, expected digests published |
| No copyable minimal `result-doctor.yml` | A2, B3 | P1 | **Fixed** — `examples/minimal-result-manifest/` with both variants re-run and their outputs recorded |
| README's "no verdict for a dataset" is too broad | A7 | P1 | **Fixed** — row scoped, and DD's measured `FORMAL_EVAL_*` gate now stated explicitly |
| RD README says the package is not on PyPI | A4 (census S1) | P1 | **Recorded** — owned by a RD release; cannot be fixed in this repository |
| `demo` exits 0 while `audit` exits 1 on the same content | B5, and A's exit-code surprises | P2 | **Fixed** — measured three-surface table in quickstart and status semantics |
| `PD006 FAIL` on C2 missing from the case study prose | B4 | P2 | **Fixed** — chain table, new subsection, FAQ, "three genuine inconsistencies" |
| Version story inconsistent; two tools refuse `--version` | A6, B | P2 | **Fixed** in wording (README routes verification through `pip show`); the underlying banner and missing flags are STACK_STATUS rows 2 and 4 |
| No instruction to isolate the install | A8 | P2 | **Fixed** — venv + `which` check in README and quickstart |
| Manifest-authoring cost never quantified | A9, B3 | P2 | **Fixed** — the smallest public whole manifest is now named and counted |
| `component-guide.md` command list incomplete | B6 | P3 | **Fixed** |
| `--dataset` placeholder unfilled; bad path degrades silently | B7 | P3 | **Fixed** |
| ED adapter `KeyError` traceback instead of a usage error | maintainer (§7.4) | P3 | **Recorded** — STACK_STATUS row 9, ROADMAP follow-up |
| "`init` hides `--force`" | A10 | — | **Rejected** — `--force` is printed in `init --help` |
| "98-line manifest" | — | — | **Rejected as a defect** — 105 raw, 98 content lines; both correct |
| "ED `--config` cares about the extension" | — | — | **Rejected** — a `.toml` path was accepted; the tool fingerprints bytes |

A note on the ratio: of A's ten numbered claims plus two further observations, three were disproofed;
of B's seven defects, none were. That is not evidence that B was more careful. B's brief was the
finished portal, whose statements are already measured; A's brief was a landing page plus four foreign
repositories, which forced more inference. Rejections are kept in the register because a proxy report
is only evidence about the proxy's experience until the maintainer measures it.

## What both proxies left unmeasured

Neither proxy is a human, and both were run by me on one Windows machine with Python 3.13 and no GPU.
Nothing here changes `STACK_STATUS.md` §3: `human_onboarding_observed` stays `false`, and the human
first-use requirement stays open for the 0.1.x line.

The list of what a real stranger would still have to discover alone did shrink, but it is not empty.
Both proxies audited other people's fixtures. Neither could tell whether someone with a real project,
real deadlines, and no interest in this toolchain would find the manifest authoring worth the cost —
that is an adoption question, and adoption is measured by issues, PRs, and external case studies,
none of which exist yet.
