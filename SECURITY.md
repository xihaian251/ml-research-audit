# Security

## Reporting a vulnerability

Open a **private** security advisory on the repository of the component affected, via GitHub's
"Report a vulnerability" tab, or — if you cannot reach it — open an issue titled exactly
`[SECURITY] <component> <one-line summary>` with no reproducing data in it, and we will escalate.

| Affected | Report in |
| --- | --- |
| dataset audit behaviour, parsing of your data files | [dataset-doctor](https://github.com/xihaian251/dataset-doctor) |
| capture pipeline, adapters, bundle verification | [experiment-doctor](https://github.com/xihaian251/experiment-doctor) |
| manifest parsing, artifact reads, rule evaluation | [result-doctor](https://github.com/xihaian251/result-doctor) |
| LaTeX parsing, manifest handling | [paper-doctor](https://github.com/xihaian251/paper-doctor) |
| this portal: docs, metadata, scripts | this repository |

There is no security mailing list, no PGP key, and no response-time commitment. That is a limitation of
the project's size, so it is stated rather than papered over. If a week passes with no reply, open an
ordinary issue with `[SECURITY]` in the title so it is visible.

## What the tools touch

Measured 2026-09-29 against the four published wheels: none of the four packages contains a token from
`requests.`, `urllib.request`, `urlopen`, `httpx`, `urllib3`, `socket.`, `smtplib` or `ftplib`, and none
declares an HTTP client dependency. No component sends your data anywhere.

Two boundaries this does not cover, stated plainly:

- **`experiment-doctor run` executes a command you give it.** The tool makes no network calls; your
  training script may, and the command line you pass is written into `experiment.run.json`.
- **A manifest lists paths; the tool reads exactly those.** Result Doctor and Paper Doctor resolve
  quoted paths relative to the manifest's own `root:` and read nothing else. A path you put in a
  manifest is a path you have agreed to have read. Do not point a manifest at a secret file.

Each component's own README documents its read/write contract; where they differ, the component is
authoritative and this page is a summary. Dataset Doctor writes reports into a directory you name and,
with `split`, writes a new dataset directory you name; it does not modify the data it audits.

**One exception, and it is in the portal, not in a tool.** `scripts/verify_stack.py` makes no network
calls as run by default. With `--online` it issues one HTTPS GET per component to
`https://pypi.org/pypi/<name>/json` and reads nothing else; it sends no local path, filename, or
finding content, and a failure to reach PyPI is reported as a warning rather than retried silently.
The portal's CI runs that mode on a schedule, so the version numbers published here age visibly.

## Do not attach private material to issues

Audit inputs are the sensitive part of this workflow. A bug report usually needs neither of the things
you might reach for.

| Do not post | Do this instead |
| --- | --- |
| your dataset, or a slice of it | the schema, row counts, and the Dataset Doctor `fingerprint` / `report.json` |
| a real manuscript under review | a synthetic `.tex` that reproduces the parser behaviour |
| credentials, tokens, or cloud config found in a run directory | delete them; if one leaked, rotate it and say that it leaked |
| an unredacted `experiment.run.json` | the same file with `execution.command` and environment package lists reviewed first |
| internal issue trackers or client names in a path | a relative path, or a note that the path was changed |

Redact before posting:

```bash
# look at what a report would reveal before you reveal it
grep -nEi 'token|secret|password|key|/home/|/Users/|C:\\Users' report.json
```

A SHA256 of a private file is generally safe to publish and is often enough to reproduce a finding. A
filename that encodes a client, a patient cohort, or an unpublished experiment may not be.

## Threat model — what these tools are not

| Not a control against | Because |
| --- | --- |
| data exfiltration by your own training code | `experiment-doctor run` executes that code by design |
| a malicious manifest | auditing a project you do not trust means reading its artifacts; treat untrusted repositories as untrusted inputs and run in a sandbox you control |
| someone lying in a declaration | a declaration is evidence about who said what, never proof that it is so |
| tampering with a published paper | the input is a source tree; the tools cannot tell you the tree matches the PDF |
| supply-chain safety generally | the packages are small and dependency-light, but no component has been independently security-reviewed |

## Path traversal and archives

If you report that a manifest with `../../` escapes a project root, or that a crafted archive is
followed, that is a real bug and it belongs in the component repository. Nothing here has been
penetration-tested; the absence of a known issue means the absence of a report, not the presence of a
guarantee.
