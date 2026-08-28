#!/usr/bin/env python3
# coding: utf-8
"""Validating that the dataset on disk delivers what its manifest declares.

Everything downstream — suites, run identity, result merging — trusts the
manifest, and nothing enforces that trust by itself: a question that fails to
render, a media path that resolves to nothing, or a count that drifted would
each surface mid-evaluation at best. This sweep loads every question the way
the evaluation does — through ``load_questions``, rendered — so what it
validates is what actually runs.

One implementation serves both ``robochrono validate-data`` and the test
suite; two lists of checks would drift apart exactly where it matters.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .loader import load_questions, media_paths
from .manifest import Manifest, load_manifest
from .render import load_question_bank


@dataclass
class ValidationReport:
    manifest: Manifest | None = None
    problems: list[str] = field(default_factory=list)
    total: int = 0
    dimension_counts: Counter = field(default_factory=Counter)
    scenario_counts: Counter = field(default_factory=Counter)
    media_references: int = 0
    media_missing: int = 0

    @property
    def ok(self) -> bool:
        return not self.problems


def _check_question(q: dict[str, Any], dimension: str, problems: list[str]) -> None:
    if not q.get("question", "").strip():
        problems.append(f"{q.get('id')}: empty question")
    options = q.get("options") or []
    if options:
        letters = [o.get("id") for o in options]
        if letters != [chr(ord("A") + i) for i in range(len(options))]:
            problems.append(f"{q.get('id')}: option letters {letters}")
        if q.get("answer") not in letters:
            problems.append(f"{q.get('id')}: answer {q.get('answer')!r} not an option")
        for o in options:
            if not o.get("text") and not o.get("image_path"):
                problems.append(f"{q.get('id')}: option {o.get('id')} has neither "
                                f"text nor image")
    if dimension == "action_time":
        sec = q.get("answer_seconds") or {}
        if options:
            problems.append(f"{q.get('id')}: action_time question has options")
        if not (isinstance(sec.get("start"), (int, float))
                and isinstance(sec.get("end"), (int, float))
                and sec["start"] < sec["end"]):
            problems.append(f"{q.get('id')}: answer_seconds {sec!r}")
    elif len(options) != 4:
        problems.append(f"{q.get('id')}: {len(options)} options")


def validate_dataset(data_root: Any) -> ValidationReport:
    report = ValidationReport()
    data_root = Path(data_root)
    try:
        report.manifest = load_manifest(data_root)
        bank = load_question_bank(data_root)
    except Exception as exc:  # noqa: BLE001 — any load failure is the finding
        report.problems.append(str(exc))
        return report
    manifest = report.manifest

    media_refs: set[str] = set()
    for scenario in manifest.scenario_names():
        for dimension in manifest.dimension_names():
            try:
                questions = load_questions(data_root, scenario, dimension, bank=bank)
            except Exception as exc:  # noqa: BLE001
                report.problems.append(f"{scenario}/{dimension}: {exc!r}")
                continue
            for q in questions:
                _check_question(q, dimension, report.problems)
                media_refs.update(media_paths(q))
            report.dimension_counts[dimension] += len(questions)
            report.scenario_counts[scenario] += len(questions)
            report.total += len(questions)

    for scenario, declared in manifest.scenarios.items():
        if report.scenario_counts[scenario] != declared["questions"]:
            report.problems.append(
                f"{scenario}: {report.scenario_counts[scenario]} questions loaded "
                f"vs {declared['questions']} declared")
    for dimension, declared in manifest.dimensions.items():
        if report.dimension_counts[dimension] != declared:
            report.problems.append(
                f"{dimension}: {report.dimension_counts[dimension]} loaded "
                f"vs {declared} declared")
    if report.total != manifest.questions:
        report.problems.append(f"total {report.total} vs {manifest.questions} declared")

    report.media_references = len(media_refs)
    missing = sorted(p for p in media_refs if not (data_root / p).exists())
    report.media_missing = len(missing)
    for path in missing[:10]:
        report.problems.append(f"missing media: {path}")
    if len(missing) > 10:
        report.problems.append(f"... and {len(missing) - 10} more missing media files")
    # The manifest counts the media that ships; the questions reference some
    # set of files. Equal (with none missing) means nothing in the download is
    # dead weight and nothing referenced is absent.
    if len(media_refs) != manifest.media["files"]:
        report.problems.append(
            f"{len(media_refs)} unique media references vs "
            f"{manifest.media['files']} files declared")
    return report


def format_report(report: ValidationReport) -> str:
    lines = []
    if report.manifest:
        m = report.manifest
        lines.append(f"dataset {m.name} v{m.version}, fingerprint {m.fingerprint}")
        lines.append(f"  {report.total} questions across "
                     f"{len(report.scenario_counts)} scenarios × "
                     f"{len(report.dimension_counts)} dimensions")
        lines.append(f"  {report.media_references} media references, "
                     f"{report.media_missing} missing")
    if report.ok:
        lines.append("all checks passed")
    else:
        lines.append(f"{len(report.problems)} problem(s):")
        lines.extend(f"  {p}" for p in report.problems[:50])
        if len(report.problems) > 50:
            lines.append(f"  ... and {len(report.problems) - 50} more")
    return "\n".join(lines)
