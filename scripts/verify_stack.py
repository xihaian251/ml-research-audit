#!/usr/bin/env python3
"""Validate stack.yaml and the portal file set. Read-only; no network by default.

    python scripts/verify_stack.py             # offline structural checks
    python scripts/verify_stack.py --online    # also re-measure PyPI and diff versions

Exit codes: 0 = the portal metadata is consistent; 1 = a stated invariant is violated;
2 = stack.yaml is missing or is not readable YAML. This script never writes anything.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_COMPONENT_FIELDS = (
    "display_name",
    "layer",
    "repository",
    "default_branch",
    "pypi",
    "version",
    "cli",
    "python_requires",
    "license",
    "rules",
    "responsibility",
    "status",
    "release_tag",
    "release_commit",
    "cross_platform_ci_verified",
    "known_documentation_defects",
)
ALLOWED_COMPONENTS = {"dataset_doctor", "experiment_doctor", "result_doctor", "paper_doctor"}
ALLOWED_CHAIN = ["dataset", "experiment", "result", "paper"]
MUST_BE_TRUE = (
    "no_global_score",
    "no_paper_verdict",
    "no_misconduct_verdict",
    "no_llm_judge",
    "unknown_over_inference",
    "inconclusive_is_not_failure",
    "certainty_does_not_increase_across_layers",
    "declares_provenance_not_truth",
)
SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:[.\-+].*)?$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
REPO_URL = re.compile(r"^https://github\.com/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+$")
PORTAL_FILES = (
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "ROADMAP.md",
    "STACK_STATUS.md",
    "stack.yaml",
    "docs/architecture.md",
    "docs/quickstart.md",
    "docs/component-guide.md",
    "docs/evidence-model.md",
    "docs/status-semantics.md",
    "docs/end-to-end-tabm.md",
    "docs/faq.md",
    "docs/community.md",
    "examples/tabm-chain/README.md",
    "examples/minimal-result-manifest/README.md",
    "research/COMPONENT_FACTS.md",
    "research/FRESH_USER_AUDIT.md",
    "scripts/verify_stack.py",
    ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/documentation.yml",
    ".github/ISSUE_TEMPLATE/onboarding-case.yml",
    ".github/ISSUE_TEMPLATE/feature.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/portal-checks.yml",
)
# Assertion wordings the project refuses to make. Two exemptions, both narrow:
# a negation earlier in the same line ("does not prove reproducibility"), and a phrase
# wrapped in quotes or backticks, which mentions the wording as an example instead of
# asserting it. A bare unquoted assertion on a line with no negation is a violation.
BANNED_PHRASES = (
    "proves reproducibility",
    "guarantees reproducibility",
    "proves the paper is true",
    "proves a paper true",
    "detects fraud",
    "detects misconduct",
    "first of its kind",
    "the only tool that",
    "automatic peer reviewer",
    "global trust score",
    "verdict on the paper",
)
NEGATIONS = ("not ", "no ", "never ", "without ", "refuse", "refuses", "prohibited", "banned")
QUOTE_CHARS = "\"'`“”‘’"
# Files whose whole purpose is to quote stale or prohibited wording as evidence.
WORDING_SCAN_SKIP_PREFIXES = ("research/",)


def fail(errors: list[str], msg: str) -> None:
    errors.append(msg)


def check_structure(data: dict, errors: list[str]) -> None:
    if data.get("schema_version") != 1:
        fail(errors, "schema_version must be 1")
    project = data.get("project") or {}
    for field in ("name", "repository", "license"):
        if not project.get(field):
            fail(errors, f"project.{field} is missing")
    if not REPO_URL.match(str(project.get("repository", ""))):
        fail(errors, f"project.repository is not a https://github.com/<owner>/<repo> URL: {project.get('repository')!r}")
    if project.get("pypi") is not None:
        fail(errors, "project.pypi must be null: the umbrella publishes no PyPI distribution")

    components = data.get("components") or {}
    if set(components) != ALLOWED_COMPONENTS:
        fail(errors, f"components must be exactly {sorted(ALLOWED_COMPONENTS)}, got {sorted(components)}")
    layers = []
    for key, comp in sorted(components.items()):
        comp = comp or {}
        for field in REQUIRED_COMPONENT_FIELDS:
            if field not in comp:
                fail(errors, f"components.{key}.{field} is missing")
        if not REPO_URL.match(str(comp.get("repository", ""))):
            fail(errors, f"components.{key}.repository is not a well-formed GitHub URL: {comp.get('repository')!r}")
        if not SEMVER.match(str(comp.get("version", ""))):
            fail(errors, f"components.{key}.version is not a version string: {comp.get('version')!r}")
        if not str(comp.get("release_tag", "")).startswith("v"):
            fail(errors, f"components.{key}.release_tag should be the released git tag")
        if not COMMIT.match(str(comp.get("release_commit", ""))):
            fail(errors, f"components.{key}.release_commit must be a 40-hex commit SHA")
        if not comp.get("cli"):
            fail(errors, f"components.{key}.cli is empty")
        if not str(comp.get("python_requires", "")).startswith(">="):
            fail(errors, f"components.{key}.python_requires should pin a floor")
        if comp.get("license") != "Apache-2.0":
            fail(errors, f"components.{key}.license is {comp.get('license')!r}, expected Apache-2.0")
        if comp.get("status") not in {"released", "pre-release", "archived"}:
            fail(errors, f"components.{key}.status must be released | pre-release | archived")
        if not isinstance(comp.get("known_documentation_defects"), list):
            fail(errors, f"components.{key}.known_documentation_defects must be a list")
        layers.append(comp.get("layer"))

    if data.get("chain") != ALLOWED_CHAIN:
        fail(errors, f"chain must be exactly {ALLOWED_CHAIN}, got {data.get('chain')}")
    if sorted(layers) != sorted(ALLOWED_CHAIN):
        fail(errors, f"component layers must cover the chain once each, got {layers}")

    principles = data.get("principles") or {}
    for key in MUST_BE_TRUE:
        if principles.get(key) is not True:
            fail(errors, f"principles.{key} must be true; this project does not negotiate that invariant")


def check_status(data: dict, errors: list[str]) -> None:
    status = data.get("status_model") or {}
    if status.get("released_components") != len(ALLOWED_COMPONENTS):
        fail(errors, "status_model.released_components must equal the number of released components")
    if status.get("human_onboarding_observed") is not False:
        fail(
            errors,
            "status_model.human_onboarding_observed may only become true once a real person has "
            "completed an onboarding and the evidence is recorded; an agent simulation is not human onboarding",
        )


def check_portal_files(errors: list[str]) -> None:
    for rel in PORTAL_FILES:
        if not (ROOT / rel).is_file():
            fail(errors, f"required portal file missing: {rel}")


def check_wording(errors: list[str]) -> None:
    for path in sorted(ROOT.rglob("*.md")):
        rel = path.relative_to(ROOT).as_posix()
        if rel.startswith(WORDING_SCAN_SKIP_PREFIXES):
            continue
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            low = line.lower()
            for phrase in BANNED_PHRASES:
                start = 0
                while True:
                    idx = low.find(phrase, start)
                    if idx == -1:
                        break
                    end = idx + len(phrase)
                    before = line[max(0, idx - 1) : idx]
                    after = line[end : end + 1]
                    quoted_mention = before in QUOTE_CHARS and after in QUOTE_CHARS
                    if quoted_mention or any(n in low[:idx] for n in NEGATIONS):
                        start = end
                        continue
                    fail(
                        errors,
                        f"{rel}:{lineno}: prohibited claim wording {phrase!r} stated as a claim, "
                        "without a negation or quotation marks",
                    )
                    start = end


def check_online(data: dict, errors: list[str]) -> None:
    """Opt-in. A mismatch means the census is stale, not that a component is wrong."""
    for key, comp in sorted((data.get("components") or {}).items()):
        name = comp["pypi"]
        url = f"https://pypi.org/pypi/{name}/json"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ml-research-audit-portal-check"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                latest = json.load(resp)["info"]["version"]
        except Exception as exc:  # noqa: BLE001 - network is a system boundary: report, never crash silently
            print(f"  WARN  {key}: PyPI unreachable ({exc})", file=sys.stderr)
            continue
        if latest != comp["version"]:
            fail(errors, f"components.{key}.version says {comp['version']}, PyPI says {latest} - re-run the census")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--online", action="store_true", help="also compare versions against PyPI")
    args = parser.parse_args()

    path = ROOT / "stack.yaml"
    if not path.is_file():
        print("ERROR: stack.yaml is missing", file=sys.stderr)
        return 2
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"ERROR: stack.yaml is not readable YAML: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("ERROR: stack.yaml must be a mapping", file=sys.stderr)
        return 2

    errors: list[str] = []
    check_structure(data, errors)
    check_status(data, errors)
    check_portal_files(errors)
    check_wording(errors)
    if args.online:
        check_online(data, errors)

    components = data.get("components") or {}
    print(f"stack.yaml schema_version={data.get('schema_version')} components={len(components)}")
    for key, comp in sorted(components.items()):
        print(f"  {key:18s} {comp['pypi']:22s} {comp['version']:8s} cli={comp['cli']}")

    if errors:
        print(f"\n{len(errors)} problem(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1
    print("\nOK: portal metadata is consistent.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
