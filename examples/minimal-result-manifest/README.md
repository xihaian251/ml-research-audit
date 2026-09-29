# A minimal Result Doctor manifest you can run

Every other document in this portal describes what the tools found in a published paper. This one
exists because the fresh-user audit in [`research/FRESH_USER_AUDIT.md`](../../research/FRESH_USER_AUDIT.md)
found the opposite problem: a reader who has never written a manifest cannot tell which fields are
required and which are optional, and the layer-2 example in
[`examples/tabm-chain`](../tabm-chain/README.md) is a real acceptance input — one published paper's
claims, artifacts pinned by digest, 32 findings. Correct, but not a place to start.

So this directory is the smallest input that makes Result Doctor *decide* rather than decline. Both
manifests here were executed against the published `result-doctor` 0.1.0 wheel in a clean virtual
environment on 2026-09-29; the outputs below are copied from that run, not written by hand.
## What is in the box

Three files on disk, and one number per file:

```
runs/seed0/test_acc.txt   ->  0.8231
runs/seed1/test_acc.txt   ->  0.8245
runs/seed2/test_acc.txt   ->  0.8238
```

The claim under audit is that a table prints **82.4**. That is what the `steps:` block is for. The
`scale` step carries `stage: member`, so it applies to each run before aggregation: 0.8231, 0.8245
and 0.8238 become 82.31, 82.45 and 82.38; their mean is 82.38; the `format` step renders that to one
decimal place, which is the string `82.4`. So the printed number is a *derived* value, and the
manifest says so — the `declared:` block is the author's statement that the paper prints 82.4, and
the `observed:` blocks point at files. Result Doctor's job is to check the first against the last
two.

## Run it

```bash
pip install result-doctor
cd examples/minimal-result-manifest
result-doctor audit result-doctor.yml
```

Measured output, exit code `0`:

```text
RD001   PASS            acc/val
        reason: recomputed rendering equals the reported cell
RD002   PASS            aggregation:agg:acc/val
        reason: membership enumerable and every exclusion bindable
RD003   NOT_APPLICABLE  reported:acc/val
        reason: no selection step is recorded in the production of this cell
RD004   NOT_RUN         rule:RD004
        reason: no target of this class was supplied (candidate_sets is empty)
RD005   NOT_APPLICABLE  acc/val
        reason: the cell carries no dispersion
RD006   PASS            reported:acc/val
        reason: the chain applied step by step yields the printed cell
RD007   NOT_RUN         rule:RD007
        reason: no target of this class was supplied (comparison_sets is empty)
RD008   NOT_RUN         rule:RD008
        reason: no target was supplied for this rule: reported_results is populated,
                but nothing in it carries the key RD008 reads

PASS: 3
FAIL: 0
INCONCLUSIVE: 0
NOT_APPLICABLE: 2
NOT_RUN: 3
```

## Read the passing output before you trust it

This is the single most useful thing about the example: **a clean run here is a clean run of three
rules out of eight.** `RD004`, `RD007` and `RD008` report `NOT_RUN` because this manifest declares
no candidate sets, no comparison sets, and no key those rules read. The tool does not raise an
error and does not mark them `PASS`; it says the input never gave it anything to check.

That is the difference between this stack and a score. A grade of "3 pass, 0 fail" out of eight
rules sounds like 38%, and the tool refuses to compute that percentage, because `NOT_RUN` is not a
failure, `NOT_APPLICABLE` is not a pass, and the three states do not belong in the same arithmetic.
See [`docs/status-semantics.md`](../../docs/status-semantics.md).

## Now break it on purpose

```bash
result-doctor audit result-doctor.noscale.yml
```

`result-doctor.noscale.yml` is identical except that the `scale` step is missing from `steps:` —
the shape of a very ordinary mistake, where the run script multiplied by 100 but the manifest
forgot to record it. Measured output, again exit code `0`:

```text
RD001   FAIL            acc/val
        reason: members, aggregation and transforms are all determined yet the cell differs
RD006   INCONCLUSIVE    reported:acc/val
        reason: the recorded chain does not yield the printed cell; an unrecorded step cannot be excluded
```

with the summary line `PASS: 1`, `FAIL: 1`, `INCONCLUSIVE: 1`, `NOT_APPLICABLE: 2`, `NOT_RUN: 3`.

Two rules disagree about how much the failure tells you. `RD001` is a decision rule: the
determined recomputation does not equal the printed cell, so it says `FAIL`. `RD006` reads the same
chain and stops at `INCONCLUSIVE`, because a manifest that omits a step cannot exclude the
possibility that the author simply forgot to record it. Both statements are true, and the tool does
not collapse them into one.

The important part is the exit code. A `FAIL` here is a **finding**, not a crash: `result-doctor`
returns `0` because the audit ran and produced an answer. Exit `2` means the manifest was not a
readable contract, and exit `1` means the tool itself faulted. If you wire this into CI, decide
deliberately whether a provenance finding should break your build — the tool will not decide for
you.

## What this example does not cover

`RD003` and `RD005` came back `NOT_APPLICABLE` because there is no model-selection step and no
dispersion in a three-seed mean without a spread field. Ancestry, universe recovery and
cross-run comparison are the rest of the schema, and they are what the TabM chain example is
actually about:

- [`examples/tabm-chain/README.md`](../tabm-chain/README.md) — the four-layer trace, including the
  Paper Doctor manifest that pins this tool's findings by digest.
- What this manifest exercises is five fields per reported result: `printed_in`, `value`,
  `aggregate`, `members`, `steps`. That is the minimum needed to bind a printed number to files on
  disk. Everything else in the schema — ancestry, candidate sets, comparison sets, universe
  recovery — is there because a real paper needed it, and the TabM chain shows which paper needed
  which field.
