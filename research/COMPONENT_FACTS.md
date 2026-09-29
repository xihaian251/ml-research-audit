# Component facts census

Closed: 2026-09-29. This file is the **only** permitted source of version, package, CLI and
status facts for the umbrella repository's public documentation. Every fact below carries the
source it was measured from. Nothing here was copied from a README's release wording.

This census was run **read-only**. No child repository, tag, release, package or file was
modified in producing it.

## 0. Measurement environment and source hierarchy

| Item | Value | Source |
| --- | --- | --- |
| Date of all measurements | 2026-09-29 (UTC) | this session |
| Machine | Windows 10.0.26200, x64 | `ver` of the measuring host |
| Interpreter used for install/CLI measurements | Python 3.13.1, pip 24.3.1 | `python -V`, `pip --version` in the measurement venv |
| Measurement venv | single fresh venv with all four packages installed together | `python -m venv` + `pip install dataset-doctor-audit==0.1.2 experiment-doctor==1.0.0 result-doctor==0.1.0 paper-doctor==0.1.0` |

Source authority, highest first, as used throughout:

1. **PyPI JSON API** — `https://pypi.org/pypi/<name>/json` (name, version, files, sizes, SHA256,
   `Requires-Python`, `License-Expression`, upload time).
2. **The published wheel** — `entry_points.txt` and `METADATA` read out of the downloaded `.whl`
   (this is the authoritative source of the CLI command name).
3. **GitHub REST API** — `/repos/...` (default branch, license, description),
   `/repos/.../releases/latest`, `/repos/.../tags`, `/repos/.../git/matching-refs/tags/`,
   `/repos/.../actions/workflows` (workflow name, path, state).
4. **`--help` / `--version` of the installed console scripts** (the actual user-facing surface).
5. **Repository file tree** — `/repos/.../git/trees/HEAD` (which community files exist).
6. **README** — used only for the responsibility statements, and **never** for a version,
   install command or release claim where it conflicts with 1–4. Two conflicts were found; see §4.

## 1. The four components as measured

### 1.1 Dataset Doctor

| Field | Measured value | Source |
| --- | --- | --- |
| Repository URL | https://github.com/xihaian251/dataset-doctor | GitHub `/repos/xihaian251/dataset-doctor` |
| Default branch | `main` | same |
| Latest GitHub Release | `v0.1.2`, published 2026-09-25T15:53:01Z, 0 assets | `/releases/latest` |
| Tags | `v0.1.2`→`107504ed7d2f…`, `v0.1.1`→`6ba94129566b…`, `v0.1.0`→`31200147cc8c…` | `/tags` (annotated tag objects `8d4c329aa08b`, `ae03c28ece76`, `1886f449bcdb` per `/git/matching-refs/tags/`) |
| PyPI name | `dataset-doctor-audit` | PyPI JSON |
| Latest published version | `0.1.2` (all releases: 0.1.0, 0.1.1, 0.1.2; not yanked) | PyPI JSON `info.version`, `releases`, `yanked` |
| Wheel | `dataset_doctor_audit-0.1.2-py3-none-any.whl`, 146,928 B, SHA256 `3d7c73572d09985715de8af51dbe9e45c266a1dcee3829f823fc89dc084a9f1d`, uploaded 2026-09-25T16:01:20Z | PyPI JSON `releases['0.1.2']` |
| sdist | `dataset_doctor_audit-0.1.2.tar.gz`, 440,442 B, SHA256 `d785c10a2f5f6f04d57d64a0d955e4c2afe386a81133517029900342a8f82ecb` | same |
| CLI command | `dataset-doctor-audit` → `dataset_doctor_audit.cli:main` | `entry_points.txt` inside the published wheel |
| Python requirement | `>=3.11` | wheel `METADATA: Requires-Python` |
| License | Apache-2.0 | wheel `METADATA: License-Expression` + GitHub `/repos` license `spdx_id` |
| Import package | `dataset_doctor_audit` | wheel contents |
| Runtime dependencies | numpy≥1.26, pandas≥2.2, pillow≥10.2, pyarrow≥15.0, pydantic≥2.7, pyyaml≥6.0, rich≥13.7, scipy≥1.11, typer≥0.12 | PyPI JSON `info.requires_dist` (non-extra entries) |
| Rule registry | DD001–DD021 (21 rules counted in CLI output) | `dataset-doctor-audit rules` in the measurement venv |
| Subcommands | `init`, `scan`, `audit`, `fingerprint`, `snapshot`, `diff`, `report`, `rules`, `demo`, `show` | `dataset-doctor-audit --help` |
| `--version` flag | **does not exist** — `dataset-doctor-audit --version` prints a Typer usage error | measured |
| Built-in demo | **yes** — `demo` generates planted-fault datasets and audits them; measured exit code 0 on Windows/Python 3.13 | `dataset-doctor-audit demo` run in a temp dir |
| GitHub Actions | 3 active workflows: CI (`.github/workflows/ci.yml`), Publish to PyPI, Publish to TestPyPI | `/actions/workflows` |
| CI matrix | ubuntu-latest × windows-latest × Python 3.11/3.12/3.13 | `.github/workflows/ci.yml` |
| Community files present | `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`, `CHANGELOG.md`, `docs/`, `examples/` (no `CITATION.cff`) | `/git/trees/HEAD` + raw fetch of `CITATION.cff` → 404 |
| Author metadata | PyPI `author = 冯硕` | PyPI JSON `info.author` (read as UTF-8; a cp936 console mangles it) |
| Repo description | "Dataset Doctor — Detect data leakage before it corrupts your ML experiment." | `/repos` `description` |
| README release wording | **Current.** States 0.1.2 on PyPI and warns that `pip install dataset-doctor` is a different tool | `README.md` lines 98–124 |

### 1.2 Experiment Doctor

| Field | Measured value | Source |
| --- | --- | --- |
| Repository URL | https://github.com/xihaian251/experiment-doctor | `/repos/xihaian251/experiment-doctor` |
| Default branch | **`master`** | same |
| Latest GitHub Release | `v1.0.0`, published 2026-09-27T13:32:34Z, 2 assets (`experiment_doctor-1.0.0-py3-none-any.whl`, `.tar.gz`) | `/releases/latest` |
| Tags | `v1.0.0`→`fb3a24200a56…`, `v0.1.0`→`7c9e5506efec…` (annotated objects `6e85a56a6609`, `b13aae2e0b2e`) | `/tags`, `/git/matching-refs/tags/` |
| PyPI name | `experiment-doctor` | PyPI JSON |
| Latest published version | `1.0.0` (all releases: 0.1.0, 1.0.0) | PyPI JSON |
| Wheel | `experiment_doctor-1.0.0-py3-none-any.whl`, 132,523 B, SHA256 `2bf8aa04a3b1ee8f065ea9d4c0a79cd13c958b75a7bdd36941e7bcb6705a56b2`, uploaded 2026-09-27T13:33:49Z | PyPI JSON |
| sdist | `experiment_doctor-1.0.0.tar.gz`, 144,788 B, SHA256 `6c4606aeb278949ca59f3ea9b0b2aeee88ad7039eda991b8d5d436fec83eda24` | same |
| CLI command | `experiment-doctor` → `experiment_doctor.cli:main` | `entry_points.txt` in the published wheel |
| Python requirement | `>=3.11` | wheel `METADATA` |
| License | Apache-2.0 | wheel `METADATA` + `/repos` license |
| Runtime dependencies | pydantic≥2.5, typer≥0.12, PyYAML≥6.0 | PyPI JSON `requires_dist` |
| Rule registry | ED001–ED010, each labelled with its evaluation entity (`family` / `run` / `aggregation`) | `experiment-doctor rules` |
| Subcommands | `scan`, `audit`, `rules`, `adapters`, `init`, `run`, `verify` | `experiment-doctor --help` |
| `--version` flag | **does not exist** — usage error | measured |
| Built-in demo | **no** `demo` subcommand; smallest path is `scan`/`audit` over a real artifacts directory | `--help` |
| GitHub Actions | 2 active: CI (`.github/workflows/ci.yml`), Publish to PyPI | `/actions/workflows` |
| CI matrix | Python 3.11 × 3.13, **single OS (Linux)** — no `os:` matrix key in `ci.yml` | `.github/workflows/ci.yml` |
| Community files present | `README.md`, `CHANGELOG.md`, `docs/`, `examples/`, `release/`, three phase/MVP reports at top level; **no** `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`, `CITATION.cff` | `/git/trees/HEAD` |
| Author metadata | PyPI `author = beihai` | PyPI JSON `info.author` |
| Repo description | "Read-only ML experiment provenance and aggregation auditor." | `/repos` |
| README release wording | **Stale in flavour, harmless in effect**: `pip install experiment-doctor # after PyPI publication` — the package *is* published (1.0.0, 2026-09-27), so the comment reads as a condition that has since been met | `README.md` line 38 vs PyPI JSON |
| Shipped CLI help wording | **Stale**: `experiment-doctor --help` prints "Experiment Doctor **v0.1**" while the installed distribution is 1.0.0 | measured `--help` output vs PyPI `info.version` |

### 1.3 Result Doctor

| Field | Measured value | Source |
| --- | --- | --- |
| Repository URL | https://github.com/xihaian251/result-doctor | `/repos/xihaian251/result-doctor` |
| Default branch | `main` | same |
| Latest GitHub Release | `v0.1.0`, published 2026-09-28T13:48:33Z, `target_commitish=bec3ab98e528`, 0 assets | `/releases/latest` |
| Tags | `v0.1.0`→`bec3ab98e5289d4739d57c34413a7a4d2b687da0` (annotated object `5b87cbae3824`) | `/tags`, `/git/matching-refs/tags/` |
| PyPI name | `result-doctor` | PyPI JSON |
| Latest published version | `0.1.0` (only release) | PyPI JSON |
| Wheel | `result_doctor-0.1.0-py3-none-any.whl`, 57,593 B, SHA256 `54b3ddd9a9831cbf08ce4ec0ce2e172eb061ba5ae58121048234c229281038fe`, uploaded 2026-09-28T13:49:01Z | PyPI JSON |
| sdist | `result_doctor-0.1.0.tar.gz`, 78,008 B, SHA256 `e054b57cf1c3f12e41d7d28c1e7567e6b0368fa18033be1f1d630e845d2a7343` | same |
| CLI command | `result-doctor` → `result_doctor.cli:main` | `entry_points.txt` in the published wheel |
| Python requirement | `>=3.11` | wheel `METADATA` |
| License | Apache-2.0 | wheel `METADATA` + `/repos` |
| Runtime dependencies | PyYAML≥6 | PyPI JSON `requires_dist` |
| Rule registry | RD001–RD008 over an eight-object bundle (reported cells, aggregations, members, result artifacts, transformations, candidate sets, selection events, comparison sets) | `README.md` + `/repos` description; consistent with `--help` |
| Subcommands | `audit` only | `result-doctor --help` |
| `--version` flag | **yes** — prints `result-doctor 0.1.0` | measured |
| Status lexicon (as printed by the tool itself) | `PASS \| FAIL \| INCONCLUSIVE \| NOT_APPLICABLE \| NOT_RUN` | `result-doctor --help` |
| Exit codes (as printed by the tool itself) | `0` = audit ran whatever it found; `2` = manifest is not a readable contract; `1` = unexpected tool failure | `result-doctor --help` |
| Built-in demo | **no** `demo` subcommand | `--help` |
| GitHub Actions | 2 active: CI, Publish to PyPI | `/actions/workflows` |
| CI matrix | Python 3.11 × 3.13, **single OS (Linux)** | `.github/workflows/ci.yml` |
| Community files present | `README.md`, `CHANGELOG.md`, `phase0/`–`phase6/`, `release/`, `src/`, `tests/`; **no** `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`, `docs/`, `examples/`, `CITATION.cff` | `/git/trees/HEAD` |
| Author metadata | PyPI `author = None` | PyPI JSON |
| Repo description | "Deterministic, evidence-graded audit of how the runs behind a reported ML result became the printed number (RD001-RD008)." | `/repos` |
| README release wording | **STALE AND WRONG — see §4.** The README states "The package is not published to PyPI, so `pip install result-doctor` will not find it." PyPI shows `result-doctor 0.1.0` published 2026-09-28T13:49:01Z | `README.md` line 18 vs PyPI JSON |

### 1.4 Paper Doctor

| Field | Measured value | Source |
| --- | --- | --- |
| Repository URL | https://github.com/xihaian251/paper-doctor | `/repos/xihaian251/paper-doctor` |
| Default branch | `main` | same |
| Latest GitHub Release | `v0.1.0`, published 2026-09-29T10:38:21Z, `target_commitish=2a02698637f3`, 0 assets, = `/releases/latest` | `/releases/latest` |
| Tags | exactly one: `v0.1.0`→commit `2a02698637f35bd3fec28d98a8b6e272b8e1fc9a`; the annotated tag object is `cd49fcdd705f14a9a03924843c79259909be5db4` | `/tags`, `/git/matching-refs/tags/`, and the local `git rev-parse v0.1.0^{}` at release time |
| PyPI name | `paper-doctor` | PyPI JSON |
| Latest published version | `0.1.0` (only release), uploaded 2026-09-29T10:38:46Z | PyPI JSON |
| Wheel | `paper_doctor-0.1.0-py3-none-any.whl`, 67,719 B, SHA256 `10a5fc2cfe28155b6647edb85fd0e74422e814efc7ac1685a436b06226928461` | PyPI JSON; re-hashed from **downloaded** bytes at release time |
| sdist | `paper_doctor-0.1.0.tar.gz`, 182,137 B, SHA256 `29b759f815d60dc896901eeec3fa3e125faa2caa1e184d4908dbb4d292a11d2e` | same |
| Publishing route | GitHub Actions OIDC trusted publishing, run `36556801154` (event `release`, success); no long-lived token exists | `.github/workflows/publish-pypi.yml` + the run |
| CLI command | `paper-doctor` → `paper_doctor.cli:main` | `entry_points.txt` in the published wheel |
| Python requirement | `>=3.11` | wheel `METADATA` |
| License | Apache-2.0 | wheel `METADATA` + `/repos` |
| Runtime dependencies | PyYAML≥6 | PyPI JSON `requires_dist` |
| Rule registry | PD001–PD007 over `Claim` / `FloatAnchor` / `EvidenceLink` | `/repos` description + `--help` |
| Subcommands | `audit` only | `paper-doctor --help` |
| `--version` flag | **yes** — prints `paper-doctor 0.1.0` | measured |
| Status lexicon | `PASS \| FAIL \| INCONCLUSIVE \| NOT_APPLICABLE \| NOT_RUN` | `paper-doctor --help` |
| Exit codes | `0` = audit ran whatever it found; `2` = manifest is not a readable contract; `1` = unexpected tool failure | `paper-doctor --help` |
| Built-in demo | **no** `demo` subcommand; the repository ships a frozen TabM acceptance corpus reached by `scripts/fetch_acceptance_inputs.py` | `--help` + `/git/trees/HEAD` (`examples/`, `phase3/`, `scripts/`) |
| GitHub Actions | 2 active: `gates` (`.github/workflows/gates.yml`), `publish-pypi` | `/actions/workflows` |
| CI matrix | ubuntu-latest × windows-latest × Python 3.11/3.13 (4 jobs) | `.github/workflows/gates.yml` |
| Community files present | `README.md`, `CHANGELOG.md`, `CITATION.cff` **absent**, `examples/`, `phase0/`–`phase3/`, `release/`, `scripts/`, `src/`, `tests/`; **no** `CONTRIBUTING.md`, `SECURITY.md`, `ROADMAP.md`, `docs/` | `/git/trees/HEAD` |
| Author metadata | PyPI `author = None` | PyPI JSON |
| Repo description | "Deterministic claim-to-evidence audits of reported results in an ML paper. PD001-PD007 over Claim/FloatAnchor/EvidenceLink; no scores, no verdicts." | `/repos` |
| README release wording | **Current.** `pip install paper-doctor==0.1.0` | `README.md` line 44 |
| Frozen scientific state | Phase 3 §15 (real human first-use test) is recorded **NOT OBSERVED** and was waived by the owner; `v0.1.0` is immutable and must never be moved | `release/RELEASE_FREEZE.md` §6, `release/ML_RESEARCH_FINAL_STATE.md` §4 in the repository |

## 2. Cross-component facts

| Fact | Value | Source |
| --- | --- | --- |
| All four install side by side | yes — one fresh venv holds 0.1.2 / 1.0.0 / 0.1.0 / 0.1.0 simultaneously with no resolver complaint | `pip list` in the measurement venv |
| Uniform Python floor | `>=3.11` for all four | each wheel's `METADATA` |
| Uniform license | Apache-2.0 for all four | each wheel's `License-Expression` |
| Uniform authorship identity | **not uniform** — see §5 | PyPI `info.author` |
| Windows compatibility, verified | Dataset Doctor (CI matrix) and Paper Doctor (CI matrix) | workflow files |
| Windows compatibility, **not** CI-verified | Experiment Doctor and Result Doctor (Linux-only matrices) | workflow files |
| Name collision on PyPI | `dataset-doctor` (1.0.1, MIT, author "Dataset Doctor Contributors", homepage `https://github.com/Mirdula18/dataset-doctor`, summary "Automatically diagnose and clean…") is an **unrelated project**. The Dataset Doctor tool is `dataset-doctor-audit` | `https://pypi.org/pypi/dataset-doctor/json` |
| Umbrella name on PyPI | `ml-research-audit` returns `{"message": "Not Found"}` and `/simple/ml-research-audit/` returns **404**, i.e. the name is unclaimed | PyPI JSON + simple index |
| Rule counts | DD 21 (DD001–DD021), ED 10 (ED001–ED010), RD 8 (RD001–RD008), PD 7 (PD001–PD007) | CLI `rules` output for DD/ED; `--help` and repo descriptions for RD/PD |

## 3. Responsibility statements (one line each, as the tools describe themselves)

| Component | Question it answers | Source |
| --- | --- | --- |
| Dataset Doctor | What data entered the evaluation, and does the evaluation boundary hold? | repo description + README ("Detect data leakage before it corrupts your ML experiment") |
| Experiment Doctor | How did this run come to exist — seed, config, code revision, environment? | repo description + `rules` entity labels |
| Result Doctor | How did these runs become this reported number? | repo description + README opening line |
| Paper Doctor | Does this claim faithfully represent the evidence it explicitly points to? | repo description + `--help` |

## 4. README staleness register

Two README/CLI texts conflict with the authoritative sources. Per the task's read-only rule for
child repositories, **neither was edited in this round.** The umbrella documentation must use the
PyPI/GitHub values above, not these strings.

| # | Where | The stale statement | The measured reality | Authority used | Action taken |
| --- | --- | --- | --- | --- | --- |
| S1 | `result-doctor` `README.md:18` | "The package is not published to PyPI, so `pip install result-doctor` will not find it." | `result-doctor 0.1.0` has been on PyPI since 2026-09-28T13:49:01Z | PyPI JSON API | Recorded here; README left untouched; umbrella quickstart uses `pip install result-doctor` |
| S2 | `experiment-doctor` `--help` (shipped in the 1.0.0 wheel) | "Experiment Doctor **v0.1**: audit the provenance…" | installed distribution is `experiment-doctor 1.0.0` | PyPI JSON + wheel `METADATA` | Recorded here; not a scientific defect; umbrella text says "1.0.0" and never quotes that help line as a version source |
| S3 | `experiment-doctor` `README.md:38` | `pip install experiment-doctor # after PyPI publication` | published 2026-09-27 | PyPI JSON | Cosmetic ordering of a comment; recorded, no action |

S1 is the only one that would actively stop a reader from installing the tool. It is the reason the
quickstart in this repository states install commands from measured PyPI data rather than from the
child READMEs.

## 5. Citation identity — no authoritative convention exists

| Component | Author metadata found | Source |
| --- | --- | --- |
| Dataset Doctor | `冯硕` | PyPI JSON `info.author` |
| Experiment Doctor | `beihai` | PyPI JSON `info.author` |
| Result Doctor | none | PyPI JSON (`author = null`) |
| Paper Doctor | none | PyPI JSON (`author = null`) |
| Any child repo `CITATION.cff` | **none** (all four return 404 on `raw.githubusercontent.com/.../HEAD/CITATION.cff`) | measured |

There are three different states across four components and no established citation convention.
Per §24 of the launch brief, **no `CITATION.cff` is created in this round** — writing one would
mean either inventing an author or picking one component's metadata over the others'. Recorded as a
follow-up item in `ROADMAP.md` for the owner to decide.

## 6. Census closure

Every field §2 requires is measured, sourced, and above. Nothing in the umbrella's public
documentation may state a version, package name, CLI name, Python floor, license, or release fact
that contradicts this file; if a value changes, this census is re-run and `stack.yaml` is
regenerated from it by `scripts/verify_stack.py`.

**Census status: CLOSED 2026-09-29.** Public umbrella documentation work may begin.
