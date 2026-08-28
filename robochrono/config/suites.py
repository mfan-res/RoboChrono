#!/usr/bin/env python3
# coding: utf-8
"""Reading ``configs/suites/*.json`` — a frozen set of scenarios and dimensions.

A suite pins exactly which scenarios and dimensions a published number covers.
The dataset grows over time; without a pinned set, "the score on RoboChrono"
would silently mean different things at different dates, and two such numbers
would look directly comparable when they are not.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Suite:
    name: str
    dataset_version: str
    scenarios: tuple[str, ...]
    dimensions: tuple[str, ...]


def load_suite(name_or_path: Any, root: Any = "configs/suites") -> Suite:
    path = Path(name_or_path)
    if not path.exists():
        path = Path(root) / f"{name_or_path}.json"
    raw = json.loads(path.read_text(encoding="utf-8"))
    for k in ("name", "dataset_version", "scenarios", "dimensions"):
        if k not in raw:
            raise ValueError(f"{path} is missing {k}")
    return Suite(name=raw["name"], dataset_version=raw["dataset_version"],
                 scenarios=tuple(raw["scenarios"]), dimensions=tuple(raw["dimensions"]))
