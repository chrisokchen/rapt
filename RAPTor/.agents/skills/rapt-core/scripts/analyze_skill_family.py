#!/usr/bin/env python3
"""檢查 RAPTor skill family 的文件一致性。"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REQUIRED_SECTIONS = [
    "## TRIGGER",
    "## SKIP",
    "## PRINCIPLE",
    "## Artifact Output Contract",
]


@dataclass
class Finding:
    severity: str
    skill: str
    message: str


def infer_expected_type(skill_name: str) -> str:
    if skill_name in {"rapt-core", "rapt-RAscore", "rapt-clarify-loop"}:
        return "utility"
    if skill_name in {"rapt-openapi", "rapt-lofi", "rapt-design-brief"}:
        return "preview"
    if skill_name == "rapt-verify":
        return "verifier"
    if skill_name.startswith("rapt-form-"):
        return "worker"
    return "planner"


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    result: dict[str, str] = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, value = line.split(":", 1)
            result[key.strip()] = value.strip().strip('"')
    metadata = re.search(r"metadata:\n(?P<body>(?:  .+\n?)+)", text[3:end])
    if metadata:
        for line in metadata.group("body").splitlines():
            if ":" in line:
                key, value = line.strip().split(":", 1)
                result[f"metadata.{key.strip()}"] = value.strip().strip('"')
    return result


def section_body(text: str, header: str) -> str:
    """取出 '## {header}' 到下一個 '## ' 之間的內文（正規化空白）。"""
    match = re.search(
        rf"^## {re.escape(header)}\s*\n(?P<body>.*?)(?=^## |\Z)",
        text,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        return ""
    return " ".join(match.group("body").split())


def check_markdown_structure(text: str, skill_name: str) -> list[Finding]:
    """偵測裸 code fence（無語言標記）內出現 markdown 標題（複製貼上/插入事故），以及未閉合 fence。

    帶語言標記的 fence（```markdown、```yaml 等）視為刻意的內容模板，不檢查。
    """
    findings: list[Finding] = []
    in_fence = False
    fence_info = ""
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_fence:
                in_fence = False
                fence_info = ""
            else:
                in_fence = True
                fence_info = stripped[3:].strip()
            continue
        if in_fence and not fence_info and re.match(r"^#{2,3} \S", stripped):
            findings.append(
                Finding(
                    "medium",
                    skill_name,
                    f"markdown heading inside bare code fence (line {lineno}): {stripped[:40]}",
                )
            )
    if in_fence:
        findings.append(Finding("medium", skill_name, "unclosed code fence at end of file"))
    return findings


def analyze_skill(path: Path) -> list[Finding]:
    text = path.read_text(encoding="utf-8")
    frontmatter = parse_frontmatter(text)
    skill_name = frontmatter.get("name", path.parent.name)
    findings: list[Finding] = []

    if not frontmatter.get("name"):
        findings.append(Finding("high", skill_name, "missing frontmatter name"))
    if not frontmatter.get("description"):
        findings.append(Finding("high", skill_name, "missing frontmatter description"))

    expected_type = infer_expected_type(skill_name)
    actual_type = frontmatter.get("metadata.skill-type") or frontmatter.get("skill-type")
    if not actual_type:
        findings.append(Finding("medium", skill_name, f"missing skill-type, expected {expected_type}"))
    elif actual_type != expected_type:
        findings.append(
            Finding("medium", skill_name, f"skill-type is {actual_type}, expected {expected_type}")
        )

    for section in REQUIRED_SECTIONS:
        if section not in text:
            findings.append(Finding("medium", skill_name, f"missing section {section}"))

    if "## Artifact Output Contract" in text and "DENY" not in text:
        findings.append(Finding("low", skill_name, "Artifact Output Contract has no DENY row"))

    if expected_type == "worker" and "failure_kind" not in text:
        findings.append(Finding("medium", skill_name, "worker missing failure_kind contract"))

    findings.extend(check_markdown_structure(text, skill_name))

    return findings


def check_duplicate_triggers(texts: dict[str, str]) -> list[Finding]:
    """偵測跨 skill 完全相同的 TRIGGER 內文（模板複製未改的事故）。

    TRIGGER 是路由條件，必須每個 skill 各自可判定；SKIP 允許家族樣板共用，不檢查。
    """
    findings: list[Finding] = []
    by_body: dict[str, list[str]] = {}
    for skill_name, text in texts.items():
        body = section_body(text, "TRIGGER")
        if body:
            by_body.setdefault(body, []).append(skill_name)
    for body, skills in by_body.items():
        if len(skills) > 1:
            group = ", ".join(sorted(skills))
            findings.append(
                Finding(
                    "medium",
                    group,
                    "TRIGGER section is byte-identical across these skills; "
                    "each skill needs its own trigger semantics",
                )
            )
    return findings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="RAPTor/.agents/skills")
    args = parser.parse_args()
    root = Path(args.root)
    findings: list[Finding] = []
    texts: dict[str, str] = {}
    for path in sorted(root.glob("rapt-*/SKILL.md")):
        findings.extend(analyze_skill(path))
        text = path.read_text(encoding="utf-8")
        texts[parse_frontmatter(text).get("name", path.parent.name)] = text
    findings.extend(check_duplicate_triggers(texts))

    if not findings:
        print("OK skill family is consistent")
        return 0

    for finding in findings:
        print(f"{finding.severity.upper()} {finding.skill}: {finding.message}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
