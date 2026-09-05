# RoboChrono — Results on dataset 2.0 (suite v1) and 2.1 (suite v2)

Prepared for paper writing. Every number here comes from finished, audited runs;
nothing is extrapolated. Read §5 before quoting anything — it lists what is and
is not measured.

## 1. What the benchmark asks

Temporal visual reasoning over egocentric robot-manipulation video, in seven
dimensions:

| Dimension | Question | Input | Metric |
| --- | --- | --- | --- |
| `current_action` | which action is happening | action clip | accuracy |
| `next_action` | which action comes next | action clip | accuracy |
| `next_action_with_goal` | which action comes next, given the goal | action clip | accuracy |
| `frame_match` | which still frame belongs to this clip | clip + frames | accuracy |
| `view_match` | which other camera shows the same moment | frames | accuracy |
| `frame_order` | put three frames in chronological order | frames | accuracy |
| `action_time` | when does the named action occur | full episode | tIoU@0.5 |

Six choice dimensions are 4-way multiple choice (floor 0.25). `action_time` is
temporal grounding, scored tIoU@0.5; answering "the whole video" without watching
reaches mean tIoU ≈ 0.13, which is the floor used here.

## 2. Two evaluation sets

Dataset version and suite are separate axes. A dataset version says which
questions exist; a suite is the frozen scenario × dimension set a published
number cites. Scores are comparable exactly when they share both.

| | **Suite v1** | **Suite v2** |
| --- | --- | --- |
| Dataset version | 2.0 (fingerprint `64fbe7657d0d`) | 2.1 (fingerprint `44375188275c`) |
| Scenarios | 15 | 10 |
| Questions in dataset | 13,636 | 7,812 |
| Coverage | 105/105 combinations | 65/70 (see §5.2) |
| Models evaluated | 11 | 11 |
| **Answers collected** | **149,996** | **85,932** |
| Error rows | **0** | **0** |

The two sets share no scenarios, so v1 and v2 numbers are not comparable
model-for-model as "improvement"; they are two different exam papers over
disjoint material.

## 3. Results — suite v1 (dataset 2.0, 15 scenarios, 11 models)

Per-scenario breakdowns are in Appendix A.

Weighted by question count. "Choice avg" is the question-weighted mean over the
six choice dimensions (`Time` is excluded from it: tIoU and accuracy are not
the same scale and must not be averaged together).

| Model | Params | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time | Choice avg |
| --- | :--: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 9B | 0.711 | 0.527 | 0.570 | 0.864 | 0.423 | 0.326 | 0.325 | **0.576** |
| Qwen3-VL-32B-Instruct | 32B | 0.734 | 0.505 | 0.574 | 0.749 | 0.322 | 0.330 | 0.496 | **0.541** |
| Qwen3-VL-30B-A3B-Instruct | 30B-A3B | 0.662 | 0.435 | 0.457 | 0.871 | 0.336 | 0.274 | 0.406 | **0.512** |
| RynnBrain1.1-2B | 2B | 0.614 | 0.393 | 0.467 | 0.835 | 0.389 | 0.257 | 0.099 | **0.498** |
| Qwen3-VL-8B-Instruct | 8B | 0.660 | 0.442 | 0.477 | 0.748 | 0.333 | 0.270 | 0.359 | **0.494** |
| Qwen3-VL-8B-Thinking | 8B | 0.609 | 0.409 | 0.441 | 0.746 | 0.301 | 0.258 | 0.337 | **0.466** |
| RynnBrain-2B | 2B | 0.566 | 0.357 | 0.391 | 0.679 | 0.347 | 0.237 | 0.135 | **0.434** |
| Cosmos-Reason2-2B | 2B | 0.575 | 0.397 | 0.416 | 0.535 | 0.318 | 0.262 | 0.393 | **0.421** |
| Qwen3-VL-2B-Instruct | 2B | 0.503 | 0.313 | 0.314 | 0.439 | 0.306 | 0.258 | 0.204 | **0.358** |
| SenseNova-SI-1.1-InternVL3-2B | 2B | 0.440 | 0.329 | 0.372 | 0.402 | 0.286 | 0.275 | 0.000 | **0.352** |
| Cosmos3-Edge-2B | 2B | 0.492 | 0.381 | 0.406 | 0.239 | 0.243 | 0.207 | 0.246 | **0.335** |


## 4. Results — suite v2 (dataset 2.1, 10 scenarios, 11 models)

Per-scenario breakdowns are in Appendix B.

| Model | Params | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time | Choice avg |
| --- | :--: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 9B | 0.740 | 0.629 | 0.676 | 0.884 | 0.478 | 0.381 | 0.530 | **0.655** |
| Qwen3-VL-30B-A3B-Instruct | 30B-A3B | 0.774 | 0.545 | 0.644 | 0.906 | 0.317 | 0.327 | 0.478 | **0.618** |
| Qwen3-VL-32B-Instruct | 32B | 0.743 | 0.580 | 0.645 | 0.732 | 0.294 | 0.354 | 0.434 | **0.586** |
| RynnBrain1.1-2B | 2B | 0.661 | 0.431 | 0.495 | 0.907 | 0.447 | 0.300 | 0.251 | **0.563** |
| Qwen3-VL-8B-Instruct | 8B | 0.683 | 0.512 | 0.569 | 0.761 | 0.347 | 0.336 | 0.378 | **0.558** |
| Qwen3-VL-8B-Thinking | 8B | 0.631 | 0.555 | 0.577 | 0.796 | 0.310 | 0.327 | 0.434 | **0.558** |
| RynnBrain-2B | 2B | 0.613 | 0.478 | 0.519 | 0.793 | 0.369 | 0.307 | 0.267 | **0.535** |
| Cosmos-Reason2-2B | 2B | 0.611 | 0.529 | 0.485 | 0.537 | 0.303 | 0.291 | 0.320 | **0.478** |
| Qwen3-VL-2B-Instruct | 2B | 0.531 | 0.401 | 0.359 | 0.397 | 0.297 | 0.304 | 0.190 | **0.393** |
| SenseNova-SI-1.1-InternVL3-2B | 2B | 0.439 | 0.401 | 0.447 | 0.419 | 0.245 | 0.326 | 0.000 | **0.390** |
| Cosmos3-Edge-2B | 2B | 0.617 | 0.435 | 0.443 | 0.283 | 0.205 | 0.195 | 0.251 | **0.386** |


## 5. What is and is not measured — read before quoting

### 5.1 Cells marked "not measured" (✗)

A cell is excluded from every average above when more than half its answers could
not be parsed although the calls succeeded. These are **not zeros**; the model
produced output the answer parser could not read, so the cell measures nothing.
Excluding them is the conservative choice — scoring them zero would flatter the
other models.

Suite v1 — 6 cells excluded (of 1,155): Cosmos3-Edge-2B ×4
(`box_pen_tianjihand/action_time`, `brew_teabag_tianji/frame_order`,
`pack_airpods_tianji/frame_order`, `stack_cubes_tianjihand/frame_order`),
RynnBrain-2B ×1 (`pack_aidkit_tianji/action_time`),
SenseNova-SI-1.1-InternVL3-2B ×1 (`box_pen_tianjihand/action_time`).

Suite v2 — 2 cells excluded (of 770): Cosmos3-Edge-2B
(`sort_cubes_tianji/frame_order`, 56% unparseable — outputs such as `4c`, a bare
`_`, or 19,864 characters of prose that never names an option) and
RynnBrain1.1-9B (`tidy_stationery_tianji/action_time`, 63% unparseable — 120
answers were the identical string `{"answers": []}`, i.e. the model declined in
bulk on the longest scenario).

### 5.2 Empty cells (n/a) — suite v2 only

88 of 770 cells report `n/a`: the dataset asks no questions there, so nothing was
run. Two causes, both structural:

- **Single-camera scenarios have no `view_match`**: `box_pen_hand`,
  `pack_sunglasses_hand`, `stack_cubes_hand` (11 cells each).
- **`move_flower_hand` is a partial scenario** (55 cells): its episodes contain
  only two annotated segments, which is below the structural minimum for
  `next_action` and `next_action_with_goal` (no real distractor besides the
  answer), `frame_match` and `view_match` (no third distractor frame outside the
  anchor segment) and `frame_order` (fewer than three adjacent segments). It is
  kept as an honest partial scenario rather than dropped; its `current_action`
  and `action_time` numbers are real.

Coverage is therefore 65/70 scenario × dimension combinations for suite v2, and
105/105 for suite v1.

### 5.3 Below-floor cells (⚠)

Suite v1 has 181 cells at or below the degenerate floor, suite v2 has 78. Below
floor does **not** by itself mean the model is weak — a unit mismatch, a parser
mismatch, or a question measuring something other than intended look identical.
They are included in the averages (they are real scores) but should be checked
before being used as evidence about a specific model on a specific dimension.

The concentration is informative: the three weakest models account for most of
them, and within a model they cluster on `frame_match` / `view_match` /
`frame_order` — the multi-image dimensions.

### 5.4 A known data defect in dataset 2.1

128 of 1,707 clips in dataset 2.1 are each **one frame short** of what their
annotation declares (ratio 1.01–1.03): `pack_sunglasses_hand` 68,
`stack_cubes_hand` 53, `box_pen_hand` 5, `move_flower_hand` 2. The cause is a
stream-copy cut landing next to, rather than on, a keyframe.

358 of 7,812 questions (4.58%) reference an affected clip, in
`current_action`, `next_action`, `next_action_with_goal` and `frame_match`.
`action_time`, `view_match` and `frame_order` do not read clips and are
unaffected.

**Assessed impact: none on any conclusion.** The missing frame is the last one of
a ~44–58 frame clip (2–3% of its duration); the action it shows is fully present
in the remaining frames, and frames are sampled at a fixed 2 fps rather than by
index. The runs were left as they are rather than repeated. Dataset 2.0 is free
of this defect (0 of its clips affected).

### 5.5 Context-window truncation on one model family

SenseNova-SI-1.1-InternVL3-2B has a 12,288-token context and spends 256 tokens
per frame at a fixed 448² tile, so roughly 48 frames fill the window regardless
of source resolution. On `action_time`, which reads full one-to-two-minute
episodes, the model sees a truncated prefix — its measured mean tIoU is 0.000 in
both suites, and its answers collapse to a near-constant interval (on
`box_pen_hand`, 112 of the 119 parsed answers were the identical 0.01–0.11 s
window, against ground-truth intervals spread through the episode). This is a
measured property of the model under a protocol that was deliberately not
lowered per model, not a framework fault. Qwen3-VL models allocate vision tokens
dynamically and merge across frames, and are not subject to this limit.

## 6. Protocol (state this in the methods section)

Identical for every model; a model may raise `max_new_tokens` but never lower it.

| Setting | Value |
| --- | --- |
| Temperature | 0.0 (greedy; sampling would make runs unreproducible) |
| `max_new_tokens` | 4096 baseline |
| Thinking mode | disabled where it can be disabled; models that cannot declare their real state |
| System prompt | identical for all models, asks for a single JSON object |
| Frame sampling | fixed **temporal density**, not frame count: 2 fps for clip dimensions, 1 fps for `action_time`; min 4, max 768 frames |
| Answer parsing | one baseline parser for all; additive fallbacks only, and rows they rescue are flagged |
| Retries | 3, on infrastructure failure only |

Frame sampling fixes density rather than count on purpose: with a fixed count,
video length becomes a confound, and a low score on a longer scenario would mix
"the model is worse here" with "we showed it less".

An unreadable answer is scored zero with `parse_ok=False`; it is never an error
row. Error rows are reserved for call and infrastructure failures — of which
there were **zero across all 235,928 answers**.

## 7. Reproducing these numbers

Both merged reports are checked in under `results/`:

- Suite v1: `results/merged-v1/` (runs `2026-08-28_3cf47468139a` on 8×RTX 4090,
  `2026-08-28_0a64f2a8065a` on 8×H100)
- Suite v2: `results/merged-v2/` (runs `2026-08-30_936cabf1d429` on 8×RTX 4090,
  `2026-08-30_84b1066c4566` on 8×H100)

Each contains `report.md` (per-scenario tables, fault and floor listings) and
`report.csv` (one row per model × scenario × dimension, with `total`,
`answered`, `errors`, `parse_failure_rate`, `floor` and `fault` columns) — the
csv is the right source for any recomputation.

Regenerate with:

```bash
robochrono report <run-dir> <run-dir> --out <out-dir>
```

Every run directory carries a `run.json` recording the suite, the dataset
fingerprint, the model set, the code commit and the exact command line; runs are
identified by `<date>_<fingerprint>` where the fingerprint covers the protocol,
the suite, the selected model configurations, the dataset and the code state.
`tools/audit_run.py <run-dir> --data-root <root>` re-checks a run for
completeness before it is merged; all four runs above pass it.

## 8. Two things worth a sentence in the paper

**No model is close to solved on temporal ordering.** `frame_order` falls in
0.195–0.381 for every one of the 11 models across both suites (best: Qwen3-VL-32B
at 0.330 on v1, RynnBrain1.1-9B at 0.381 on v2), against a 0.25 floor. Several
models sit below the floor. Whatever these models do with video, putting three
frames in chronological order is not it.

**Parameter count is not the ordering.** RynnBrain1.1-9B leads both suites ahead
of Qwen3-VL-32B and Qwen3-VL-30B-A3B, and RynnBrain1.1-2B places fourth on both,
ahead of both 8B models. The spread *within* the six 2B models is wider than the
distance from the best 2B model to the best model overall: on suite v2, 0.386
(Cosmos3-Edge-2B) to 0.563 (RynnBrain1.1-2B) is a 0.177 spread, while
RynnBrain1.1-2B to RynnBrain1.1-9B (0.655) is 0.092. Training matters more than
scale at this size.


## Appendix A. Per-scenario results — suite v1 (dataset 2.0)

### Scenarios

| Scenario | Embodiment | Views | fps | Resolution | Episodes | Questions |
| --- | --- | :--: | ---: | :--: | ---: | ---: |
| `box_pen_tianjihand` | tianjihand | 3 | 30 | 640×480 | 50 | 1000 |
| `brew_teabag_tianji` | tianji | 3 | 30 | 640×480 | 52 | 1092 |
| `cap_pen_gim` | gim | 3 | 50 | 736×416 | 60 | 1200 |
| `make_tea_tianji` | tianji | 3 | 25 | 770×398 | 39 | 819 |
| `move_gift_tianjihand` | tianjihand | 3 | 20 | 640×480 | 30 | 510 |
| `pack_aidkit_gim` | gim | 3 | 50 | 736×416 | 50 | 1050 |
| `pack_aidkit_tianji` | tianji | 3 | 25 | 770×398 | 40 | 840 |
| `pack_airpods_tianji` | tianji | 3 | 30 | 640×480 | 40 | 840 |
| `pack_gift_gim` | gim | 3 | 50 | 736×416 | 25 | 525 |
| `slip_tshirt_gim` | gim | 3 | 50 | 736×416 | 49 | 980 |
| `stack_cubes_gim` | gim | 3 | 50 | 736×416 | 50 | 1050 |
| `stack_cubes_tianjihand` | tianjihand | 3 | 30 | 640×480 | 50 | 1000 |
| `takeout_trash_tianji` | tianji | 3 | 25 | 770×398 | 40 | 840 |
| `wash_dishes_tianji` | tianji | 3 | 25 | 770×398 | 40 | 840 |
| `wipe_plate_gim` | gim | 3 | 50 | 736×416 | 50 | 1050 |

### Scenario difficulty — mean over the 11 models

Not-measured cells (✗) are excluded from these means; `n/a` means the dataset asks nothing there. `Choice mean` averages the six choice dimensions only.

| Scenario | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time | Choice mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `box_pen_tianjihand` | 0.464 | 0.244 | 0.285 | 0.767 | 0.345 | 0.278 | 0.352 | **0.397** |
| `brew_teabag_tianji` | 0.609 | 0.447 | 0.422 | 0.830 | 0.308 | 0.314 | 0.371 | **0.488** |
| `cap_pen_gim` | 0.436 | 0.268 | 0.383 | 0.663 | 0.243 | 0.302 | 0.237 | **0.382** |
| `make_tea_tianji` | 0.830 | 0.376 | 0.355 | 0.724 | 0.382 | 0.288 | 0.583 | **0.492** |
| `move_gift_tianjihand` | 0.347 | 0.614 | 0.745 | 0.561 | 0.358 | 0.312 | 0.157 | **0.489** |
| `pack_aidkit_gim` | 0.615 | 0.393 | 0.403 | 0.559 | 0.402 | 0.293 | 0.137 | **0.444** |
| `pack_aidkit_tianji` | 0.635 | 0.509 | 0.520 | 0.590 | 0.352 | 0.331 | 0.188 | **0.490** |
| `pack_airpods_tianji` | 0.477 | 0.220 | 0.279 | 0.718 | 0.248 | 0.259 | 0.048 | **0.367** |
| `pack_gift_gim` | 0.394 | 0.463 | 0.383 | 0.559 | 0.276 | 0.299 | 0.063 | **0.396** |
| `slip_tshirt_gim` | 0.538 | 0.438 | 0.637 | 0.544 | 0.287 | 0.261 | 0.336 | **0.451** |
| `stack_cubes_gim` | 0.639 | 0.493 | 0.493 | 0.590 | 0.285 | 0.270 | 0.401 | **0.462** |
| `stack_cubes_tianjihand` | 0.886 | 0.547 | 0.677 | 0.722 | 0.445 | 0.252 | 0.433 | **0.588** |
| `takeout_trash_tianji` | 0.845 | 0.686 | 0.651 | 0.743 | 0.345 | 0.180 | 0.193 | **0.575** |
| `wash_dishes_tianji` | 0.648 | 0.363 | 0.389 | 0.589 | 0.371 | 0.224 | 0.251 | **0.431** |
| `wipe_plate_gim` | 0.516 | 0.259 | 0.201 | 0.468 | 0.285 | 0.221 | 0.225 | **0.325** |

### Per-scenario detail

`✗` = not measured (majority of answers unparseable; excluded from every mean in
this document). `⚠` = at or below the degenerate floor. `n/a` = the dataset asks
no questions there. A cell can carry both marks.


**`box_pen_tianjihand`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.453 | 0.327 | 0.493 | 0.980 | 0.413 | 0.420 | 0.400 |
| Qwen3-VL-32B | 0.420 | 0.347 | 0.407 | 0.973 | 0.387 | 0.290 | 0.520 |
| Qwen3-VL-30B-A3B | 0.513 | 0.273 | 0.300 | 0.980 | 0.393 | 0.290 | 0.507 |
| RynnBrain1.1-2B | 0.433 | 0.333 | 0.540 | 0.953 | 0.393 | 0.330 | 0.073 |
| Qwen3-VL-8B | 0.553 | 0.247⚠ | 0.213⚠ | 0.960 | 0.440 | 0.260 | 0.520 |
| Qwen3-VL-8B-Thinking | 0.480 | 0.327 | 0.307 | 0.913 | 0.347 | 0.280 | 0.413 |
| RynnBrain-2B | 0.560 | 0.120⚠ | 0.093⚠ | 0.933 | 0.347 | 0.240⚠ | 0.173 |
| Cosmos-Reason2-2B | 0.400 | 0.047⚠ | 0.087⚠ | 0.707 | 0.287 | 0.200⚠ | 0.433 |
| Qwen3-VL-2B | 0.453 | 0.160⚠ | 0.060⚠ | 0.393 | 0.320 | 0.250 | 0.127 |
| SenseNova-InternVL3-2B | 0.500 | 0.213⚠ | 0.347 | 0.473 | 0.273 | 0.310 | 0.000✗⚠ |
| Cosmos3-Edge-2B | 0.333 | 0.293 | 0.287 | 0.173⚠ | 0.193⚠ | 0.190⚠ | 0.093✗⚠ |

**`brew_teabag_tianji`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.667 | 0.442 | 0.359 | 1.000 | 0.385 | 0.346 | 0.333 |
| Qwen3-VL-32B | 0.686 | 0.494 | 0.474 | 0.987 | 0.276 | 0.378 | 0.744 |
| Qwen3-VL-30B-A3B | 0.622 | 0.417 | 0.455 | 0.987 | 0.237⚠ | 0.346 | 0.641 |
| RynnBrain1.1-2B | 0.622 | 0.385 | 0.410 | 0.955 | 0.410 | 0.308 | 0.173 |
| Qwen3-VL-8B | 0.577 | 0.506 | 0.474 | 0.936 | 0.308 | 0.333 | 0.526 |
| Qwen3-VL-8B-Thinking | 0.679 | 0.288 | 0.359 | 0.929 | 0.263 | 0.308 | 0.365 |
| RynnBrain-2B | 0.481 | 0.397 | 0.276 | 0.929 | 0.417 | 0.250 | 0.167 |
| Cosmos-Reason2-2B | 0.660 | 0.513 | 0.513 | 0.699 | 0.282 | 0.282 | 0.468 |
| Qwen3-VL-2B | 0.596 | 0.481 | 0.417 | 0.744 | 0.288 | 0.276 | 0.359 |
| SenseNova-InternVL3-2B | 0.500 | 0.558 | 0.474 | 0.487 | 0.295 | 0.314 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.609 | 0.436 | 0.429 | 0.474 | 0.224⚠ | 0.096✗⚠ | 0.308 |

**`cap_pen_gim`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.550 | 0.328 | 0.439 | 0.967 | 0.311 | 0.325 | 0.228 |
| Qwen3-VL-32B | 0.656 | 0.228⚠ | 0.456 | 0.911 | 0.194⚠ | 0.417 | 0.578 |
| Qwen3-VL-30B-A3B | 0.400 | 0.311 | 0.517 | 0.972 | 0.189⚠ | 0.317 | 0.350 |
| RynnBrain1.1-2B | 0.417 | 0.306 | 0.439 | 0.894 | 0.339 | 0.325 | 0.039⚠ |
| Qwen3-VL-8B | 0.572 | 0.322 | 0.406 | 0.872 | 0.200⚠ | 0.342 | 0.328 |
| Qwen3-VL-8B-Thinking | 0.428 | 0.394 | 0.428 | 0.833 | 0.194⚠ | 0.275 | 0.289 |
| RynnBrain-2B | 0.422 | 0.233⚠ | 0.278 | 0.578 | 0.294 | 0.242⚠ | 0.100 |
| Cosmos-Reason2-2B | 0.411 | 0.128⚠ | 0.350 | 0.372 | 0.272 | 0.258 | 0.428 |
| Qwen3-VL-2B | 0.278 | 0.139⚠ | 0.244⚠ | 0.489 | 0.233⚠ | 0.233⚠ | 0.128 |
| SenseNova-InternVL3-2B | 0.322 | 0.261 | 0.350 | 0.311 | 0.256 | 0.325 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.339 | 0.294 | 0.306 | 0.094⚠ | 0.194⚠ | 0.258 | 0.139 |

**`make_tea_tianji`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.974 | 0.615 | 0.479 | 0.795 | 0.453 | 0.316 | 0.803 |
| Qwen3-VL-32B | 1.000 | 0.368 | 0.487 | 0.915 | 0.376 | 0.291 | 0.974 |
| Qwen3-VL-30B-A3B | 1.000 | 0.214⚠ | 0.179⚠ | 0.923 | 0.385 | 0.282 | 0.880 |
| RynnBrain1.1-2B | 0.897 | 0.479 | 0.530 | 0.812 | 0.402 | 0.325 | 0.197 |
| Qwen3-VL-8B | 0.983 | 0.299 | 0.162⚠ | 0.778 | 0.419 | 0.291 | 0.846 |
| Qwen3-VL-8B-Thinking | 0.872 | 0.402 | 0.222⚠ | 0.795 | 0.393 | 0.291 | 0.795 |
| RynnBrain-2B | 0.880 | 0.299 | 0.299 | 0.692 | 0.385 | 0.333 | 0.248 |
| Cosmos-Reason2-2B | 0.735 | 0.462 | 0.462 | 0.658 | 0.393 | 0.171⚠ | 0.761 |
| Qwen3-VL-2B | 0.786 | 0.256 | 0.291 | 0.615 | 0.368 | 0.231⚠ | 0.436 |
| SenseNova-InternVL3-2B | 0.325 | 0.410 | 0.427 | 0.368 | 0.333 | 0.376 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.675 | 0.333 | 0.368 | 0.615 | 0.291 | 0.265 | 0.470 |

**`move_gift_tianjihand`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.489 | 0.650 | 0.900 | 0.667 | 0.500 | 0.400 | 0.244 |
| Qwen3-VL-32B | 0.322 | 0.883 | 0.933 | 0.622 | 0.311 | 0.433 | 0.167 |
| Qwen3-VL-30B-A3B | 0.200⚠ | 0.817 | 0.783 | 0.700 | 0.400 | 0.433 | 0.133 |
| RynnBrain1.1-2B | 0.300 | 0.350 | 0.633 | 0.767 | 0.400 | 0.300 | 0.000⚠ |
| Qwen3-VL-8B | 0.300 | 0.683 | 0.767 | 0.678 | 0.322 | 0.267 | 0.156 |
| Qwen3-VL-8B-Thinking | 0.400 | 0.600 | 0.683 | 0.622 | 0.344 | 0.267 | 0.200 |
| RynnBrain-2B | 0.278 | 0.683 | 0.900 | 0.589 | 0.344 | 0.333 | 0.111 |
| Cosmos-Reason2-2B | 0.478 | 0.683 | 0.617 | 0.433 | 0.389 | 0.367 | 0.456 |
| Qwen3-VL-2B | 0.344 | 0.500 | 0.583 | 0.400 | 0.356 | 0.233⚠ | 0.144 |
| SenseNova-InternVL3-2B | 0.289 | 0.267 | 0.733 | 0.378 | 0.344 | 0.300 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.422 | 0.633 | 0.667 | 0.311 | 0.222⚠ | 0.100⚠ | 0.111 |

**`pack_aidkit_gim`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.820 | 0.487 | 0.547 | 0.767 | 0.627 | 0.387 | 0.220 |
| Qwen3-VL-32B | 0.807 | 0.540 | 0.580 | 0.647 | 0.407 | 0.387 | 0.407 |
| Qwen3-VL-30B-A3B | 0.687 | 0.353 | 0.260 | 0.727 | 0.400 | 0.307 | 0.227 |
| RynnBrain1.1-2B | 0.667 | 0.453 | 0.480 | 0.700 | 0.553 | 0.273 | 0.007⚠ |
| Qwen3-VL-8B | 0.793 | 0.507 | 0.507 | 0.633 | 0.440 | 0.293 | 0.107 |
| Qwen3-VL-8B-Thinking | 0.627 | 0.400 | 0.427 | 0.633 | 0.407 | 0.267 | 0.093 |
| RynnBrain-2B | 0.460 | 0.273 | 0.327 | 0.567 | 0.387 | 0.207⚠ | 0.027⚠ |
| Cosmos-Reason2-2B | 0.633 | 0.360 | 0.393 | 0.533 | 0.353 | 0.247⚠ | 0.233 |
| Qwen3-VL-2B | 0.300 | 0.193⚠ | 0.200⚠ | 0.440 | 0.340 | 0.327 | 0.080⚠ |
| SenseNova-InternVL3-2B | 0.453 | 0.380 | 0.407 | 0.313 | 0.287 | 0.267 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.513 | 0.380 | 0.307 | 0.193⚠ | 0.220⚠ | 0.260 | 0.107 |

**`pack_aidkit_tianji`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.650 | 0.742 | 0.758 | 0.883 | 0.367 | 0.425 | 0.075 |
| Qwen3-VL-32B | 0.783 | 0.783 | 0.800 | 0.700 | 0.350 | 0.342 | 0.208 |
| Qwen3-VL-30B-A3B | 0.675 | 0.433 | 0.433 | 0.700 | 0.425 | 0.308 | 0.200 |
| RynnBrain1.1-2B | 0.617 | 0.558 | 0.600 | 0.658 | 0.350 | 0.383 | 0.058⚠ |
| Qwen3-VL-8B | 0.700 | 0.742 | 0.750 | 0.658 | 0.358 | 0.342 | 0.200 |
| Qwen3-VL-8B-Thinking | 0.617 | 0.500 | 0.575 | 0.492 | 0.325 | 0.325 | 0.150 |
| RynnBrain-2B | 0.592 | 0.483 | 0.483 | 0.683 | 0.375 | 0.367 | 0.008✗⚠ |
| Cosmos-Reason2-2B | 0.567 | 0.350 | 0.275 | 0.675 | 0.375 | 0.275 | 0.375 |
| Qwen3-VL-2B | 0.525 | 0.250 | 0.267 | 0.508 | 0.350 | 0.317 | 0.342 |
| SenseNova-InternVL3-2B | 0.625 | 0.283 | 0.342 | 0.275 | 0.308 | 0.342 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.633 | 0.475 | 0.433 | 0.258 | 0.292 | 0.217⚠ | 0.275 |

**`pack_airpods_tianji`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.683 | 0.375 | 0.283 | 0.992 | 0.317 | 0.275 | 0.042 |
| Qwen3-VL-32B | 0.558 | 0.317 | 0.317 | 0.875 | 0.133⚠ | 0.250 | 0.208 |
| Qwen3-VL-30B-A3B | 0.608 | 0.183⚠ | 0.250 | 0.983 | 0.250 | 0.275 | 0.050 |
| RynnBrain1.1-2B | 0.475 | 0.300 | 0.342 | 0.958 | 0.283 | 0.225⚠ | 0.017⚠ |
| Qwen3-VL-8B | 0.525 | 0.233⚠ | 0.275 | 0.925 | 0.250 | 0.267 | 0.042 |
| Qwen3-VL-8B-Thinking | 0.575 | 0.175⚠ | 0.208⚠ | 0.967 | 0.175⚠ | 0.233⚠ | 0.092 |
| RynnBrain-2B | 0.517 | 0.225⚠ | 0.292 | 0.725 | 0.250 | 0.233⚠ | 0.000⚠ |
| Cosmos-Reason2-2B | 0.342 | 0.183⚠ | 0.292 | 0.650 | 0.225⚠ | 0.267 | 0.017⚠ |
| Qwen3-VL-2B | 0.242⚠ | 0.125⚠ | 0.275 | 0.350 | 0.192⚠ | 0.250 | 0.008⚠ |
| SenseNova-InternVL3-2B | 0.317 | 0.142⚠ | 0.292 | 0.417 | 0.350 | 0.317 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.408 | 0.158⚠ | 0.242⚠ | 0.058⚠ | 0.300 | 0.108✗⚠ | 0.058⚠ |

**`pack_gift_gim`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.587 | 0.787 | 0.627 | 0.907 | 0.480 | 0.307 | 0.093 |
| Qwen3-VL-32B | 0.520 | 0.640 | 0.440 | 0.613 | 0.173⚠ | 0.320 | 0.107 |
| Qwen3-VL-30B-A3B | 0.440 | 0.427 | 0.347 | 0.867 | 0.320 | 0.333 | 0.080⚠ |
| RynnBrain1.1-2B | 0.533 | 0.227⚠ | 0.267 | 0.813 | 0.360 | 0.267 | 0.053⚠ |
| Qwen3-VL-8B | 0.293 | 0.587 | 0.387 | 0.800 | 0.227⚠ | 0.280 | 0.000⚠ |
| Qwen3-VL-8B-Thinking | 0.360 | 0.573 | 0.387 | 0.680 | 0.240⚠ | 0.280 | 0.120⚠ |
| RynnBrain-2B | 0.333 | 0.347 | 0.347 | 0.427 | 0.293 | 0.320 | 0.013⚠ |
| Cosmos-Reason2-2B | 0.373 | 0.480 | 0.360 | 0.387 | 0.187⚠ | 0.347 | 0.120 |
| Qwen3-VL-2B | 0.280 | 0.373 | 0.333 | 0.253 | 0.280 | 0.387 | 0.000⚠ |
| SenseNova-InternVL3-2B | 0.320 | 0.293 | 0.333 | 0.360 | 0.213⚠ | 0.280 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.293 | 0.360 | 0.387 | 0.040⚠ | 0.267 | 0.173⚠ | 0.107 |

**`slip_tshirt_gim`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.633 | 0.517 | 0.939 | 0.741 | 0.265 | 0.316 | 0.408 |
| Qwen3-VL-32B | 0.844 | 0.476 | 0.748 | 0.694 | 0.333 | 0.398 | 0.395 |
| Qwen3-VL-30B-A3B | 0.687 | 0.442 | 0.551 | 0.816 | 0.306 | 0.163⚠ | 0.374 |
| RynnBrain1.1-2B | 0.565 | 0.381 | 0.626 | 0.844 | 0.279 | 0.214⚠ | 0.245 |
| Qwen3-VL-8B | 0.483 | 0.299 | 0.578 | 0.687 | 0.313 | 0.245⚠ | 0.272 |
| Qwen3-VL-8B-Thinking | 0.551 | 0.401 | 0.755 | 0.633 | 0.259 | 0.286 | 0.497 |
| RynnBrain-2B | 0.524 | 0.510 | 0.585 | 0.429 | 0.293 | 0.224⚠ | 0.422 |
| Cosmos-Reason2-2B | 0.286 | 0.503 | 0.605 | 0.252 | 0.306 | 0.276 | 0.463 |
| Qwen3-VL-2B | 0.313 | 0.544 | 0.537 | 0.367 | 0.340 | 0.286 | 0.184 |
| SenseNova-InternVL3-2B | 0.551 | 0.238⚠ | 0.463 | 0.306 | 0.245⚠ | 0.286 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.483 | 0.503 | 0.619 | 0.218⚠ | 0.218⚠ | 0.173⚠ | 0.435 |

**`stack_cubes_gim`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.673 | 0.667 | 0.660 | 0.947 | 0.280 | 0.400 | 0.447 |
| Qwen3-VL-32B | 0.833 | 0.533 | 0.627 | 0.513 | 0.313 | 0.327 | 0.853 |
| Qwen3-VL-30B-A3B | 0.700 | 0.620 | 0.607 | 0.907 | 0.300 | 0.293 | 0.580 |
| RynnBrain1.1-2B | 0.620 | 0.473 | 0.473 | 0.827 | 0.273 | 0.240⚠ | 0.047⚠ |
| Qwen3-VL-8B | 0.767 | 0.560 | 0.527 | 0.687 | 0.320 | 0.253 | 0.580 |
| Qwen3-VL-8B-Thinking | 0.667 | 0.567 | 0.513 | 0.700 | 0.193⚠ | 0.220⚠ | 0.487 |
| RynnBrain-2B | 0.500 | 0.413 | 0.467 | 0.607 | 0.340 | 0.213⚠ | 0.107 |
| Cosmos-Reason2-2B | 0.820 | 0.553 | 0.520 | 0.313 | 0.307 | 0.293 | 0.667 |
| Qwen3-VL-2B | 0.660 | 0.247⚠ | 0.240⚠ | 0.360 | 0.300 | 0.260 | 0.300 |
| SenseNova-InternVL3-2B | 0.207⚠ | 0.260 | 0.207⚠ | 0.513 | 0.267 | 0.267 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.580 | 0.533 | 0.587 | 0.120⚠ | 0.247⚠ | 0.200⚠ | 0.340 |

**`stack_cubes_tianjihand`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.987 | 0.827 | 0.907 | 0.960 | 0.647 | 0.260 | 0.593 |
| Qwen3-VL-32B | 1.000 | 0.800 | 0.933 | 0.740 | 0.480 | 0.370 | 0.733 |
| Qwen3-VL-30B-A3B | 1.000 | 0.667 | 0.767 | 1.000 | 0.507 | 0.190⚠ | 0.660 |
| RynnBrain1.1-2B | 0.873 | 0.300 | 0.467 | 0.953 | 0.600 | 0.220⚠ | 0.327 |
| Qwen3-VL-8B | 0.973 | 0.467 | 0.773 | 0.920 | 0.493 | 0.240⚠ | 0.713 |
| Qwen3-VL-8B-Thinking | 0.980 | 0.560 | 0.687 | 0.827 | 0.507 | 0.270 | 0.447 |
| RynnBrain-2B | 0.853 | 0.327 | 0.640 | 0.960 | 0.447 | 0.220⚠ | 0.313 |
| Cosmos-Reason2-2B | 0.973 | 0.653 | 0.707 | 0.607 | 0.353 | 0.300 | 0.467 |
| Qwen3-VL-2B | 0.880 | 0.367 | 0.413 | 0.320 | 0.320 | 0.210⚠ | 0.307 |
| SenseNova-InternVL3-2B | 0.567 | 0.560 | 0.607 | 0.387 | 0.320 | 0.240⚠ | 0.000⚠ |
| Cosmos3-Edge-2B | 0.660 | 0.487 | 0.547 | 0.273 | 0.220⚠ | 0.030✗⚠ | 0.207 |

**`takeout_trash_tianji`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.950 | 0.825 | 0.808 | 0.867 | 0.433 | 0.167⚠ | 0.267 |
| Qwen3-VL-32B | 0.942 | 0.825 | 0.858 | 0.733 | 0.342 | 0.158⚠ | 0.333 |
| Qwen3-VL-30B-A3B | 0.892 | 0.825 | 0.725 | 0.925 | 0.392 | 0.158⚠ | 0.308 |
| RynnBrain1.1-2B | 0.875 | 0.567 | 0.525 | 0.908 | 0.367 | 0.167⚠ | 0.050⚠ |
| Qwen3-VL-8B | 0.925 | 0.775 | 0.825 | 0.683 | 0.317 | 0.192⚠ | 0.200 |
| Qwen3-VL-8B-Thinking | 0.733 | 0.608 | 0.633 | 0.808 | 0.258 | 0.192⚠ | 0.383 |
| RynnBrain-2B | 0.892 | 0.742 | 0.675 | 0.908 | 0.392 | 0.150⚠ | 0.033⚠ |
| Cosmos-Reason2-2B | 0.892 | 0.750 | 0.700 | 0.900 | 0.350 | 0.167⚠ | 0.183 |
| Qwen3-VL-2B | 0.908 | 0.650 | 0.550 | 0.483 | 0.342 | 0.225⚠ | 0.108 |
| SenseNova-InternVL3-2B | 0.608 | 0.567 | 0.458 | 0.550 | 0.325 | 0.158⚠ | 0.000⚠ |
| Cosmos3-Edge-2B | 0.675 | 0.417 | 0.400 | 0.408 | 0.275 | 0.250 | 0.258 |

**`wash_dishes_tianji`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.858 | 0.342 | 0.392 | 0.742 | 0.575 | 0.333 | 0.208 |
| Qwen3-VL-32B | 0.758 | 0.325 | 0.417 | 0.600 | 0.450 | 0.325 | 0.408 |
| Qwen3-VL-30B-A3B | 0.825 | 0.475 | 0.483 | 0.833 | 0.333 | 0.267 | 0.408 |
| RynnBrain1.1-2B | 0.750 | 0.417 | 0.433 | 0.775 | 0.458 | 0.142⚠ | 0.142 |
| Qwen3-VL-8B | 0.725 | 0.425 | 0.475 | 0.517 | 0.283 | 0.208⚠ | 0.367 |
| Qwen3-VL-8B-Thinking | 0.550 | 0.350 | 0.367 | 0.708 | 0.400 | 0.200⚠ | 0.358 |
| RynnBrain-2B | 0.642 | 0.442 | 0.483 | 0.642 | 0.350 | 0.175⚠ | 0.033⚠ |
| Cosmos-Reason2-2B | 0.633 | 0.325 | 0.325 | 0.558 | 0.400 | 0.275 | 0.333 |
| Qwen3-VL-2B | 0.550 | 0.317 | 0.342 | 0.367 | 0.292 | 0.167⚠ | 0.283 |
| SenseNova-InternVL3-2B | 0.450 | 0.267 | 0.200⚠ | 0.517 | 0.267 | 0.208⚠ | 0.000⚠ |
| Cosmos3-Edge-2B | 0.392 | 0.308 | 0.358 | 0.225⚠ | 0.275 | 0.167⚠ | 0.217 |

**`wipe_plate_gim`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.693 | 0.273 | 0.200⚠ | 0.647 | 0.373 | 0.247⚠ | 0.347 |
| Qwen3-VL-32B | 0.713 | 0.387 | 0.313 | 0.573 | 0.267 | 0.327 | 0.393 |
| Qwen3-VL-30B-A3B | 0.587 | 0.300 | 0.280 | 0.653 | 0.280 | 0.233⚠ | 0.387 |
| RynnBrain1.1-2B | 0.553 | 0.347 | 0.273 | 0.640 | 0.353 | 0.173⚠ | 0.000⚠ |
| Qwen3-VL-8B | 0.540 | 0.267 | 0.193⚠ | 0.413 | 0.267 | 0.220⚠ | 0.253 |
| Qwen3-VL-8B-Thinking | 0.507 | 0.187⚠ | 0.153⚠ | 0.547 | 0.233⚠ | 0.207⚠ | 0.240 |
| RynnBrain-2B | 0.507 | 0.160⚠ | 0.087⚠ | 0.407 | 0.280 | 0.173⚠ | 0.040⚠ |
| Cosmos-Reason2-2B | 0.367 | 0.247⚠ | 0.140⚠ | 0.347 | 0.293 | 0.293 | 0.320 |
| Qwen3-VL-2B | 0.393 | 0.273 | 0.173⚠ | 0.393 | 0.300 | 0.233⚠ | 0.167 |
| SenseNova-InternVL3-2B | 0.487 | 0.187⚠ | 0.113⚠ | 0.380 | 0.233⚠ | 0.180⚠ | 0.000⚠ |
| Cosmos3-Edge-2B | 0.333 | 0.220⚠ | 0.280 | 0.147⚠ | 0.260 | 0.140⚠ | 0.327 |

## Appendix B. Per-scenario results — suite v2 (dataset 2.1)

### Scenarios

| Scenario | Embodiment | Views | fps | Resolution | Episodes | Questions |
| --- | --- | :--: | ---: | :--: | ---: | ---: |
| `box_pen_hand` | hand | 1 | 24 | 1920×1920 | 40 | 680 |
| `box_shoe_tianji` | tianji | 3 | 25 | 770×398 | 40 | 671 |
| `move_flower_hand` | hand | 1 | 24 | 1920×1920 | 40 | 160 |
| `pack_express_tianji` | tianji | 3 | 30 | 640×480 | 50 | 1000 |
| `pack_gift_tianji` | tianji | 3 | 30 | 640×480 | 41 | 861 |
| `pack_sunglasses_hand` | hand | 1 | 24 | 1920×1920 | 41 | 738 |
| `sort_cubes_tianji` | tianji | 3 | 30 | 640×480 | 41 | 861 |
| `stack_cubes_hand` | hand | 1 | 24 | 1920×1920 | 43 | 731 |
| `stow_sunglasses_tianjihand` | tianjihand | 3 | 30 | 640×480 | 50 | 850 |
| `tidy_stationery_tianji` | tianji | 3 | 30 | 640×480 | 63 | 1260 |

### Scenario difficulty — mean over the 11 models

Not-measured cells (✗) are excluded from these means; `n/a` means the dataset asks nothing there. `Choice mean` averages the six choice dimensions only.

| Scenario | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time | Choice mean |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `box_pen_hand` | 0.764 | 0.373 | 0.394 | 0.752 | n/a | 0.270 | 0.442 | **0.511** |
| `box_shoe_tianji` | 0.940 | 0.892 | 0.898 | 0.617 | 0.375 | 0.373 | 0.397 | **0.682** |
| `move_flower_hand` | 0.881 | n/a | n/a | n/a | n/a | n/a | 0.518 | **0.881** |
| `pack_express_tianji` | 0.452 | 0.280 | 0.401 | 0.724 | 0.239 | 0.295 | 0.280 | **0.398** |
| `pack_gift_tianji` | 0.530 | 0.264 | 0.268 | 0.627 | 0.369 | 0.342 | 0.203 | **0.400** |
| `pack_sunglasses_hand` | 0.749 | 0.532 | 0.499 | 0.538 | n/a | 0.315 | 0.337 | **0.527** |
| `sort_cubes_tianji` | 0.729 | 0.738 | 0.705 | 0.670 | 0.394 | 0.272 | 0.161 | **0.585** |
| `stack_cubes_hand` | 0.849 | 0.566 | 0.657 | 0.662 | n/a | 0.312 | 0.431 | **0.609** |
| `stow_sunglasses_tianjihand` | 0.436 | 0.569 | 0.608 | 0.699 | 0.350 | 0.295 | 0.318 | **0.493** |
| `tidy_stationery_tianji` | 0.383 | 0.486 | 0.531 | 0.730 | 0.284 | 0.364 | 0.216 | **0.463** |

### Per-scenario detail

`✗` = not measured (majority of answers unparseable; excluded from every mean in
this document). `⚠` = at or below the degenerate floor. `n/a` = the dataset asks
no questions there. A cell can carry both marks.


**`box_pen_hand`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.783 | 0.458 | 0.600 | 0.958 | n/a | 0.300 | 0.683 |
| Qwen3-VL-30B-A3B | 0.900 | 0.458 | 0.417 | 0.983 | n/a | 0.325 | 0.875 |
| Qwen3-VL-32B | 0.833 | 0.550 | 0.775 | 0.842 | n/a | 0.225⚠ | 0.567 |
| RynnBrain1.1-2B | 0.775 | 0.442 | 0.558 | 0.967 | n/a | 0.263 | 0.383 |
| Qwen3-VL-8B | 0.750 | 0.175⚠ | 0.150⚠ | 0.883 | n/a | 0.312 | 0.517 |
| Qwen3-VL-8B-Thinking | 0.700 | 0.467 | 0.408 | 0.933 | n/a | 0.300 | 0.692 |
| RynnBrain-2B | 0.842 | 0.217⚠ | 0.158⚠ | 0.983 | n/a | 0.237⚠ | 0.233 |
| Cosmos-Reason2-2B | 0.783 | 0.375 | 0.250 | 0.617 | n/a | 0.237⚠ | 0.367 |
| Qwen3-VL-2B | 0.642 | 0.350 | 0.225⚠ | 0.275 | n/a | 0.250 | 0.058⚠ |
| SenseNova-InternVL3-2B | 0.458 | 0.208⚠ | 0.367 | 0.533 | n/a | 0.275 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.933 | 0.408 | 0.425 | 0.300 | n/a | 0.250 | 0.483 |

**`box_shoe_tianji`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.992 | 1.000 | 1.000 | 0.718 | 0.546 | 0.308 | 0.487 |
| Qwen3-VL-30B-A3B | 1.000 | 0.987 | 0.987 | 0.658 | 0.471 | 0.333 | 0.361 |
| Qwen3-VL-32B | 1.000 | 1.000 | 1.000 | 0.667 | 0.303 | 0.436 | 0.429 |
| RynnBrain1.1-2B | 0.992 | 0.861 | 0.848 | 0.812 | 0.529 | 0.308 | 0.303 |
| Qwen3-VL-8B | 0.992 | 1.000 | 1.000 | 0.496 | 0.412 | 0.410 | 0.370 |
| Qwen3-VL-8B-Thinking | 0.941 | 0.823 | 0.835 | 0.718 | 0.370 | 0.564 | 0.437 |
| RynnBrain-2B | 0.992 | 0.987 | 0.975 | 0.658 | 0.378 | 0.308 | 0.311 |
| Cosmos-Reason2-2B | 0.882 | 0.962 | 0.873 | 0.650 | 0.336 | 0.282 | 0.655 |
| Qwen3-VL-2B | 0.941 | 0.987 | 0.924 | 0.496 | 0.286 | 0.436 | 0.445 |
| SenseNova-InternVL3-2B | 0.899 | 0.696 | 0.975 | 0.368 | 0.277 | 0.436 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.714 | 0.506 | 0.456 | 0.547 | 0.218⚠ | 0.282 | 0.571 |

**`move_flower_hand`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 1.000 | n/a | n/a | n/a | n/a | n/a | 0.925 |
| Qwen3-VL-30B-A3B | 0.988 | n/a | n/a | n/a | n/a | n/a | 0.825 |
| Qwen3-VL-32B | 0.925 | n/a | n/a | n/a | n/a | n/a | 0.375 |
| RynnBrain1.1-2B | 0.825 | n/a | n/a | n/a | n/a | n/a | 0.463 |
| Qwen3-VL-8B | 0.925 | n/a | n/a | n/a | n/a | n/a | 0.512 |
| Qwen3-VL-8B-Thinking | 0.838 | n/a | n/a | n/a | n/a | n/a | 0.825 |
| RynnBrain-2B | 0.825 | n/a | n/a | n/a | n/a | n/a | 0.412 |
| Cosmos-Reason2-2B | 0.988 | n/a | n/a | n/a | n/a | n/a | 0.487 |
| Qwen3-VL-2B | 0.762 | n/a | n/a | n/a | n/a | n/a | 0.362 |
| SenseNova-InternVL3-2B | 0.613 | n/a | n/a | n/a | n/a | n/a | 0.000⚠ |
| Cosmos3-Edge-2B | 1.000 | n/a | n/a | n/a | n/a | n/a | 0.512 |

**`pack_express_tianji`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.593 | 0.287 | 0.380 | 0.727 | 0.420 | 0.310 | 0.540 |
| Qwen3-VL-30B-A3B | 0.647 | 0.127⚠ | 0.293 | 0.927 | 0.193⚠ | 0.300 | 0.180 |
| Qwen3-VL-32B | 0.607 | 0.307 | 0.313 | 0.920 | 0.173⚠ | 0.260 | 0.547 |
| RynnBrain1.1-2B | 0.347 | 0.193⚠ | 0.487 | 0.873 | 0.247⚠ | 0.230⚠ | 0.267 |
| Qwen3-VL-8B | 0.573 | 0.207⚠ | 0.260 | 0.713 | 0.260 | 0.280 | 0.347 |
| Qwen3-VL-8B-Thinking | 0.500 | 0.380 | 0.413 | 0.773 | 0.233⚠ | 0.320 | 0.593 |
| RynnBrain-2B | 0.373 | 0.100⚠ | 0.340 | 0.833 | 0.193⚠ | 0.300 | 0.087 |
| Cosmos-Reason2-2B | 0.387 | 0.393 | 0.627 | 0.733 | 0.267 | 0.340 | 0.267 |
| Qwen3-VL-2B | 0.380 | 0.480 | 0.547 | 0.813 | 0.293 | 0.350 | 0.173 |
| SenseNova-InternVL3-2B | 0.307 | 0.300 | 0.400 | 0.407 | 0.220⚠ | 0.270 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.260 | 0.307 | 0.347 | 0.240⚠ | 0.127⚠ | 0.280 | 0.080 |

**`pack_gift_tianji`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.756 | 0.309 | 0.154⚠ | 0.886 | 0.528 | 0.447 | 0.407 |
| Qwen3-VL-30B-A3B | 0.675 | 0.203⚠ | 0.317 | 0.870 | 0.333 | 0.390 | 0.276 |
| Qwen3-VL-32B | 0.683 | 0.211⚠ | 0.260 | 0.650 | 0.341 | 0.407 | 0.382 |
| RynnBrain1.1-2B | 0.634 | 0.252 | 0.179⚠ | 0.805 | 0.650 | 0.358 | 0.016⚠ |
| Qwen3-VL-8B | 0.415 | 0.382 | 0.390 | 0.724 | 0.350 | 0.382 | 0.309 |
| Qwen3-VL-8B-Thinking | 0.415 | 0.407 | 0.350 | 0.593 | 0.268 | 0.317 | 0.236 |
| RynnBrain-2B | 0.626 | 0.154⚠ | 0.138⚠ | 0.724 | 0.317 | 0.366 | 0.122 |
| Cosmos-Reason2-2B | 0.488 | 0.325 | 0.268 | 0.496 | 0.496 | 0.252 | 0.252 |
| Qwen3-VL-2B | 0.569 | 0.268 | 0.325 | 0.407 | 0.236⚠ | 0.325 | 0.073 |
| SenseNova-InternVL3-2B | 0.285 | 0.203⚠ | 0.333 | 0.317 | 0.211⚠ | 0.358 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.285 | 0.187⚠ | 0.236⚠ | 0.431 | 0.325 | 0.163⚠ | 0.163 |

**`pack_sunglasses_hand`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.780 | 0.854 | 0.984 | 0.683 | n/a | 0.390 | 0.528 |
| Qwen3-VL-30B-A3B | 0.854 | 0.691 | 0.829 | 0.740 | n/a | 0.325 | 0.634 |
| Qwen3-VL-32B | 0.748 | 0.626 | 0.821 | 0.642 | n/a | 0.374 | 0.260 |
| RynnBrain1.1-2B | 0.870 | 0.447 | 0.480 | 0.846 | n/a | 0.301 | 0.057 |
| Qwen3-VL-8B | 0.707 | 0.593 | 0.593 | 0.577 | n/a | 0.350 | 0.431 |
| Qwen3-VL-8B-Thinking | 0.764 | 0.553 | 0.455 | 0.569 | n/a | 0.301 | 0.333 |
| RynnBrain-2B | 0.764 | 0.553 | 0.382 | 0.724 | n/a | 0.293 | 0.374 |
| Cosmos-Reason2-2B | 0.724 | 0.512 | 0.211⚠ | 0.317 | n/a | 0.285 | 0.374 |
| Qwen3-VL-2B | 0.659 | 0.220⚠ | 0.106⚠ | 0.163⚠ | n/a | 0.317 | 0.382 |
| SenseNova-InternVL3-2B | 0.431 | 0.244⚠ | 0.171⚠ | 0.431 | n/a | 0.309 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.935 | 0.561 | 0.455 | 0.228⚠ | n/a | 0.220⚠ | 0.333 |

**`sort_cubes_tianji`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.935 | 0.935 | 0.951 | 0.976 | 0.496 | 0.301 | 0.211 |
| Qwen3-VL-30B-A3B | 0.927 | 0.878 | 0.870 | 0.984 | 0.398 | 0.268 | 0.236 |
| Qwen3-VL-32B | 0.902 | 0.894 | 0.943 | 0.813 | 0.439 | 0.317 | 0.333 |
| RynnBrain1.1-2B | 0.821 | 0.626 | 0.724 | 0.967 | 0.512 | 0.244⚠ | 0.220 |
| Qwen3-VL-8B | 0.911 | 0.919 | 0.911 | 0.756 | 0.407 | 0.285 | 0.081 |
| Qwen3-VL-8B-Thinking | 0.683 | 0.878 | 0.886 | 0.846 | 0.382 | 0.260 | 0.171 |
| RynnBrain-2B | 0.707 | 0.821 | 0.748 | 0.772 | 0.455 | 0.293 | 0.268 |
| Cosmos-Reason2-2B | 0.626 | 0.626 | 0.569 | 0.398 | 0.276 | 0.268 | 0.033 |
| Qwen3-VL-2B | 0.496 | 0.252 | 0.171⚠ | 0.317 | 0.407 | 0.228⚠ | 0.041 |
| SenseNova-InternVL3-2B | 0.382 | 0.642 | 0.463 | 0.341 | 0.350 | 0.260 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.634 | 0.650 | 0.520 | 0.203⚠ | 0.211⚠ | 0.106✗⚠ | 0.179 |

**`stack_cubes_hand`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.930 | 0.860 | 0.922 | 0.984 | n/a | 0.430 | 0.667 |
| Qwen3-VL-30B-A3B | 0.984 | 0.643 | 0.721 | 0.930 | n/a | 0.360 | 0.674 |
| Qwen3-VL-32B | 0.984 | 0.721 | 0.806 | 0.550 | n/a | 0.430 | 0.628 |
| RynnBrain1.1-2B | 0.791 | 0.364 | 0.558 | 0.969 | n/a | 0.384 | 0.395 |
| Qwen3-VL-8B | 1.000 | 0.620 | 0.667 | 0.806 | n/a | 0.326 | 0.690 |
| Qwen3-VL-8B-Thinking | 0.822 | 0.574 | 0.760 | 0.837 | n/a | 0.395 | 0.535 |
| RynnBrain-2B | 0.783 | 0.558 | 0.721 | 0.814 | n/a | 0.221⚠ | 0.434 |
| Cosmos-Reason2-2B | 0.868 | 0.504 | 0.674 | 0.465 | n/a | 0.244⚠ | 0.357 |
| Qwen3-VL-2B | 0.729 | 0.318 | 0.271 | 0.240⚠ | n/a | 0.233⚠ | 0.140 |
| SenseNova-InternVL3-2B | 0.481 | 0.450 | 0.372 | 0.512 | n/a | 0.302 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.969 | 0.612 | 0.752 | 0.171⚠ | n/a | 0.105⚠ | 0.225 |

**`stow_sunglasses_tianjihand`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.473 | 0.760 | 0.670 | 0.980 | 0.547 | 0.320 | 0.467 |
| Qwen3-VL-30B-A3B | 0.540 | 0.590 | 0.820 | 0.980 | 0.307 | 0.300 | 0.540 |
| Qwen3-VL-32B | 0.587 | 0.570 | 0.500 | 0.700 | 0.313 | 0.320 | 0.467 |
| RynnBrain1.1-2B | 0.507 | 0.530 | 0.560 | 0.907 | 0.440 | 0.300 | 0.307 |
| Qwen3-VL-8B | 0.380 | 0.430 | 0.630 | 0.787 | 0.347 | 0.400 | 0.487 |
| Qwen3-VL-8B-Thinking | 0.447 | 0.680 | 0.880 | 0.833 | 0.433 | 0.320 | 0.413 |
| RynnBrain-2B | 0.287 | 0.680 | 0.670 | 0.807 | 0.433 | 0.300 | 0.213 |
| Cosmos-Reason2-2B | 0.373 | 0.620 | 0.410 | 0.660 | 0.260 | 0.240⚠ | 0.320 |
| Qwen3-VL-2B | 0.327 | 0.480 | 0.510 | 0.387 | 0.313 | 0.300 | 0.140 |
| SenseNova-InternVL3-2B | 0.440 | 0.540 | 0.560 | 0.413 | 0.200⚠ | 0.320 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.433 | 0.380 | 0.480 | 0.240⚠ | 0.253 | 0.120⚠ | 0.147 |

**`tidy_stationery_tianji`**

| Model | Cur | Next | Next+G | FrmMat | ViewMat | FrmOrd | Time |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| RynnBrain1.1-9B | 0.481 | 0.487 | 0.619 | 0.989 | 0.381 | 0.508 | 0.291✗ |
| Qwen3-VL-30B-A3B | 0.519 | 0.566 | 0.725 | 1.000 | 0.265 | 0.333 | 0.392 |
| Qwen3-VL-32B | 0.444 | 0.556 | 0.587 | 0.762 | 0.243⚠ | 0.413 | 0.344 |
| RynnBrain1.1-2B | 0.370 | 0.407 | 0.302 | 0.979 | 0.386 | 0.317 | 0.190 |
| Qwen3-VL-8B | 0.466 | 0.503 | 0.677 | 0.979 | 0.333 | 0.349 | 0.169 |
| Qwen3-VL-8B-Thinking | 0.444 | 0.450 | 0.450 | 0.963 | 0.217⚠ | 0.333 | 0.291 |
| RynnBrain-2B | 0.302 | 0.508 | 0.672 | 0.804 | 0.429 | 0.389 | 0.296 |
| Cosmos-Reason2-2B | 0.360 | 0.603 | 0.534 | 0.471 | 0.238⚠ | 0.405 | 0.222 |
| Qwen3-VL-2B | 0.169⚠ | 0.444 | 0.349 | 0.397 | 0.265 | 0.349 | 0.175 |
| SenseNova-InternVL3-2B | 0.280 | 0.450 | 0.550 | 0.439 | 0.233⚠ | 0.437 | 0.000⚠ |
| Cosmos3-Edge-2B | 0.381 | 0.370 | 0.370 | 0.243⚠ | 0.138⚠ | 0.167⚠ | 0.079 |
