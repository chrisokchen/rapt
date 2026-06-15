#!/usr/bin/env python3
"""RAscore 報告渲染器：由 scorecard / draft / precheck 產生 Markdown 與 JSON findings。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


SEVERITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig") if path.exists() else ""


def extract_scalar(yaml_text: str, path: str, default: str = "") -> str:
    # 對 rascore_calculate.py 產生的簡單 YAML 做保守擷取。
    patterns = {
        "project": r"(?m)^project:\s+\"?(.*?)\"?\s*$",
        "total": r"(?m)^\s+total:\s+([0-9.]+)\s*$",
        "raw_grade": r"(?m)^\s+raw_grade:\s+\"?(.*?)\"?\s*$",
        "grade": r"(?m)^\s+grade:\s+\"?(.*?)\"?\s*$",
        "veto_triggered": r"(?m)^\s+triggered:\s+(true|false)\s*$",
    }
    pattern = patterns.get(path)
    if not pattern:
        return default
    match = re.search(pattern, yaml_text)
    return match.group(1).strip() if match else default


def extract_dimensions(yaml_text: str) -> list[dict[str, str]]:
    dimensions: list[dict[str, str]] = []
    for key in ["A", "B", "C", "D", "E", "F", "G"]:
        match = re.search(
            rf"(?ms)^  {key}:\n\s+name:\s+\"?(.*?)\"?\s*\n\s+weight:\s+([0-9.]+)\s*\n\s+average:\s+([0-9.]+)\s*\n\s+weighted_score:\s+([0-9.]+)",
            yaml_text,
        )
        if match:
            dimensions.append(
                {
                    "key": key,
                    "name": match.group(1),
                    "weight": match.group(2),
                    "average": match.group(3),
                    "weighted_score": match.group(4),
                }
            )
    return dimensions


def recommended_action_type(category: str) -> str:
    mapping = {
        "coverage-loss": "clarify_or_add_scenario",
        "scope-creep": "clarify_scope",
        "gherkin-quality": "behavior_revision",
        "dbml-quality": "modeling_revision",
        "cross-spec-gap": "traceability_mapping",
        "traceability-gap": "traceability_or_decision_sync",
        "readiness-gap": "readiness_revision",
        "process-gap": "process_revision",
    }
    return mapping.get(category, "manual_review")


def collect_findings(draft: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    counters: dict[str, int] = {}
    criteria = draft.get("criteria", {}) if isinstance(draft.get("criteria"), dict) else {}
    for criterion, entry in criteria.items():
        if not isinstance(entry, dict):
            continue
        for finding in entry.get("findings", []) or []:
            if not isinstance(finding, dict):
                continue
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
            item.setdefault("recommended_action_type", recommended_action_type(item["category"]))
            item["id"] = item.get("id") or f"RA-{criterion}-{counters[criterion]:03d}"
            findings.append(item)
    return sorted(findings, key=lambda item: (SEVERITY_RANK.get(item.get("severity"), 9), item["id"]))


def render_report(scorecard_text: str, findings: list[dict[str, Any]], precheck: dict[str, Any]) -> str:
    project = extract_scalar(scorecard_text, "project", "")
    total = extract_scalar(scorecard_text, "total", "0")
    raw_grade = extract_scalar(scorecard_text, "raw_grade", "")
    grade = extract_scalar(scorecard_text, "grade", "")
    veto = extract_scalar(scorecard_text, "veto_triggered", "false")
    dimensions = extract_dimensions(scorecard_text)

    lines = [
        "# RAPTor RAscore 評分報告",
        "",
        f"專案：{project}",
        "評分模式：LLM-assisted advisory-only",
        "",
        "## 總覽",
        "",
        "| 項目 | 結果 |",
        "|---|---:|",
        f"| RAscore | {total} / 100 |",
        f"| Raw Grade | {raw_grade} |",
        f"| Advisory Grade | {grade} |",
        "| Advisory-only | true |",
        f"| Veto | {'觸發' if veto == 'true' else '未觸發'} |",
        "",
        "## 維度分數",
        "",
        "| 維度 | 名稱 | 平均分 | 加權分 |",
        "|---|---|---:|---:|",
    ]
    for dim in dimensions:
        lines.append(f"| {dim['key']} | {dim['name']} | {dim['average']} / 3 | {dim['weighted_score']} |")

    lines.extend(["", "## Top Findings", ""])
    if findings:
        for index, finding in enumerate(findings[:5], start=1):
            lines.append(f"{index}. [{finding['id']}] {finding.get('issue', '')}")
    else:
        lines.append("無 findings。")

    cross_spec = precheck.get("cross_spec", {}) if isinstance(precheck, dict) else {}
    lines.extend(
        [
            "",
            "## Precheck 摘要",
            "",
            f"- glossary mappings: {len(cross_spec.get('glossary_mappings', []) or [])}",
            f"- scenario table candidates: {len(cross_spec.get('scenario_table_candidates', []) or [])}",
            f"- orphan tables after glossary: {len(cross_spec.get('orphan_dbml_tables_after_glossary', []) or [])}",
            f"- L2 traceability ratio: {cross_spec.get('l2_traceability_coverage', {}).get('ratio', 0)}",
            "",
            "## 建議行動",
            "",
            "1. 將 high / medium findings 交由 `rapt-reconcile` 分類。",
            "2. 對 need-human 項目執行 `/rapt-clarify`。",
            "3. 修正後執行 `/rapt-verify`，再重跑 `/rapt-RAscore`。",
            "",
            "完整 findings：`.raptor/reports/rascore-findings.md`",
            "機器可讀 findings：`.raptor/reports/rascore-findings.json`",
        ]
    )
    return "\n".join(lines) + "\n"


def render_findings_md(findings: list[dict[str, Any]]) -> str:
    lines = ["# RAscore Findings", ""]
    if not findings:
        lines.append("無 findings。")
        return "\n".join(lines) + "\n"
    current = None
    for finding in findings:
        severity = str(finding.get("severity", "medium")).capitalize()
        if severity != current:
            current = severity
            lines.extend(["", f"## {severity}", ""])
        lines.extend(
            [
                f"### {finding['id']}",
                "",
                f"- Criterion: {finding.get('criterion', '')}",
                f"- Category: {finding.get('category', '')}",
                f"- Artifact: `{finding.get('artifact', '')}`",
                f"- Location: {finding.get('location', '')}",
                f"- Issue: {finding.get('issue', '')}",
                f"- Recommendation: {finding.get('recommendation', '')}",
                f"- Owner Skill: `{finding.get('owner_skill', 'manual-review')}`",
                f"- Recommended Action Type: `{finding.get('recommended_action_type', 'manual_review')}`",
                "",
            ]
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Render RAscore reports")
    parser.add_argument("--scorecard", required=True)
    parser.add_argument("--draft", required=True)
    parser.add_argument("--precheck", required=True)
    parser.add_argument("--report", required=True)
    parser.add_argument("--findings-md", required=True)
    parser.add_argument("--findings-json", required=True)
    args = parser.parse_args()

    scorecard_text = read_text(Path(args.scorecard))
    draft = read_json(Path(args.draft))
    precheck = read_json(Path(args.precheck))
    findings = collect_findings(draft)

    report_path = Path(args.report)
    findings_md_path = Path(args.findings_md)
    findings_json_path = Path(args.findings_json)
    for path in [report_path, findings_md_path, findings_json_path]:
        path.parent.mkdir(parents=True, exist_ok=True)

    report_path.write_text(render_report(scorecard_text, findings, precheck), encoding="utf-8")
    findings_md_path.write_text(render_findings_md(findings), encoding="utf-8")
    findings_json_path.write_text(
        json.dumps({"findings": findings}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
