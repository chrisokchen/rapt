#!/usr/bin/env python3
"""管理 `.raptor/impact-matrix.yml` 的 stdlib-only 工具。"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from pathlib import Path


REQUIRED_FIELDS = {
    "id",
    "source_type",
    "source_ref",
    "target_artifact",
    "impact_type",
    "decision_id",
    "status",
}


@dataclass
class Entry:
    values: dict[str, str] = field(default_factory=dict)

    @property
    def id(self) -> str:
        return self.values.get("id", "")


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def parse_pair(text: str) -> tuple[str, str]:
    key, value = text.split(":", 1)
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return key.strip(), value


def parse_matrix(text: str) -> list[Entry]:
    entries: list[Entry] = []
    current: Entry | None = None
    for raw in text.splitlines():
        line = raw.rstrip()
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("- "):
            if current:
                entries.append(current)
            current = Entry()
            body = line[2:].strip()
            if body:
                key, value = parse_pair(body)
                current.values[key] = value
            continue
        if current and line.startswith("  ") and ":" in line:
            key, value = parse_pair(line.strip())
            current.values[key] = value
    if current:
        entries.append(current)
    return entries


def render_matrix(entries: list[Entry]) -> str:
    lines = ["# RAPTor Impact Matrix", "# 由 rapt-core/scripts/manage_impact_matrix.py 維護。"]
    order = [
        "id",
        "source_type",
        "source_ref",
        "target_artifact",
        "impact_type",
        "decision_id",
        "status",
        "owner_skill",
        "notes",
    ]
    for entry in entries:
        lines.append(f"- id: {yaml_quote(entry.values.get('id', ''))}")
        for key in order[1:]:
            if key in entry.values:
                lines.append(f"  {key}: {yaml_quote(entry.values[key])}")
        for key in sorted(set(entry.values) - set(order)):
            lines.append(f"  {key}: {yaml_quote(entry.values[key])}")
    return "\n".join(lines) + "\n"


def load_entries(path: Path) -> list[Entry]:
    if not path.exists():
        return []
    return parse_matrix(path.read_text(encoding="utf-8"))


def validate_entries(entries: list[Entry]) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for index, entry in enumerate(entries, start=1):
        missing = sorted(REQUIRED_FIELDS - set(entry.values))
        if missing:
            errors.append(f"entry #{index} missing: {', '.join(missing)}")
        entry_id = entry.id
        if entry_id in seen:
            errors.append(f"duplicate id: {entry_id}")
        seen.add(entry_id)
        if entry_id and not re.match(r"^IMPACT-[0-9A-Za-z_.-]+$", entry_id):
            errors.append(f"invalid id format: {entry_id}")
    return errors


def cmd_validate(args: argparse.Namespace) -> int:
    errors = validate_entries(load_entries(Path(args.file)))
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    print("OK impact matrix is valid")
    return 0


def cmd_query(args: argparse.Namespace) -> int:
    entries = load_entries(Path(args.file))
    for entry in entries:
        if args.artifact and args.artifact not in entry.values.get("target_artifact", ""):
            continue
        if args.decision_id and args.decision_id != entry.values.get("decision_id"):
            continue
        print(render_matrix([entry]).strip())
    return 0


def cmd_upsert(args: argparse.Namespace) -> int:
    path = Path(args.file)
    entries = load_entries(path)
    values = {
        "id": args.id,
        "source_type": args.source_type,
        "source_ref": args.source_ref,
        "target_artifact": args.target_artifact,
        "impact_type": args.impact_type,
        "decision_id": args.decision_id,
        "status": args.status,
        "owner_skill": args.owner_skill,
        "notes": args.notes,
    }
    values = {key: value for key, value in values.items() if value is not None}
    for entry in entries:
        if entry.id == args.id:
            entry.values.update(values)
            break
    else:
        entries.append(Entry(values))
    errors = validate_entries(entries)
    if errors:
        for error in errors:
            print(f"ERROR {error}")
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_matrix(entries), encoding="utf-8", newline="\n")
    print(f"OK upserted {args.id}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default=".raptor/impact-matrix.yml")
    sub = parser.add_subparsers(dest="cmd", required=True)
    validate = sub.add_parser("validate")
    validate.set_defaults(func=cmd_validate)
    query = sub.add_parser("query")
    query.add_argument("--artifact")
    query.add_argument("--decision-id")
    query.set_defaults(func=cmd_query)
    upsert = sub.add_parser("upsert")
    upsert.add_argument("--id", required=True)
    upsert.add_argument("--source-type", required=True)
    upsert.add_argument("--source-ref", required=True)
    upsert.add_argument("--target-artifact", required=True)
    upsert.add_argument("--impact-type", required=True)
    upsert.add_argument("--decision-id", required=True)
    upsert.add_argument("--status", default="open")
    upsert.add_argument("--owner-skill")
    upsert.add_argument("--notes")
    upsert.set_defaults(func=cmd_upsert)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
