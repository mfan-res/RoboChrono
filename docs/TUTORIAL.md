# Running RoboChrono on a fresh machine

Two paths through this guide. **Part 1** runs local models on a GPU cluster;
**Part 2** runs API-served models and needs no GPU at all. Both start from a
machine with nothing on it.

Wherever a command mentions a model list, substitute the models you were
assigned. The worked examples below use the current assignments:

- **GPU cluster (4×H100)**: `rynnbrain1-1-122b-a10b`, `internvl3-2b`
- **API**: `qwen3-8-max`, `qwen3-8-max-thinking`, `gemini-3-6-flash`,
  `doubao-seed-2-0-lite`, `qwen3-vl-235b-a22b-api`

---

## Part 1 — GPU cluster

### 1.0 What you need

| Requirement | Why |
| --- | --- |
| Linux, NVIDIA driver ≥ CUDA 12.4 | the pinned torch build is cu124 |
| `git`, `ffmpeg` (with `ffprobe`) | clone; media probing and shrinking |
| ~60 GB disk for data, plus your models' weights (122B alone is 229 GB) | see table in 1.4 |
| A Hugging Face token with access to `GIM-RoboLab/robochrono` | the dataset is private during review |
| [`uv`](https://docs.astral.sh/uv/) | builds the two Python environments |

Install `uv` if missing:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1.1 Clone

```bash
git clone https://github.com/mfan-res/RoboChrono.git
cd RoboChrono
```

Everything below happens inside this directory. Data, weights and results all
live under it — nothing is installed system-wide.

### 1.2 Build the two environments

Two are required, not one: some model families only load under
transformers 4.x, others only under 5.x. The evaluator switches between them
automatically at run time; you only build them.

```bash
uv python install 3.11
UV_PROJECT_ENVIRONMENT=.venvs/tf4 uv sync --extra tf4
UV_PROJECT_ENVIRONMENT=.venvs/tf5 uv sync --extra tf5
```

Which models need which environment is declared in
`configs/models/local/*.json` (`environment` field); you never activate
either by hand.

### 1.3 Download the dataset

```bash
hf auth login          # paste your token once
hf download GIM-RoboLab/robochrono --repo-type dataset --local-dir /tmp/robochrono-dl
for t in /tmp/robochrono-dl/vqa_2/*.tar; do tar -xf "$t" -C data/; done
cp /tmp/robochrono-dl/vqa_2/manifest.json /tmp/robochrono-dl/vqa_2/README.md data/
cp -r /tmp/robochrono-dl/vqa_2/qa data/

.venvs/tf4/bin/python -m robochrono validate-data
```

The last command must end with `all checks passed` — 13,636 questions,
18,540 media files, none missing. If it does not, stop and re-download;
nothing downstream can repair missing data.

### 1.4 Download your models' weights

Weights go under `models/<name>` — the exact directory names below matter,
they are what `configs/models/local/*.json` declares:

```bash
mkdir -p models
hf download Alibaba-DAMO-Academy/RynnBrain1.1-122B-A10B --local-dir models/RynnBrain1_1-122B-A10B
hf download OpenGVLab/InternVL3-2B                       --local-dir models/InternVL3-2B
```

InternVL-family models need one small edit so their code loads from the local
directory instead of reaching for the hub at run time:

```bash
.venvs/tf4/bin/python - << 'PY'
import json
p = "models/InternVL3-2B/config.json"
cfg = json.load(open(p))
cfg["auto_map"] = {k: v.split("--", 1)[-1] for k, v in cfg["auto_map"].items()}
json.dump(cfg, open(p, "w"), indent=2)
print("patched", p)
PY
```

### 1.5 Preflight

```bash
.venvs/tf4/bin/python -m robochrono preflight \
  --models rynnbrain1-1-122b-a10b internvl3-2b
```

Every line must be OK or SKIP. Each FAIL names what is missing and how to fix
it. Do not proceed past a FAIL — the whole point of preflight is that a
problem found here costs a minute, and the same problem found mid-run costs
hours.

### 1.6 Smoke test (10 minutes)

One small slice through the real pipeline before committing to the long run:

```bash
python3 -m robochrono eval \
  --models internvl3-2b \
  --scenarios make_tea_tianji --dimensions current_action \
  --limit-items 8 --gpus 4
```

Expected: a `results/<date>_<fingerprint>/` directory appears, the log ends
with a `report.md` line, and the summary inside shows `errors: 0`.

### 1.7 The full run

```bash
nohup python3 -m robochrono eval \
  --models rynnbrain1-1-122b-a10b internvl3-2b \
  --gpus 4 > full_run.log 2>&1 &
```

Notes on what happens:

- No `--scenarios` flag means all 15 scenarios; expect roughly **30 hours**
  for this two-model assignment (the 122B is the bulk of it).
- Models run one at a time; all four GPUs work on the current model. The
  122B needs all 4 GPUs per copy — that is declared in its configuration,
  nothing to set.
- Every answered question is written to disk immediately. Killing the run
  loses at most the questions in flight.

### 1.8 Monitoring

```bash
tail -f full_run.log                          # everything
grep -E "pool: |ABORTED|error: " full_run.log # the lines that matter
nvidia-smi                                    # GPUs busy?
```

What the lines mean:

- `[model] pool: N pending unit(s)` — a new model started.
- `[k/N] 12.3 unit/min errors=E` — progress; a nonzero error count is not an
  emergency (see below).
- `ABORTED — circuit breaker` — twenty consecutive failures; something is
  systematically wrong. Read the nearest `error:` lines and get in touch.

**If the machine reboots or you kill the run**: run the exact same command
again. It finds its directory by configuration fingerprint and continues
where it stopped — already-answered questions are never redone.

**If the finished run shows a few errors** (out-of-memory on the longest
videos is the known kind): rerun the same command with
`--gpus-per-worker 2` appended. Only the failed questions are retried, with
two GPUs per model copy.

### 1.9 Ship the results back

```bash
python3 -m robochrono report          # prints the table location
python3 -m robochrono pack            # results/<run_id>.tar.gz, a few hundred KB
python3 -m robochrono pack --full     # adds per-question records (hundreds of MB)
```

Send the default pack. Keep the full per-question records on the machine —
they are the raw material for any later analysis.

---

## Part 2 — API models

No GPU, no weights, no heavy environments — any Linux machine with Python
3.11+ and `ffmpeg` works. Do steps 1.1 and 1.3 above (clone + dataset), then:

### 2.1 Keys

```bash
mkdir -p ~/.config/robochrono
cat > ~/.config/robochrono/keys.env << 'K'
DASHSCOPE_API_KEY=...       # Qwen3.8-Max, both arms, and the 235B
GEMINI_API_KEY=...          # Gemini
ARK_API_KEY=...             # Doubao
K
chmod 600 ~/.config/robochrono/keys.env
```

Keys never go into the repository or into any configuration file; the model
configurations name the environment variable, and you load them per shell:

```bash
set -a; source ~/.config/robochrono/keys.env; set +a
```

If your network cannot reach Google directly, the Gemini model configuration
carries a `proxy` field (`configs/models/api/gemini-3-6-flash.json`) — point
it at your proxy URL.

### 2.2 A minimal environment and a preflight

```bash
UV_PROJECT_ENVIRONMENT=.venvs/api uv venv .venvs/api --python 3.11
uv pip install --python .venvs/api/bin/python requests pillow numpy
.venvs/api/bin/python -m robochrono preflight --only api
```

### 2.3 One-question probe per model (pennies)

```bash
for m in qwen3-8-max qwen3-8-max-thinking gemini-3-6-flash \
         doubao-seed-2-0-lite qwen3-vl-235b-a22b-api; do
  .venvs/api/bin/python -m robochrono eval --models "$m" \
    --scenarios make_tea_tianji --dimensions current_action \
    --limit-items 1 --no-dispatch
done
```

Every probe should answer with `errors=0`. This confirms keys, media upload,
and that each provider's thinking switch behaves as configured.

### 2.4 The run

```bash
nohup .venvs/api/bin/python -m robochrono eval \
  --models qwen3-8-max qwen3-8-max-thinking gemini-3-6-flash \
           doubao-seed-2-0-lite qwen3-vl-235b-a22b-api \
  --no-dispatch --api-concurrency 8 > api_run.log 2>&1 &
```

Two things to know:

- The 235B endpoint rate-limits harder than the rest. If its section of the
  log fills with `429`, let the run finish, then rerun the same command with
  `--api-concurrency 2` — only its failed questions are retried.
- Cost scales with what you select. `--limit-items N` caps questions per
  (scenario, dimension) if a sampled run is wanted instead of the full one;
  agree on the budget before launching the full thing.

Monitoring, interruption recovery and shipping results are identical to
sections 1.8–1.9.
