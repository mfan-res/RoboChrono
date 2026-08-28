# results/

Evaluation output lands here. Not in git.

```
results/<run_id>/
├── run.json                                what this run was
├── report.md / report.csv
├── log/<model>.log
└── <model>/<scenario>/<dimension>.jsonl    per-question records
    <model>/<scenario>/<dimension>.summary.json
```

## `<run_id>`

The directory name combines the date it was first created with a fingerprint of
the configuration that determines the results: the protocol, the suite, the
dataset fingerprint, the models involved, and the code version. It does not
include concurrency, proxying, or anything else that varies by machine.

- **Re-running the same command after an interruption** — same fingerprint, same
  directory, work resumes
- **Running with changed settings** — different fingerprint, new directory, the
  two sets of results cannot silently mix
- `--fresh` forces a new directory

## The three files

| File | One per | Contents |
| --- | --- | --- |
| `run.json` | run | Dataset version and fingerprint, protocol version, suite, models, code version, environments |
| `summary.json` | (model, scenario, dimension) | Metrics |
| `.jsonl` | (model, scenario, dimension) | Per-question records, including the model's raw output and the full prompt |

Raw output is kept, so a change in how a metric is defined can be recomputed
offline without re-running any model.

## `answered` is not the same as parsed

In `summary.json`:

- `answered` — calls that returned non-empty text
- `parse_failure_rate` — answers that could not be read
- `errors` — calls that failed

**Read `parse_failure_rate` to judge whether a run is healthy.** A run can show
every question answered and no errors while scoring zero, because the model
responded and the answer could not be extracted from what it said.
