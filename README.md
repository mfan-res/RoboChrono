# RoboChrono

> ⚠ **Draft.** Structure is settled; content is being filled in.

A temporal visual reasoning benchmark over egocentric robot manipulation video.

---

## What it measures

**15 manipulation scenarios × 7 evaluation dimensions = 13,636 questions,
recorded on 3 embodiments.**

A *dimension* is a way of asking — the same footage queried seven different
ways. It is not a scoring axis.

| Dimension | Asks | Input | Metric | Questions |
| --- | --- | --- | --- | ---: |
| `current_action` | What is happening right now | clip | accuracy | 1,995 |
| `next_action` | What the robot should do next | clip | accuracy | 1,965 |
| `next_action_with_goal` | What to do next, given the overall goal | clip | accuracy | 1,965 |
| `action_time` | When a named action occurs | full episode | tIoU@0.5 | 1,995 |
| `view_match` | Which image is a given wrist camera's view at this moment | head image + option images | accuracy | 1,995 |
| `frame_match` | Which option image appears in the clip | clip + option images | accuracy | 1,995 |
| `frame_order` | The chronological order of three frames | still frames | accuracy | 1,726 |

`next_action` and `next_action_with_goal` differ only in whether the prompt
names the overall task, which is what makes the pair a controlled comparison.

Names describe **what is asked**, not what an answer proves. A dimension is not
claimed to isolate a capability — see *Reading the results* below for what each
score does and does not support.

Scenarios are named `<task>_<embodiment>`, across three platforms — `tianji`
(parallel gripper), `tianjihand` (the same arm with a five-finger hand) and
`gim` (a different bimanual platform):

| Embodiment | Scenarios |
| --- | --- |
| `tianji` | `brew_teabag_tianji` `make_tea_tianji` `pack_aidkit_tianji` `pack_airpods_tianji` `takeout_trash_tianji` `wash_dishes_tianji` |
| `tianjihand` | `box_pen_tianjihand` `move_gift_tianjihand` `stack_cubes_tianjihand` |
| `gim` | `cap_pen_gim` `pack_aidkit_gim` `pack_gift_gim` `slip_tshirt_gim` `stack_cubes_gim` `wipe_plate_gim` |

Two tasks appear on two embodiments each (`pack_aidkit_*`, `stack_cubes_*`),
which allows a like-for-like cross-embodiment comparison on those tasks.

<!-- TODO: worked example, ideally view_match -->

---

## Quickstart

### 1. Environments — **two are required**

Model families have mutually exclusive requirements: some load only under
transformers 4.x, others only under 5.x. No single environment runs every model.

`pip install robochrono` therefore does **not** give you a working setup; the
package deliberately does not pin a transformers version.

```bash
uv sync --extra tf4
uv sync --extra tf5
```

`robochrono preflight` checks this and prints what to fix.

### 2. Data

Each dataset release lives in its own root — `data/v20` (the fifteen
scenarios of 2.0), `data/v21` (the ten of 2.1) — and every command names the
root it works on with `--data-root`. The root name is the dataset version
with the dot dropped (dots in directory names invite tooling trouble); the
scheme assumes single-digit minor versions. A suite pins the dataset version
it belongs to, and a mismatched root fails loudly rather than silently mixing.

Suites and dataset versions are separate axes on purpose. A dataset version
says which questions exist; a suite (`configs/suites/*.json`) is a frozen
scenario-and-dimension set that published scores cite. Published suites are
never edited — a new dataset release gets a new suite file, and several
suites may draw on the same release. Scores are comparable exactly when they
share a suite and a dataset fingerprint; `robochrono report` enforces this.

```bash
hf download GIM-RoboLab/robochrono --repo-type dataset --local-dir /tmp/robochrono-dl
mkdir -p data/v20 data/v21
for t in /tmp/robochrono-dl/vqa_2/*.tar;       do tar -xf "$t" -C data/v20; done
for t in /tmp/robochrono-dl/vqa_10_task/*.tar; do tar -xf "$t" -C data/v21; done
cp /tmp/robochrono-dl/vqa_2/manifest.json data/v20/ && cp -r /tmp/robochrono-dl/vqa_2/qa data/v20/
cp /tmp/robochrono-dl/vqa_10_task/manifest.json data/v21/ && cp -r /tmp/robochrono-dl/vqa_10_task/qa data/v21/

robochrono validate-data --data-root data/v20   # check immediately after downloading
robochrono validate-data --data-root data/v21
```

The dataset repository is private during review; ask for access.

The download lands in `data/` and documents itself — `data/README.md` ships
with the dataset and describes the layout, the question format, and the known
limitations. In brief:

```
data/
├── manifest.json      version, fingerprint, per-scenario and per-dimension counts
├── qa/                questions, and everything they are rendered from
└── media/             episodes, clips, frames
```

`media/episodes/` is 26 GB of the 42 GB and only `action_time` uses it.
Skip it if you are not running that dimension.

### 3. Run

```bash
robochrono eval --suite v1 --data-root data/v20
robochrono eval --suite v1 --data-root data/v20 --dry-run   # what would run, and its cost
```

Environment switching is automatic — each model is dispatched to the interpreter
it needs. No manual activation.

### 4. Report

```bash
robochrono report               # the most recent run
robochrono report <run_id>      # a specific one
```

---

## How it works

```
robochrono/
├── config/        readers for configs/ — protocol, models, suites, environments
├── dataset/       the data contract: manifest, question loading, rendering
├── dimensions/    how each dimension asks, parses and scores
├── parsing.py     extracting an answer from free-form model output
├── results/       run identity, per-question storage, reporting
├── adapters/      one file per model family — the only code importing an inference stack
├── engine.py      runs one (model, scenario, dimension): load → call → parse → score → store
├── media_prep.py  API only: fitting media into a request-size budget
├── orchestrate/   expands suite × models, dispatches to the right environment, pools GPUs
├── preflight.py   pre-run checks: environments, weights, data, configuration
└── cli.py         thin entry points for the five commands
```

One `eval` invocation flows top to bottom:

1. **config** reads the protocol, suite and model files; anything missing is a
   hard error rather than a default.
2. **preflight** cross-checks environments, weights and the dataset
   fingerprint before anything runs.
3. **results/runid** fingerprints the configuration and finds or creates
   `results/<date>_<fingerprint>/`. Re-running the same command resumes in
   place; changing the experiment lands in a new directory.
4. **orchestrate** expands the suite into (model, scenario, dimension) units
   and starts each model under the interpreter its environment declares — no
   manual environment switching.
5. **engine** runs each unit: the loader renders questions, the dimension
   assembles the call, the adapter talks to the model, parsing extracts an
   answer, the dimension scores it, and the store appends one JSONL row per
   question, which is also what makes interrupted runs resumable.
6. **results/report** aggregates summaries into one table — and refuses to
   merge results produced on different datasets.

Three structural rules hold the design together:

- **The dataset is the contract.** Questions, wording and the fingerprint are
  self-contained under `data/qa/`; the loader adapts to the data, never the
  other way around.
- **Results carry their identity.** The configuration fingerprint runs through
  the directory name, `run.json` and the report header, so scores from
  different datasets or protocols cannot silently mix.
- **Orchestration never imports the inference stack.** Only `adapters/` may
  import torch or transformers, and only inside worker processes. This is what
  lets one command drive models with mutually exclusive dependencies.

## Reading the results

A run directory holds three layers, and they answer different questions:

| File | Answers |
| --- | --- |
| `run.json` | what experiment this was — dataset fingerprint, protocol, models, code |
| `<model>/<scenario>/<dimension>.summary.json` | the metrics for one combination |
| `...<dimension>.jsonl` | every question: full prompt, raw output, parse, score |

Before comparing any numbers, read the two flag sections of `report.md`:

- **✗ did not execute properly** — that cell is not a score. The calls failed,
  or the output could not be read at scale. Fix the setup before comparing.
- **⚠ at or below the degenerate floor** — the score is no better than a
  strategy that never watches the video (0.25 for four-way choice; answering
  the whole clip for temporal grounding). It does not say *why*.

Two fields that look alike and are not: `answered` counts calls that returned
text; `parse_failure_rate` counts answers no parser could read. A run can be
100% answered, 0 errors, and still measure nothing — unreadable answers score
zero, by the same convention in every dimension.

Generation settings are part of what is measured. Models running with
different thinking settings are different experiments sharing a table; the
report's *Execution settings* section lists each model's settings, and flags
any model that appears under more than one.

---

## Leaderboard

Populated when the first full run lands.

---

## Known limitations

The dataset documents its own limitations in the `README.md` it ships with —
transition entropy (in nine scenarios `next_action` is closer to recall than
prediction), authored synthetic distractors, episode-length effects on
`action_time`, and the upscaled `gim` footage. Evaluation-side, know these:

- **Scores under different thinking settings are not comparable.** Models that
  cannot disable thinking declare it, and the report flags them.
- **`frame_order` sits near the random floor for every model tested so far.**
  A low score there separates nothing yet.
- **Occasional out-of-memory failures are recorded, not hidden.** Rerun the
  same command with `--gpus-per-worker 2` to retry only the failed questions.
- **InternVL-architecture models overflow their context on full episodes.**
  At the protocol's one frame per second, a two-minute episode tokenizes to
  ~31k tokens against a 12,288-token window; the tokenizer warns, inference
  proceeds, and the near-floor `action_time` scores for these models reflect
  that reality. The frame density is not lowered per model — a context window
  that cannot hold the input is a measured limitation, not a harness defect.

---

## Citation

A citation will be added upon release.

## License

- Code: Apache-2.0
- Data: CC-BY-4.0
