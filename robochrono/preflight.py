#!/usr/bin/env python3
# coding: utf-8
"""Pre-run checks: what would fail at minute 180 should fail at minute 0.

A full matrix runs for days. Anything discoverable up front — a missing key,
absent weights, an interpreter in the wrong environment, data that is not the
dataset the suite pins — is checked here before a single model call.

Four verdict levels:

    FAIL  the run cannot proceed; fix it
    WARN  it can run, but results may be wrong or incomplete; know about it
    OK    checked and fine
    SKIP  not needed for this selection — an API-only run does not need the
          local inference stack, and saying FAIL there would demand twenty
          gigabytes of torch from someone who only wants to call an endpoint

Only FAIL affects the exit status.
"""

from __future__ import annotations

import importlib
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import adapters
from .config.environments import Environment, satisfies
from .config.models import ModelConfig
from .config.protocol import Protocol
from .config.suites import Suite
from .dataset.loader import load_questions, media_paths, resolve_media
from .dataset.manifest import load_manifest
from .dataset.render import load_question_bank
from .orchestrate.matrix import RunSpec

OK, WARN, FAIL, SKIP = "OK", "WARN", "FAIL", "SKIP"

API_PACKAGES = ("requests",)
LOCAL_PACKAGES = ("torch", "transformers", "decord", "PIL", "qwen_vl_utils",
                  "torchvision")


@dataclass
class Check:
    level: str
    name: str
    detail: str = ""


def has_failures(checks: list[Check]) -> bool:
    return any(c.level == FAIL for c in checks)


def format_checks(checks: list[Check]) -> str:
    mark = {OK: "✅", WARN: "⚠️ ", FAIL: "❌", SKIP: "⏭️ "}
    lines = [f"  {mark[c.level]} [{c.level:4}] {c.name:44} {c.detail}".rstrip()
             for c in checks]
    fails = sum(1 for c in checks if c.level == FAIL)
    warns = sum(1 for c in checks if c.level == WARN)
    lines.append("")
    lines.append(f"{len(checks)} checks: {fails} FAIL, {warns} WARN"
                 if fails or warns else f"{len(checks)} checks, all clear")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Individual check groups
# --------------------------------------------------------------------------

def check_configuration(models: list[ModelConfig], suite: Suite,
                        protocol: Protocol,
                        environments: dict[str, Environment]) -> list[Check]:
    out: list[Check] = []
    for model in models:
        try:
            adapters.build(model, protocol)
            out.append(Check(OK, f"{model.slug} configuration"))
        except Exception as exc:  # noqa: BLE001 — any config defect is the finding
            out.append(Check(FAIL, f"{model.slug} configuration", str(exc)))
        if model.environment not in environments:
            out.append(Check(FAIL, f"{model.slug} environment",
                             f"{model.environment!r} is not defined in "
                             f"configs/environments.json"))
    missing_frames = [d for d in suite.dimensions
                      if d not in protocol.frames_by_dimension]
    out.append(Check(FAIL if missing_frames else OK, "frame sampling declared",
                     f"missing: {missing_frames}" if missing_frames
                     else f"{len(suite.dimensions)} dimensions"))
    return out


def check_environment(models: list[ModelConfig],
                      environments: dict[str, Environment],
                      repo_root: Any) -> list[Check]:
    """Is this interpreter one of the declared environments, with the stack
    the selected models need?"""
    out: list[Check] = []
    needs_local = any(m.kind == "local" for m in models)

    # Which declared environment is this interpreter? sys.prefix identifies
    # the venv itself; comparing sys.executable would follow the bin/python
    # symlink to the base interpreter and compare the wrong thing.
    here = Path(sys.prefix).resolve()
    current: Environment | None = None
    for env in environments.values():
        raw = str(env.python or "").strip()
        if not raw:
            continue
        prefix = Path(raw)
        if not prefix.is_absolute():
            prefix = Path(repo_root) / prefix
        if prefix.parent.parent.resolve() == here:
            current = env
            break
    out.append(Check(OK if current else WARN, "interpreter environment",
                     f"{current.name}" if current else
                     f"{sys.prefix} is none of the declared environments — "
                     f"fine for dispatching, not for running local models"))

    packages = (LOCAL_PACKAGES if needs_local else ()) + API_PACKAGES
    if not needs_local:
        for name in LOCAL_PACKAGES:
            out.append(Check(SKIP, f"package {name}",
                             "API-only selection needs no local stack"))
    for name in packages:
        try:
            module = importlib.import_module(name)
        except ImportError:
            out.append(Check(FAIL, f"package {name}", "not importable"))
            continue
        version = getattr(module, "__version__", "")
        if name == "transformers" and current:
            ok = satisfies(f"=={current.transformers}", version)
            out.append(Check(OK if ok else FAIL, "package transformers",
                             f"{version} vs {current.transformers} declared for "
                             f"{current.name}"))
        else:
            out.append(Check(OK, f"package {name}", version))
    return out


def check_gpu(models: list[ModelConfig]) -> list[Check]:
    if not any(m.kind == "local" for m in models):
        return [Check(SKIP, "GPU", "API-only selection")]
    try:
        import torch
    except ImportError:
        return [Check(FAIL, "GPU", "torch is not importable")]
    if not torch.cuda.is_available():
        return [Check(FAIL, "GPU", "no CUDA device visible")]
    return [Check(OK, "GPU", f"{torch.cuda.device_count()} device(s)")]


def check_weights(models: list[ModelConfig], repo_root: Any) -> list[Check]:
    out: list[Check] = []
    for model in models:
        if model.kind != "local":
            out.append(Check(SKIP, f"{model.slug} weights", "API model"))
            continue
        path = Path(model.weights)
        if not path.is_absolute():
            path = Path(repo_root) / path
        out.append(Check(OK, f"{model.slug} weights", str(path)) if path.exists()
                   else Check(FAIL, f"{model.slug} weights", f"{path} not found"))
    return out


def check_api_keys(models: list[ModelConfig]) -> list[Check]:
    out: list[Check] = []
    for model in models:
        if model.kind != "api":
            continue
        key_env = model.api.get("key_env")
        if not key_env:
            out.append(Check(WARN, f"{model.slug} key", "no key_env declared"))
        elif os.environ.get(str(key_env)):
            out.append(Check(OK, f"{model.slug} key", f"{key_env} is set"))
        else:
            out.append(Check(FAIL, f"{model.slug} key", f"{key_env} is not set"))
    needs_ffmpeg = any(m.kind == "api" for m in models)
    if needs_ffmpeg:
        found = shutil.which("ffmpeg") and shutil.which("ffprobe")
        out.append(Check(OK if found else WARN, "ffmpeg",
                         "" if found else "not on PATH — media over the request "
                         "budget cannot be shrunk and will fail loudly"))
    return out


def check_data(specs: list[RunSpec], suite: Suite, data_root: Any,
               sample: int = 3) -> list[Check]:
    """The dataset is present, is the suite's dataset, and its media resolve.

    Loading goes through the same functions the evaluation uses; a check that
    loads data its own way validates something other than what runs. Media
    existence is sampled — the full sweep is ``validate-data``'s job.
    """
    out: list[Check] = []
    try:
        manifest = load_manifest(data_root)
    except (FileNotFoundError, ValueError) as exc:
        return [Check(FAIL, "dataset manifest", str(exc))]
    out.append(Check(OK, "dataset manifest",
                     f"v{manifest.version} {manifest.fingerprint}, "
                     f"{manifest.questions} questions"))
    if suite.dataset_version != manifest.version:
        out.append(Check(FAIL, "suite dataset version",
                         f"suite pins {suite.dataset_version}, "
                         f"data is {manifest.version}"))
    unknown = set(suite.scenarios) - set(manifest.scenarios)
    if unknown:
        out.append(Check(FAIL, "suite scenarios",
                         f"not in this dataset: {sorted(unknown)}"))

    try:
        bank = load_question_bank(data_root)
    except Exception as exc:  # noqa: BLE001
        return out + [Check(FAIL, "question bank", str(exc))]

    checked = missing = 0
    combos = {(s.scenario, s.dimension) for s in specs}
    for scenario, dimension in sorted(combos):
        try:
            questions = load_questions(data_root, scenario, dimension, bank=bank)
        except Exception as exc:  # noqa: BLE001
            out.append(Check(FAIL, f"{scenario}/{dimension}", f"load: {exc}"))
            continue
        for question in questions[:sample]:
            for path in media_paths(question):
                checked += 1
                if not resolve_media(data_root, path).exists():
                    missing += 1
    out.append(Check(FAIL if missing else OK, "sampled media",
                     f"{missing} of {checked} missing" if missing
                     else f"{checked} paths from {len(combos)} file(s)"))
    return out


def run_preflight(
    specs: list[RunSpec],
    models: list[ModelConfig],
    *,
    suite: Suite,
    protocol: Protocol,
    environments: dict[str, Environment],
    data_root: Any,
    repo_root: Any = ".",
    include_environment: bool = True,
) -> list[Check]:
    """All checks for one selection.

    ``include_environment`` is off when the caller is only going to dispatch:
    the parent interpreter's own stack is irrelevant then — each child gets
    checked in the environment it actually runs under.
    """
    checks = check_configuration(models, suite, protocol, environments)
    if include_environment:
        checks += check_environment(models, environments, repo_root)
        checks += check_gpu(models)
    checks += check_weights(models, repo_root)
    checks += check_api_keys(models)
    checks += check_data(specs, suite, data_root)
    return checks
