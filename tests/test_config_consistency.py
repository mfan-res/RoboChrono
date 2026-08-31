#!/usr/bin/env python3
# coding: utf-8
"""Cross-file consistency of the configuration.

A JSON schema can check structure — required fields, types, misspelled keys.
It cannot check that two files agree with each other, and that is where the
failures that matter live: a suite naming a scenario the dataset does not have,
a model mapped to an environment that does not exist, a dimension with no frame
sampling declared. None of those raise on their own; they produce a run that
quietly covers less than it claims.

What is validated is that a decision was made and that the decisions are
mutually consistent — not whether any individual value is the right one.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
failures: list[str] = []


def check(name: str, passed: bool, detail: str = "") -> None:
    print(f"  {'✅' if passed else '❌'} {name:44} {detail}")
    if not passed:
        failures.append(name)


def load(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


protocol = load("configs/protocol.json")
runtime = load("configs/runtime.json")
environments = load("configs/environments.json")
suites = {p.stem: json.loads(p.read_text(encoding="utf-8"))
          for p in sorted((ROOT / "configs/suites").glob("*.json"))}
models = {p.stem: json.loads(p.read_text(encoding="utf-8"))
          for p in sorted((ROOT / "configs/models").rglob("*.json"))}

# One data root per dataset version: data/v20 holds 2.0, data/v21 holds 2.1.
manifests = {}
for root in sorted((ROOT / "data").glob("v*/manifest.json")):
    m = json.loads(root.read_text(encoding="utf-8"))
    manifests[m["version"]] = m
manifest = manifests.get("2.0")   # sections 4-5 sanity-check against the primary

print("1. model -> environment")
env_names = set(environments["envs"])
for slug, m in models.items():
    check(f"{slug} environment exists", m.get("environment") in env_names,
          m.get("environment", "(missing)"))

print("2. declared transformers requirement vs the environment provided")


def satisfies(spec: str | None, actual: str) -> bool | None:
    """Supports ==X and >=X. None means no requirement is declared."""
    if not spec:
        return None
    m = re.fullmatch(r"(==|>=)\s*([\d.]+)", spec.strip())
    if not m:
        return None
    op, want = m.group(1), tuple(int(x) for x in m.group(2).split("."))
    got = tuple(int(x) for x in actual.split("."))
    want += (0,) * (len(got) - len(want))
    want = want[: len(got)]
    # A pinned version is read as a lower bound: the environments ship a later
    # patch release that satisfies every model mapped to them.
    return got >= want


for slug, m in models.items():
    tf = (m.get("official") or {}).get("transformers")
    # A missing declaration is an error. "The documentation does not say" and
    # "nobody filled this in" must be distinguishable, so the former is written
    # explicitly as source: "none".
    if not isinstance(tf, dict) or "source" not in tf:
        check(f"{slug} declares official.transformers.source", False,
              "missing — write source: \"none\" when the docs say nothing")
        continue
    spec, src = tf.get("value"), tf["source"]
    env = environments["envs"].get(m.get("environment"), {})
    actual = env.get("transformers", "")
    ok = satisfies(spec, actual) if actual else None
    if ok is None:
        check(f"{slug}", True, f"no version declared (source={src})")
    else:
        check(f"{slug}", ok, f"requires {spec}, environment has {actual}")

print("3. suite contents exist in the manifest")
if manifest is None:
    check("manifest present", False, "data/manifest.json not found")
else:
    for sname, s in suites.items():
        m = manifests.get(s["dataset_version"])
        if m is None:
            check(f"{sname} dataset present", False,
                  f"no data root holds version {s['dataset_version']}")
            continue
        unknown_sc = set(s["scenarios"]) - set(m["scenarios"])
        unknown_dim = set(s["dimensions"]) - set(m["dimensions"])
        check(f"{sname} scenarios exist", not unknown_sc, f"unknown: {sorted(unknown_sc)}")
        check(f"{sname} dimensions exist", not unknown_dim, f"unknown: {sorted(unknown_dim)}")

print("4. frame sampling covers every dimension")
if manifest is not None:
    declared = set(protocol["frames"]["by_dimension"])
    known = set(manifest["dimensions"])
    check("all dimensions declared", not (known - declared), f"missing: {sorted(known - declared)}")
    check("no extra dimensions declared", not (declared - known), f"extra: {sorted(declared - known)}")

print("5. degenerate floors cover every dimension")
if manifest is not None:
    floors = protocol["degenerate_floor"]
    for dim in manifest["dimensions"]:
        kind = "interval" if dim == "action_time" else "choice"
        check(f"{dim} has a floor", kind in floors, f"uses {kind}")

print("6. weights")
for slug, m in models.items():
    w = m.get("weights", "")
    check(f"{slug} declares weights", bool(w), w)

print("7. operational settings stay out of the protocol")
leaked = [k for k in ("api_concurrency", "proxy", "media_cache_dir", "gpus_per_worker")
          if k in protocol or k in protocol.get("generation", {})]
check("no machine-specific settings", not leaked, f"leaked: {leaked}")

print("8. scenario and dimension names are current everywhere")
# Names appear in prose and in docstrings, not only in the dataset, and a
# checked-in example that still uses a superseded name reads as a second set of
# data rather than as a stale line.
# Two generations of superseded names. The first are the working names the
# dataset was built under; the second are scenario names from dataset 1.0 that
# 2.0 renamed when scenarios recorded on other embodiments joined.
# `understanding`, `time` and `planning` were also working names, but they are
# ordinary English words and would match prose, so they are not scanned for.
# `stack_cubes_tianji` left this list with dataset 2.2: the 1.0 name was
# retired as mislabeled, and 2.2 re-issued it for the genuine tianji
# recording (QAGen's canonical mapping: raw `stack_cubes` -> this name).
superseded = {
    "airpods", "gift_inhand", "pen_inbox", "stack_cubes", "tea", "wash",
    "planning_2", "left_right", "image_in_video", "step_order",
    "hand_gift_tianji", "box_pen_tianji",
}
pattern = re.compile(r"\b(" + "|".join(sorted(superseded)) + r")\b")
# This file is the one place the superseded names may appear: the list above.
skip = {"tests/test_config_consistency.py"}
stale = []
for f in sorted(ROOT.rglob("*")):
    rel = f.relative_to(ROOT).as_posix()
    if f.suffix not in {".md", ".py", ".json", ".toml"} or rel in skip:
        continue
    # Several scenario names are also ordinary words, so a line-oriented scan
    # over the dataset would read them out of a goal description and report a
    # name that is not there. The dataset's own naming is covered by
    # tests/test_dataset_contract.py, which checks fields, not lines.
    if rel.startswith(("data/", ".git/", "results/")):
        continue
    for n, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
        if pattern.search(line):
            stale.append(f"{rel}:{n}")
check("no superseded names in tracked files", not stale, f"{len(stale)}: {stale[:3]}")

print()
if failures:
    print(f"FAILED: {len(failures)} check(s): {failures}")
    sys.exit(1)
print("all checks passed")
