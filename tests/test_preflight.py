#!/usr/bin/env python3
# coding: utf-8
"""Preflight verdicts: what fails, what skips, and what passes on real data."""
from __future__ import annotations

import dataclasses
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from robochrono import preflight  # noqa: E402
from robochrono.config.environments import load_environments  # noqa: E402
from robochrono.config.models import load_models  # noqa: E402
from robochrono.config.protocol import load_protocol  # noqa: E402
from robochrono.config.suites import load_suite  # noqa: E402
from robochrono.orchestrate.matrix import expand  # noqa: E402

failures: list[str] = []


def check(name: str, passed: bool, detail: str = "") -> None:
    print(f"  {'✅' if passed else '❌'} {name:52} {detail}")
    if not passed:
        failures.append(name)


def levels(checks, name_part):
    return [c.level for c in checks if name_part in c.name]


PROTOCOL = load_protocol(ROOT / "configs/protocol.json")
SUITE = load_suite("v1", ROOT / "configs/suites")
ENVS = load_environments(ROOT / "configs/environments.json")
MODELS = sorted(load_models(ROOT / "configs/models").values(), key=lambda m: m.slug)
DATA = ROOT / "data"

LOCAL = MODELS[0]
API = dataclasses.replace(
    MODELS[0], slug="test-api", kind="api", adapter="openai_compat",
    api={"url": "https://x", "model": "m", "key_env": "ROBOCHRONO_TEST_KEY"})

print("1. configuration checks")
checks = preflight.check_configuration(MODELS, SUITE, PROTOCOL, ENVS)
check("all real models configure", not preflight.has_failures(checks))
broken = dataclasses.replace(MODELS[0], slug="broken", adapter="nope")
checks = preflight.check_configuration([broken], SUITE, PROTOCOL, ENVS)
check("unknown adapter is a FAIL", preflight.FAIL in levels(checks, "broken"))
odd_env = dataclasses.replace(MODELS[0], slug="odd", environment="tf-9")
checks = preflight.check_configuration([odd_env], SUITE, PROTOCOL, ENVS)
check("undefined environment is a FAIL",
      preflight.FAIL in levels(checks, "odd environment"))

print("2. weights and keys")
ghost = dataclasses.replace(LOCAL, slug="ghost", weights="models/does-not-exist")
checks = preflight.check_weights([ghost, API], ROOT)
check("absent local weights FAIL",
      levels(checks, "ghost weights") == [preflight.FAIL])
check("API models skip the weights check",
      levels(checks, "test-api weights") == [preflight.SKIP])

os.environ.pop("ROBOCHRONO_TEST_KEY", None)
checks = preflight.check_api_keys([API])
check("unset key_env is a FAIL", levels(checks, "test-api key") == [preflight.FAIL])
os.environ["ROBOCHRONO_TEST_KEY"] = "sk-test"
checks = preflight.check_api_keys([API])
check("set key_env is OK", levels(checks, "test-api key") == [preflight.OK])

print("3. environment checks scale to the selection")
checks = preflight.check_environment([API], ENVS, ROOT)
check("API-only selection skips the local stack",
      all(l == preflight.SKIP
          for l in levels(checks, "package torch")))
check("requests still required",
      levels(checks, "package requests") == [preflight.OK])
checks = preflight.check_gpu([API])
check("API-only selection skips the GPU check",
      [c.level for c in checks] == [preflight.SKIP])

print("4. data checks run the evaluation's own loading path")
specs, _ = expand([LOCAL], SUITE, DATA,
                  only_scenarios=["make_tea_tianji"],
                  only_dimensions=["current_action", "view_match"])
checks = preflight.check_data(specs, SUITE, DATA)
check("real dataset passes", not preflight.has_failures(checks),
      str([c for c in checks if c.level == preflight.FAIL][:1]))
check("media was actually sampled",
      any("sampled media" in c.name and c.level == preflight.OK for c in checks))

checks = preflight.check_data(specs, SUITE, "/nonexistent")
check("missing dataset is a FAIL", preflight.has_failures(checks))
wrong = dataclasses.replace(SUITE, dataset_version="1.0")
checks = preflight.check_data(specs, wrong, DATA)
check("suite pinned to another dataset version is a FAIL",
      any("suite dataset version" in c.name and c.level == preflight.FAIL
          for c in checks))

print("5. the full pass, formatted")
checks = preflight.run_preflight(specs, [API], suite=SUITE, protocol=PROTOCOL,
                                 environments=ENVS, data_root=DATA, repo_root=ROOT)
text = preflight.format_checks(checks)
check("summary line present", "checks" in text.splitlines()[-1])
check("exit condition computable", isinstance(preflight.has_failures(checks), bool))

print()
if failures:
    print(f"FAILED: {len(failures)} check(s): {failures}")
    sys.exit(1)
print("all checks passed")
