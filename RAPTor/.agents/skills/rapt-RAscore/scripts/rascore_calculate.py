#!/usr/bin/env python3
"""RAscore 計分器：驗證 LLM draft 並輸出標準 scorecard YAML。"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DIMENSIONS = {
    "A": {"name": "需求覆蓋與保真度", "weight": 0.20, "criteria": ["A1", "A2", "A3"]},
    "B": {"name": "Gherkin 行為規格品質", "weight": 0.18, "criteria": ["B1", "B2", "B3", "B4", "B5"]},
    "C": {"name": "DBML 領域模型品質", "weight": 0.14, "criteria": ["C1", "C2", "C3", "C4"]},
    "D": {"name": "Gherkin ↔ DBML 跨規格一致性", "weight": 0.24, "criteria": ["D1", "D2", "D3", "D4"]},
    "E": {"name": "追溯性與決策記錄", "weight": 0.14, "criteria": ["E1", "E2", "E3"]},
    "F": {"name": "可驗證與生成準備度", "weight": 0.07, "criteria": ["F1", "F2"]},
    "G": {"name": "流程穩定性", "weight": 0.03, "criteria": ["G1", "G2"]},
}

ALL_CRITERIA = [criterion for meta in DIMENSIONS.values() for criterion in meta["criteria"]]


def grade_for(score: float) -> str:
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 50:
        return "C"
    return "D"


def yaml_scalar(value: Any) -> str:
    if value is True:
        return "true"
    if value is False:
        return "false"
    if value is None:
        return "null"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{text}"'


def write_yaml(data: Any, indent: int = 0) -> list[str]:
    prefix = " " * indent
    lines: list[str] = []
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                lines.append(f"{prefix}{key}:")
                lines.extend(write_yaml(value, indent + 2))
            else:
                lines.append(f"{prefix}{key}: {yaml_scalar(value)}")
    elif isinstance(data, list):
        if not data:
            lines.append(f"{prefix}[]")
        for item in data:
            if isinstance(item, (dict, list)):
                lines.append(f"{prefix}-")
                lines.extend(write_yaml(item, indent + 2))
            else:
                lines.append(f"{prefix}- {yaml_scalar(item)}")
    else:
        lines.append(f"{prefix}{yaml_scalar(data)}")
    return lines


def collect_findings(criteria: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    counters: dict[str, int] = {}
    for criterion in ALL_CRITERIA:
        for finding in criteria[criterion].get("findings", []) or []:
            counters[criterion] = counters.get(criterion, 0) + 1
            item = dict(finding)
            item.setdefault("criterion", criterion)
            item.setdefault("severity", "medium")
            item.setdefault("category", "process-gap")
            item.setdefault("artifact", "")
            item.setdefault("location", "")
            item.setdefault("issue", "")
            item.setdefault("recommendation", "")
            item.setdefault("owner_skill", "manual-review")
            item["id"] = f"RA-{criterion}-{counters[criterion]:03d}"
            findings.append(item)
    severity_rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    return sorted(findings, key=lambda item: (severity_rank.get(item.get("severity"), 9), item["id"]))


def validate_and_calculate(draft: dict[str, Any]) -> dict[str, Any]:
    criteria = draft.get("criteria")
    if not isinstance(criteria, dict):
        raise ValueError("draft 必須包含 criteria object")

    missing = [criterion for criterion in ALL_CRITERIA if criterion not in criteria]
    if missing:
        raise ValueError(f"draft 缺少 criteria: {', '.join(missing)}")

    for criterion in ALL_CRITERIA:
        entry = criteria[criterion]
        if not isinstance(entry, dict):
            raise ValueError(f"{criterion} 必須是 object")
        score = entry.get("score")
        if score not in (0, 1, 2, 3):
            raise ValueError(f"{criterion}.score 必須是 0, 1, 2, 3")
        entry.setdefault("confidence", "low")
        entry.setdefault("review_mode", "llm-assisted")
        entry.setdefault("reason", "")
        entry.setdefault("evidence", [])
        entry.setdefault("findings", [])

    dimensions: dict[str, Any] = {}
    total = 0.0
    for key, meta in DIMENSIONS.items():
        scores = [criteria[criterion]["score"] for criterion in meta["criteria"]]
        avg = sum(scores) / len(scores)
        weighted = (avg / 3.0) * meta["weight"] * 100.0
        total += weighted
        dimensions[key] = {
            "name": meta["name"],
            "weight": meta["weight"],
            "average": round(avg, 2),
            "weighted_score": round(weighted, 2),
            "criteria": meta["criteria"],
        }

    veto_rules: list[str] = []
    if criteria["A1"]["score"] == 0:
        veto_rules.append("A1 = 0")
    if criteria["D2"]["score"] == 0:
        veto_rules.append("D2 = 0")
    if criteria["D3"]["score"] == 0:
        veto_rules.append("D3 = 0")
    if criteria["E1"]["score"] == 0 and criteria["E2"]["score"] == 0:
        veto_rules.append("E1 = 0 且 E2 = 0")
    if criteria["B1"]["score"] == 0:
        veto_rules.append("B1 = 0")

    total = round(total, 2)
    raw_grade = grade_for(total)
    grade = raw_grade
    if len(veto_rules) >= 2:
        grade = "D"
    elif len(veto_rules) == 1 and grade in ("A", "B"):
        grade = "C"

    return {
        "project": draft.get("project", ""),
        "rascore_version": draft.get("rascore_version", "0.1"),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "advisory_only": True,
        "score": {
            "total": total,
            "raw_grade": raw_grade,
            "grade": grade,
            "veto": {"triggered": bool(veto_rules), "rules": veto_rules},
        },
        "dimensions": dimensions,
        "criteria": {criterion: criteria[criterion] for criterion in ALL_CRITERIA},
        "findings": collect_findings(criteria),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Calculate RAscore from LLM scorecard draft JSON")
    parser.add_argument("--scorecard-draft", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    draft_path = Path(args.scorecard_draft)
    output_path = Path(args.output)
    draft = json.loads(draft_path.read_text(encoding="utf-8-sig"))
    scorecard = validate_and_calculate(draft)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(write_yaml(scorecard)) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

