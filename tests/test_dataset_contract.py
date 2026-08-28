#!/usr/bin/env python3
# coding: utf-8
"""The dataset on disk delivers what its manifest declares.

The sweep itself lives in ``robochrono.dataset.validate`` — one implementation
serves both this test and ``robochrono validate-data``, because two lists of
checks would drift apart exactly where it matters. This test runs it against
the working dataset and pins the headline numbers.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from robochrono.dataset.validate import format_report, validate_dataset  # noqa: E402

DATA = ROOT / "data"
failures: list[str] = []


def check(name: str, passed: bool, detail: str = "") -> None:
    print(f"  {'✅' if passed else '❌'} {name:52} {detail}")
    if not passed:
        failures.append(name)


if not (DATA / "manifest.json").exists():
    print("data/manifest.json not found — the dataset is not downloaded; skipping.")
    sys.exit(0)

report = validate_dataset(DATA)
print(format_report(report))
print()

check("no problems found", report.ok, str(report.problems[:3]))
check("every question loads", report.total == report.manifest.questions,
      f"{report.total} vs {report.manifest.questions}")
check("every media reference resolves", report.media_missing == 0)
check("references cover the shipped media exactly",
      report.media_references == report.manifest.media["files"],
      f"{report.media_references} vs {report.manifest.media['files']}")

print()
if failures:
    print(f"FAILED: {len(failures)} check(s): {failures}")
    sys.exit(1)
print("all checks passed")
