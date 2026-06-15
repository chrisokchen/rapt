#!/usr/bin/env python3
"""偵測人工 SSoT 變更並登錄 RAPTor human-sync V1 紀錄。

本工具刻意只使用 Python stdlib，並透過 rapt-core 的
manage_impact_matrix.py 寫入 impact-matrix，避免手寫 YAML 破壞既有 schema。
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "rapt-human-sync/v1"
EXIT_ARGUMENTS_NOT_FOUND = 2
EXIT_BASELINE_NOT_FOUND = 3
EXIT_GIT_ERROR = 4


@dataclass
class Baseline:
    commit: str
    source: str
    label: str


@dataclass
class GitChange:
    path: str
    change_type: str
    old_path: str | None = None
    source: str = "committed"


@dataclass
class Hunk:
    location: str
    hunk_header: str
    added: int
    removed: int
    snippet: list[str] = field(default_factory=list)


@dataclass
class ChangeRecord:
    id: str
    impact_id: str
    fingerprint: str
    file: str
    old_file: str | None
    ssot_class: str
    dsl: str
    change_type: str
    risk: str
    source: str
    author: dict[str, str]
    committed_at: str
    commit: str
    diff_summary: dict[str, int]
    semantic_summary: list[dict[str, str]]
    hunks: list[Hunk]
    impact_assessment: dict[str, Any]


def run_git(root: Path, args: list[str], check: bool = True) -> str:
    cmd = ["git", "-c", "core.quotePath=false", *args]
    proc = subprocess.run(
        cmd,
        cwd=root,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    stdout = proc.stdout.decode("utf-8", errors="replace")
    stderr = proc.stderr.decode("utf-8", errors="replace")
    if check and proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {stderr.strip()}")
    return stdout


def _strip_comment(line: str) -> str:
    in_quote = False
    quote = ""
    for index, char in enumerate(line):
        if char in {"'", '"'}:
            if not in_quote:
                in_quote = True
                quote = char
            elif quote == char:
                in_quote = False
        if char == "#" and not in_quote:
            return line[:index]
    return line


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return ""
    if value in {"true", "True"}:
        return True
    if value in {"false", "False"}:
        return False
    if value in {"null", "Null", "~"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, root)]
    for raw_line in text.splitlines():
        line = _strip_comment(raw_line).rstrip()
        if not line.strip():
            continue
        if line.lstrip().startswith("- "):
            continue
        indent = len(line) - len(line.lstrip(" "))
        if ":" not in line:
            continue
        key, value = line.strip().split(":", 1)
        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            continue
        parent = stack[-1][1]
        if value.strip() == "":
            child: dict[str, Any] = {}
            parent[key.strip()] = child
            stack.append((indent, child))
        else:
            parent[key.strip()] = _parse_scalar(value)
    return root


def nested(data: dict[str, Any], dotted_key: str, default: str) -> str:
    current: Any = data
    for part in dotted_key.split("."):
        if not isinstance(current, dict) or part not in current:
            return default
        current = current[part]
    return str(current)


def norm_path(path: str) -> str:
    return path.replace("\\", "/").strip("/")


def path_for_git(path: str) -> str:
    value = norm_path(path)
    if value and not value.endswith("/") and Path(value).suffix == "":
        value += "/"
    return value


def load_arguments(root: Path) -> dict[str, Any]:
    path = root / ".raptor" / "arguments.yml"
    if not path.exists():
        raise FileNotFoundError(path)
    return parse_simple_yaml(path.read_text(encoding="utf-8"))


def ssot_paths(arguments: dict[str, Any]) -> list[str]:
    keys = [
        ("paths.data_model_dir", "docs/ssot/dbml/"),
        ("paths.high_gherkin_dir", "docs/ssot/habdd/"),
        ("paths.access_control_dir", "docs/ssot/haarm/"),
        ("paths.backend_intent_dir", "docs/ssot/haapi/"),
        ("paths.frontend_intent_dir", "docs/ssot/hapdl/"),
    ]
    values = [path_for_git(nested(arguments, key, default)) for key, default in keys]
    return sorted({value for value in values if value})


def resolve_baseline(root: Path, explicit: str | None) -> Baseline:
    if explicit:
        commit = run_git(root, ["rev-parse", "--verify", explicit]).strip()
        return Baseline(commit=commit, source="explicit", label=explicit)

    attempts = [
        ("session_md", ["log", "-1", "--format=%H", "--", ".raptor/session.md"], "session.md last commit"),
        ("raptor_commit", ["log", "-1", "--format=%H", "--grep=^raptor:"], "latest raptor: commit"),
    ]
    for source, args, label in attempts:
        commit = run_git(root, args, check=False).strip()
        if commit:
            return Baseline(commit=commit, source=source, label=label)

    tag = run_git(
        root,
        ["describe", "--tags", "--match", "raptor/*-done", "--abbrev=0"],
        check=False,
    ).strip()
    if tag:
        commit = run_git(root, ["rev-parse", "--verify", tag]).strip()
        return Baseline(commit=commit, source="tag", label=tag)

    raise LookupError("baseline not found")


def parse_name_status_z(raw: str, source: str) -> list[GitChange]:
    tokens = [token for token in raw.split("\0") if token]
    changes: list[GitChange] = []
    index = 0
    while index < len(tokens):
        status = tokens[index]
        index += 1
        if status.startswith("R"):
            if index + 1 >= len(tokens):
                break
            old_path = norm_path(tokens[index])
            new_path = norm_path(tokens[index + 1])
            index += 2
            changes.append(GitChange(path=new_path, old_path=old_path, change_type="renamed", source=source))
            continue
        if index >= len(tokens):
            break
        path = norm_path(tokens[index])
        index += 1
        change_type = {
            "A": "added",
            "M": "modified",
            "D": "deleted",
            "C": "added",
        }.get(status[:1], "modified")
        changes.append(GitChange(path=path, change_type=change_type, source=source))
    return changes


def diff_name_status(root: Path, left: str, right: str | None, paths: list[str], source: str) -> list[GitChange]:
    span = [left, right] if right else [left]
    raw = run_git(
        root,
        ["diff", "--find-renames", "--name-status", "-z", *[item for item in span if item], "--", *paths],
    )
    return parse_name_status_z(raw, source)


def untracked_changes(root: Path, paths: list[str]) -> list[GitChange]:
    raw = run_git(root, ["ls-files", "--others", "--exclude-standard", "-z", "--", *paths])
    return [GitChange(path=norm_path(path), change_type="added", source="working_tree") for path in raw.split("\0") if path]


def has_head(root: Path) -> bool:
    return bool(run_git(root, ["rev-parse", "--verify", "HEAD"], check=False).strip())


def current_head(root: Path) -> str:
    return run_git(root, ["rev-parse", "--verify", "HEAD"]).strip()


def short(commit: str) -> str:
    return commit[:12] if commit and commit != "HEAD" else commit


def get_operator(args: argparse.Namespace) -> dict[str, str]:
    name = args.operator_name or os.environ.get("GIT_AUTHOR_NAME") or os.environ.get("USERNAME") or os.environ.get("USER") or "unknown"
    email = args.operator_email or os.environ.get("GIT_AUTHOR_EMAIL") or ""
    result = {"name": name, "source": "argument" if args.operator_name else "environment"}
    if email:
        result["email"] = email
    return result


def author_from_git(root: Path, baseline: str, file_path: str) -> tuple[dict[str, str], str, str]:
    raw = run_git(
        root,
        ["log", "-1", "--format=%H|%an|%ae|%aI", f"{baseline}..HEAD", "--", file_path],
        check=False,
    ).strip()
    if not raw:
        return {"name": "unknown", "email": "", "source": "git_commit"}, "", ""
    commit, name, email, committed_at = (raw.split("|", 3) + ["", "", "", ""])[:4]
    return {"name": name, "email": email, "source": "git_commit"}, committed_at, commit


def diff_text(root: Path, baseline: str, right: str | None, change: GitChange) -> str:
    path = change.path
    if change.source == "untracked":
        target = root / path
        if not target.exists():
            return ""
        lines = target.read_text(encoding="utf-8", errors="replace").splitlines()
        body = "\n".join("+" + line for line in lines)
        return f"diff --git a/{path} b/{path}\nnew file mode 100644\n@@ -0,0 +1,{len(lines)} @@\n{body}\n"
    span = [baseline, right] if right else [baseline]
    return run_git(root, ["diff", "--unified=3", *[item for item in span if item], "--", path], check=False)


def dsl_for_path(path: str, arguments: dict[str, Any]) -> tuple[str, str]:
    path = norm_path(path)
    mapping = [
        ("dbml", "first_class", nested(arguments, "paths.data_model_dir", "docs/ssot/dbml/")),
        ("habdd", "first_class", nested(arguments, "paths.high_gherkin_dir", "docs/ssot/habdd/")),
        ("haarm", "first_class", nested(arguments, "paths.access_control_dir", "docs/ssot/haarm/")),
        ("haapi", "first_class", nested(arguments, "paths.backend_intent_dir", "docs/ssot/haapi/")),
        ("hapdl", "first_class", nested(arguments, "paths.frontend_intent_dir", "docs/ssot/hapdl/")),
    ]
    name = Path(path).name.lower()
    if name == "glossary.md":
        return "glossary", "supporting"
    if name == "seeds.md":
        return "seeds", "supporting"
    if name == "constraints.md":
        return "constraints", "supporting"
    for dsl, ssot_class, prefix in mapping:
        if path.startswith(norm_path(prefix).rstrip("/") + "/"):
            return dsl, ssot_class
    return "unknown", "supporting"


def detect_location(dsl: str, lines: list[str]) -> tuple[str, list[dict[str, str]]]:
    joined = "\n".join(line[1:] if line[:1] in {"+", "-", " "} else line for line in lines)
    patterns = {
        "dbml": [(r"\bTable\s+([A-Za-z0-9_]+)", "table"), (r"\bRef\b", "ref")],
        "habdd": [(r"Feature:\s*(.+)", "feature"), (r"Scenario(?: Outline)?:\s*(.+)", "scenario")],
        "haarm": [(r"^\s*(roles|permissions|resources|constraints)\s*:", "section")],
        "haapi": [(r"^\s*(api|operations|endpoints|entity)\s*:\s*([^\n#]+)?", "section")],
        "hapdl": [(r"^\s*(page|entity|components|api)\s*:\s*([^\n#]+)?", "section")],
    }
    for pattern, kind in patterns.get(dsl, []):
        match = re.search(pattern, joined, re.MULTILINE)
        if match:
            name = (match.group(2) if len(match.groups()) >= 2 and match.group(2) else match.group(1)).strip()
            return f"{kind} {name}", [{"kind": kind, "name": name, "action": "changed"}]
    return "unknown", []


def parse_hunks(diff: str, dsl: str) -> tuple[list[Hunk], dict[str, int], list[dict[str, str]]]:
    hunks: list[Hunk] = []
    current_header = ""
    current_lines: list[str] = []
    semantic: list[dict[str, str]] = []

    def flush() -> None:
        nonlocal current_header, current_lines, semantic
        if not current_header:
            return
        added = sum(1 for line in current_lines if line.startswith("+") and not line.startswith("+++"))
        removed = sum(1 for line in current_lines if line.startswith("-") and not line.startswith("---"))
        location, summary = detect_location(dsl, current_lines)
        semantic.extend(summary)
        snippet = [
            line
            for line in current_lines
            if (line.startswith("+") and not line.startswith("+++")) or (line.startswith("-") and not line.startswith("---"))
        ][:12]
        hunks.append(Hunk(location=location, hunk_header=current_header, added=added, removed=removed, snippet=snippet))

    for line in diff.splitlines():
        if line.startswith("@@"):
            flush()
            current_header = line
            current_lines = []
        elif current_header:
            current_lines.append(line)
    flush()
    summary = {
        "added_lines": sum(hunk.added for hunk in hunks),
        "removed_lines": sum(hunk.removed for hunk in hunks),
    }
    if not hunks and diff:
        added = sum(1 for line in diff.splitlines() if line.startswith("+") and not line.startswith("+++"))
        removed = sum(1 for line in diff.splitlines() if line.startswith("-") and not line.startswith("---"))
        summary = {"added_lines": added, "removed_lines": removed}
    return hunks, summary, semantic


def impact_targets(dsl: str, arguments: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    paths = {
        "dbml": [
            nested(arguments, "paths.backend_intent_dir", "docs/ssot/haapi/"),
            nested(arguments, "paths.frontend_intent_dir", "docs/ssot/hapdl/"),
            nested(arguments, "paths.access_control_dir", "docs/ssot/haarm/"),
        ],
        "haarm": [
            nested(arguments, "paths.backend_intent_dir", "docs/ssot/haapi/"),
            nested(arguments, "paths.frontend_intent_dir", "docs/ssot/hapdl/"),
        ],
        "habdd": [
            nested(arguments, "paths.traceability_file", ".raptor/traceability.md"),
            nested(arguments, "paths.backend_intent_dir", "docs/ssot/haapi/"),
        ],
        "haapi": [
            nested(arguments, "paths.frontend_intent_dir", "docs/ssot/hapdl/"),
            nested(arguments, "paths.traceability_file", ".raptor/traceability.md"),
        ],
        "hapdl": [nested(arguments, "paths.backend_intent_dir", "docs/ssot/haapi/")],
        "glossary": [nested(arguments, "paths.data_model_dir", "docs/ssot/dbml/")],
        "seeds": [nested(arguments, "paths.data_model_dir", "docs/ssot/dbml/")],
        "constraints": [nested(arguments, "paths.data_model_dir", "docs/ssot/dbml/")],
    }.get(dsl, [])
    affected = {
        "dbml": ["haapi", "hapdl", "haarm"],
        "haarm": ["haapi", "hapdl"],
        "habdd": ["traceability", "haapi"],
        "haapi": ["hapdl", "traceability"],
        "hapdl": ["haapi"],
        "glossary": ["dbml"],
        "seeds": ["dbml"],
        "constraints": ["dbml"],
    }.get(dsl, ["verify"])
    stale = {
        "dbml": ["openapi", "lofi", "designbrief"],
        "haarm": ["openapi", "lofi", "designbrief"],
        "habdd": ["isabdd"],
        "haapi": ["openapi", "isabdd"],
        "hapdl": ["lofi", "designbrief"],
    }.get(dsl, [])
    return [norm_path(path) for path in paths], affected, stale


def fingerprint_for(baseline: str, mode: str, change: GitChange, diff: str) -> str:
    normalized = "\n".join(line.rstrip() for line in diff.splitlines() if not line.startswith("index "))
    payload = f"{baseline}|{mode}|{change.path}|{change.old_path or ''}|{change.change_type}|{normalized}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def impact_id_for(fingerprint: str) -> str:
    return "IMPACT-" + fingerprint[:12]


def existing_fingerprints(output_dir: Path) -> dict[str, tuple[Path, str]]:
    found: dict[str, tuple[Path, str]] = {}
    if not output_dir.exists():
        return found
    for path in output_dir.glob("HSYNC-*.yml"):
        current_id = ""
        for raw in path.read_text(encoding="utf-8", errors="replace").splitlines():
            line = raw.strip()
            if line.startswith("- id: "):
                current_id = line.split(":", 1)[1].strip().strip('"')
            elif line.startswith("fingerprint: "):
                fp = line.split(":", 1)[1].strip().strip('"')
                if fp and current_id:
                    found[fp] = (path, current_id)
    return found


def next_sync_id(output_dir: Path, now: dt.datetime) -> str:
    prefix = "HSYNC-" + now.strftime("%Y%m%d") + "-"
    max_number = 0
    if output_dir.exists():
        for path in output_dir.glob(prefix + "*.yml"):
            match = re.match(rf"{re.escape(prefix)}(\d{{3}})\.yml$", path.name)
            if match:
                max_number = max(max_number, int(match.group(1)))
    return prefix + f"{max_number + 1:03d}"


def yaml_scalar(value: Any) -> str:
    if value is None:
        return '""'
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    text = str(value)
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_inline_dict(values: dict[str, Any]) -> str:
    pairs = [f"{key}: {yaml_scalar(value)}" for key, value in values.items() if value is not None]
    return "{ " + ", ".join(pairs) + " }"


def yaml_inline_list(values: list[str]) -> str:
    return "[" + ", ".join(yaml_scalar(value) for value in values) + "]"


def render_hsync(
    sync_id: str,
    now: dt.datetime,
    mode: str,
    baseline: Baseline,
    head_commit: str,
    dirty: bool,
    operator: dict[str, str],
    human_note: str,
    decision_ref: str,
    changes: list[ChangeRecord],
) -> str:
    lines: list[str] = [
        f"schema_version: {yaml_scalar(SCHEMA_VERSION)}",
        "sync:",
        f"  id: {yaml_scalar(sync_id)}",
        f"  scanned_at: {yaml_scalar(now.isoformat())}",
        f"  mode: {yaml_scalar(mode)}",
        "  baseline:",
        f"    commit: {yaml_scalar(baseline.commit)}",
        f"    source: {yaml_scalar(baseline.source)}",
        f"    label: {yaml_scalar(baseline.label)}",
        "  head:",
        f"    commit: {yaml_scalar(head_commit)}",
        f"    dirty: {yaml_scalar(dirty)}",
        f"  operator: {yaml_inline_dict(operator)}",
        f"  human_note: {yaml_scalar(human_note)}",
        f"  decision_ref: {yaml_scalar(decision_ref)}",
        "changes:",
    ]
    for change in changes:
        lines.extend(
            [
                f"  - id: {yaml_scalar(change.id)}",
                f"    impact_id: {yaml_scalar(change.impact_id)}",
                f"    fingerprint: {yaml_scalar(change.fingerprint)}",
                f"    file: {yaml_scalar(change.file)}",
                f"    old_file: {yaml_scalar(change.old_file or '')}",
                f"    ssot_class: {yaml_scalar(change.ssot_class)}",
                f"    dsl: {yaml_scalar(change.dsl)}",
                f"    change_type: {yaml_scalar(change.change_type)}",
                f"    risk: {yaml_scalar(change.risk)}",
                f"    source: {yaml_scalar(change.source)}",
                f"    author: {yaml_inline_dict(change.author)}",
                f"    committed_at: {yaml_scalar(change.committed_at)}",
                f"    commit: {yaml_scalar(change.commit)}",
                "    diff_summary:",
                f"      added_lines: {change.diff_summary.get('added_lines', 0)}",
                f"      removed_lines: {change.diff_summary.get('removed_lines', 0)}",
            ]
        )
        if change.semantic_summary:
            lines.append("    semantic_summary:")
            for item in change.semantic_summary:
                lines.append(f"      - {yaml_inline_dict(item)}")
        else:
            lines.append("    semantic_summary: []")
        if change.hunks:
            lines.append("    hunks:")
            for hunk in change.hunks:
                lines.extend(
                    [
                        f"      - location: {yaml_scalar(hunk.location)}",
                        f"        hunk_header: {yaml_scalar(hunk.hunk_header)}",
                        f"        added: {hunk.added}",
                        f"        removed: {hunk.removed}",
                        "        snippet:",
                    ]
                )
                if hunk.snippet:
                    for line in hunk.snippet:
                        lines.append(f"          - {yaml_scalar(line)}")
                else:
                    lines.append("          []")
        else:
            lines.append("    hunks: []")
        lines.extend(
            [
                f"    effective_human_note: {yaml_scalar(human_note)}",
                f"    effective_decision_ref: {yaml_scalar(decision_ref or sync_id + '#' + change.id)}",
                "    impact_assessment:",
                f"      affected_dsls: {yaml_inline_list(change.impact_assessment['affected_dsls'])}",
                f"      stale_generated: {yaml_inline_list(change.impact_assessment['stale_generated'])}",
                "      needs_verify: true",
            ]
        )
    return "\n".join(lines) + "\n"


def collect_changes(
    root: Path,
    baseline: Baseline,
    mode: str,
    paths: list[str],
) -> tuple[str, list[GitChange], bool]:
    committed = diff_name_status(root, baseline.commit, "HEAD", paths, "committed") if has_head(root) else []
    dirty = bool(diff_name_status(root, "HEAD", None, paths, "working_tree") if has_head(root) else []) or bool(
        untracked_changes(root, paths)
    )

    if mode == "auto":
        if dirty and committed:
            effective_mode = "mixed"
        elif dirty:
            effective_mode = "working_tree"
        else:
            effective_mode = "committed"
    else:
        effective_mode = mode

    if effective_mode == "committed":
        return effective_mode, committed, dirty
    if effective_mode == "working_tree":
        changes = diff_name_status(root, baseline.commit, None, paths, "working_tree")
        tracked_paths = {change.path for change in changes}
        for change in untracked_changes(root, paths):
            if change.path not in tracked_paths:
                change.source = "untracked"
                changes.append(change)
        return effective_mode, changes, dirty

    combined: dict[str, GitChange] = {change.path: change for change in committed}
    for change in diff_name_status(root, "HEAD", None, paths, "working_tree"):
        combined[change.path] = change
    for change in untracked_changes(root, paths):
        if change.path not in combined:
            change.source = "untracked"
            combined[change.path] = change
    return effective_mode, list(combined.values()), dirty


def build_records(
    root: Path,
    arguments: dict[str, Any],
    baseline: Baseline,
    mode: str,
    operator: dict[str, str],
    scanned_at: str,
    changes: list[GitChange],
    existing: dict[str, tuple[Path, str]],
) -> tuple[list[ChangeRecord], int]:
    records: list[ChangeRecord] = []
    skipped = 0
    for change in changes:
        right = "HEAD" if change.source == "committed" else None
        diff = diff_text(root, baseline.commit, right, change)
        fingerprint = fingerprint_for(baseline.commit, mode, change, diff)
        if fingerprint in existing:
            skipped += 1
            continue
        dsl, ssot_class = dsl_for_path(change.path, arguments)
        hunks, diff_summary, semantic = parse_hunks(diff, dsl)
        risk = "high" if change.change_type in {"deleted", "renamed"} else "medium"
        if change.source == "committed":
            author, committed_at, commit = author_from_git(root, baseline.commit, change.path)
        else:
            author = {**operator, "source": change.source}
            committed_at = scanned_at
            commit = "WORKTREE"
        targets, affected, stale = impact_targets(dsl, arguments)
        record_number = len(records) + 1
        records.append(
            ChangeRecord(
                id=f"C{record_number:03d}",
                impact_id=impact_id_for(fingerprint),
                fingerprint=fingerprint,
                file=change.path,
                old_file=change.old_path,
                ssot_class=ssot_class,
                dsl=dsl,
                change_type=change.change_type,
                risk=risk,
                source=change.source,
                author=author,
                committed_at=committed_at,
                commit=commit,
                diff_summary=diff_summary,
                semantic_summary=semantic,
                hunks=hunks,
                impact_assessment={
                    "target_artifacts": targets,
                    "affected_dsls": affected,
                    "stale_generated": stale,
                },
            )
        )
    return records, skipped


def skill_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def manage_impact_script() -> Path:
    return skill_root_from_script().parent / "rapt-core" / "scripts" / "manage_impact_matrix.py"


def call_python(script: Path, args: list[str], cwd: Path) -> None:
    proc = subprocess.run([sys.executable, str(script), *args], cwd=cwd, text=True, encoding="utf-8")
    if proc.returncode != 0:
        raise RuntimeError(f"{script.name} failed with exit code {proc.returncode}")


def upsert_impacts(
    root: Path,
    script: Path,
    impact_file: str,
    sync_file: Path,
    sync_id: str,
    decision_ref: str,
    changes: list[ChangeRecord],
) -> int:
    count = 0
    for change in changes:
        targets = change.impact_assessment.get("target_artifacts", [])
        if not targets:
            targets = [change.file]
        for target_index, target in enumerate(targets, start=1):
            impact_id = change.impact_id if target_index == 1 else f"{change.impact_id}_{target_index}"
            source_ref = f"{norm_path(str(sync_file))}#changes[{change.id}]"
            decision_id = decision_ref or f"{sync_id}#{change.id}"
            note = f"人工修改 {change.dsl} {change.file}，需由 rapt-verify 驗證 {target} 是否同步。"
            call_python(
                script,
                [
                    "--file",
                    impact_file,
                    "upsert",
                    "--id",
                    impact_id,
                    "--source-type",
                    "manual_change",
                    "--source-ref",
                    source_ref,
                    "--target-artifact",
                    target,
                    "--impact-type",
                    "verify",
                    "--decision-id",
                    decision_id,
                    "--status",
                    "open",
                    "--owner-skill",
                    "rapt-verify",
                    "--notes",
                    note,
                ],
                root,
            )
            count += 1
    call_python(script, ["--file", impact_file, "validate"], root)
    return count


def ensure_decision_traceability(path: Path) -> None:
    if path.exists():
        text = path.read_text(encoding="utf-8", errors="replace")
    else:
        text = "# RAPTor Traceability\n"
    if "## Decision Traceability" not in text:
        text = text.rstrip() + "\n\n## Decision Traceability\n\n| decision_id | cic_id | status | affected_artifacts | summary |\n|---|---|---|---|---|\n"
    elif "| decision_id | cic_id | status | affected_artifacts | summary |" not in text:
        text = text.rstrip() + "\n\n| decision_id | cic_id | status | affected_artifacts | summary |\n|---|---|---|---|---|\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def append_traceability(root: Path, arguments: dict[str, Any], sync_id: str, decision_ref: str, human_note: str, changes: list[ChangeRecord]) -> None:
    rel = nested(arguments, "paths.traceability_file", ".raptor/traceability.md")
    path = root / rel
    ensure_decision_traceability(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.rstrip().splitlines()
    existing = "\n".join(lines)
    additions: list[str] = []
    for change in changes:
        decision_id = decision_ref or f"{sync_id}#{change.id}"
        if decision_id in existing:
            continue
        summary = human_note or f"人工修改 {change.dsl} {change.file}"
        additions.append(f"| {decision_id} | — | applied (manual) | {change.file} | {summary} |")
    if additions:
        path.write_text("\n".join(lines + additions) + "\n", encoding="utf-8", newline="\n")


def append_session(root: Path, sync_id: str, sync_file: Path, mode: str, changes: list[ChangeRecord], impact_count: int) -> None:
    path = root / ".raptor" / "session.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else "# RAPTor Session\n"
    files = ", ".join(change.file for change in changes[:5])
    if len(changes) > 5:
        files += f", ... (+{len(changes) - 5})"
    block = (
        "\n\n## Human Sync\n\n"
        f"- sync_id: {sync_id}\n"
        f"- mode: {mode}\n"
        f"- record: {norm_path(str(sync_file))}\n"
        f"- changes: {len(changes)}\n"
        f"- impact_entries: {impact_count}\n"
        f"- files: {files}\n"
        "- next: /rapt-verify\n"
    )
    path.write_text(text.rstrip() + block, encoding="utf-8", newline="\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="專案根目錄，預設目前工作目錄")
    parser.add_argument("--baseline", help="明確指定 baseline commit/tag")
    parser.add_argument("--mode", choices=["auto", "committed", "working_tree", "mixed"], default="auto")
    parser.add_argument("--human-note", default="")
    parser.add_argument("--decision-ref", default="")
    parser.add_argument("--operator-name")
    parser.add_argument("--operator-email")
    parser.add_argument("--output-dir", default=".raptor/human-sync")
    parser.add_argument("--impact-file", default=".raptor/impact-matrix.yml")
    parser.add_argument("--skip-impact", action="store_true")
    parser.add_argument("--skip-traceability", action="store_true")
    parser.add_argument("--skip-session", action="store_true")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    try:
        arguments = load_arguments(root)
    except FileNotFoundError as exc:
        print(f"ERROR arguments.yml not found: {exc}", file=sys.stderr)
        return EXIT_ARGUMENTS_NOT_FOUND

    try:
        baseline = resolve_baseline(root, args.baseline)
    except (LookupError, RuntimeError) as exc:
        print(f"ERROR cannot resolve baseline: {exc}", file=sys.stderr)
        print("請用 --baseline <commit> 指定人工修改前的基準 commit。", file=sys.stderr)
        return EXIT_BASELINE_NOT_FOUND

    paths = ssot_paths(arguments)
    now = dt.datetime.now().astimezone()
    scanned_at = now.isoformat()
    operator = get_operator(args)

    try:
        effective_mode, raw_changes, dirty = collect_changes(root, baseline, args.mode, paths)
        output_dir = root / args.output_dir
        existing = existing_fingerprints(output_dir)
        records, skipped = build_records(root, arguments, baseline, effective_mode, operator, scanned_at, raw_changes, existing)
    except RuntimeError as exc:
        print(f"ERROR git scan failed: {exc}", file=sys.stderr)
        return EXIT_GIT_ERROR

    if not raw_changes:
        print("OK no SSoT changes detected; you may run /rapt-verify directly.")
        return 0
    if not records:
        print(f"OK all {skipped} detected change(s) already have HSYNC records; no duplicate created.")
        return 0

    output_dir.mkdir(parents=True, exist_ok=True)
    sync_id = next_sync_id(output_dir, now)
    sync_file = output_dir / f"{sync_id}.yml"
    head_commit = current_head(root) if has_head(root) else "NO_HEAD"
    text = render_hsync(
        sync_id=sync_id,
        now=now,
        mode=effective_mode,
        baseline=baseline,
        head_commit=head_commit,
        dirty=dirty,
        operator=operator,
        human_note=args.human_note,
        decision_ref=args.decision_ref,
        changes=records,
    )
    sync_file.write_text(text, encoding="utf-8", newline="\n")

    impact_count = 0
    if not args.skip_impact:
        impact_count = upsert_impacts(root, manage_impact_script(), args.impact_file, sync_file.relative_to(root), sync_id, args.decision_ref, records)
    if not args.skip_traceability:
        append_traceability(root, arguments, sync_id, args.decision_ref, args.human_note, records)
    if not args.skip_session:
        append_session(root, sync_id, sync_file.relative_to(root), effective_mode, records, impact_count)

    print(f"OK rapt-human-sync completed: {sync_id}")
    print(f"mode={effective_mode} baseline={short(baseline.commit)} source={baseline.source}")
    print(f"changes={len(records)} skipped_existing={skipped} impact_entries={impact_count}")
    print(f"record={norm_path(str(sync_file.relative_to(root)))}")
    if dirty:
        print("NOTE working tree contains SSoT changes; commit them if you need full git who/when provenance.")
    print("NEXT /rapt-verify")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
