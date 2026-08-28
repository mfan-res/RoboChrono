#!/usr/bin/env python3
# coding: utf-8
"""Reading ``data/manifest.json`` — the dataset's self-description.

The manifest holds **facts about the data**: which scenarios and dimensions
exist, how many questions and episodes each scenario has, how large the media
is. Its ``fingerprint`` identifies the question set; results carry it so that
scores computed on different datasets can never be merged silently.

It deliberately does not hold **judgements about the data**, such as the
degenerate-performance floor a score is compared against. Those live in
``configs/protocol.json``, because the same data can reasonably be judged
against different floors — a floor is a choice about evaluation, not a
property of the dataset.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Manifest:
    path: Path
    name: str
    version: str
    fingerprint: str
    questions: int
    scenarios: dict[str, dict[str, int]]   # scenario -> {episodes, questions}
    dimensions: dict[str, int]             # dimension -> question count
    media: dict[str, int]                  # {files, bytes}

    @property
    def data_root(self) -> Path:
        return self.path.parent

    def scenario_names(self) -> list[str]:
        return sorted(self.scenarios)

    def dimension_names(self) -> list[str]:
        return sorted(self.dimensions)


_REQUIRED = ("name", "version", "fingerprint", "questions",
             "scenarios", "dimensions", "media")


def load_manifest(data_root: Any) -> Manifest:
    """Read and validate the manifest. A missing field is a hard error.

    No defaults are supplied: filling one in would make the code assert
    something about the dataset, and what the dataset contains is not something
    code should infer.
    """
    path = Path(data_root) / "manifest.json"
    if not path.exists():
        raise FileNotFoundError(
            f"{path} not found — the dataset is not downloaded, or the path is wrong. "
            f"See the Data section of README.md, or run `robochrono validate-data`.")
    raw = json.loads(path.read_text(encoding="utf-8"))
    missing = [k for k in _REQUIRED if k not in raw]
    if missing:
        raise ValueError(f"{path} is missing fields: {missing}")

    for name, count in raw["dimensions"].items():
        if not isinstance(count, int):
            raise ValueError(f"{path}: dimensions.{name} must be a question count, "
                             f"got {type(count).__name__}")
    for name, s in raw["scenarios"].items():
        for k in ("episodes", "questions"):
            if k not in s:
                raise ValueError(f"{path}: scenarios.{name} is missing {k}")

    return Manifest(
        path=path, name=raw["name"], version=raw["version"],
        fingerprint=raw["fingerprint"], questions=raw["questions"],
        scenarios=raw["scenarios"], dimensions=raw["dimensions"], media=raw["media"],
    )
