#!/usr/bin/env python3
"""從 RAPTor SSoT 抽取 deterministic impact graph。

本工具只做保守的文字結構抽取，不做模糊語意判斷，也不修改輸入。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


TABLE_RE = re.compile(r"^\s*Table\s+(?P<name>[A-Za-z_][\w.]*)\s*\{")
INLINE_REF_RE = re.compile(
    r"\[\s*ref\s*:\s*[<>\-]*\s*(?P<table>[A-Za-z_][\w.]*)\.(?P<field>[A-Za-z_]\w*)",
    re.IGNORECASE,
)
DECLARED_REF_RE = re.compile(
    r"^\s*Ref(?:\s+\w+)?\s*:\s*"
    r"(?P<left>[A-Za-z_][\w.]*)\.(?:[A-Za-z_]\w*)\s*"
    r"[<>\-]+\s*"
    r"(?P<right>[A-Za-z_][\w.]*)\.(?:[A-Za-z_]\w*)",
    re.IGNORECASE,
)
YAML_VALUE_RE = re.compile(
    r"^(?P<indent>\s*)(?:-\s+)?(?P<key>[A-Za-z_][\w-]*)\s*:\s*(?P<value>.*?)\s*$"
)
MARKDOWN_HEADING_RE = re.compile(r"^##\s+(?P<title>.+?)\s*$")


@dataclass(frozen=True)
class Node:
    id: str
    type: str
    label: str
    source: str


@dataclass(frozen=True)
class Edge:
    source: str
    target: str
    type: str
    evidence: str
    confidence: str


class Graph:
    """去重並序列化 impact graph。"""

    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: dict[tuple[str, str, str, str], Edge] = {}
        self.warnings: list[str] = []
        self.coverage = {
            "dbml_tables": 0,
            "dbml_relationships": 0,
            "haapi_files": 0,
            "haapi_entity_bindings": 0,
            "hapdl_files": 0,
            "page_api_bindings": 0,
            "haarm_files": 0,
            "permission_bindings": 0,
            "l2_rows": 0,
            "l2_table_mappings": 0,
            "l3_rows": 0,
            "l3_mappings": 0,
        }

    def add_node(self, node_id: str, node_type: str, label: str, source: str) -> None:
        self.nodes.setdefault(node_id, Node(node_id, node_type, label, source))

    def add_edge(
        self,
        source: str,
        target: str,
        edge_type: str,
        evidence: str,
        confidence: str,
    ) -> None:
        key = (source, target, edge_type, evidence)
        self.edges.setdefault(
            key, Edge(source, target, edge_type, evidence, confidence)
        )

    def as_dict(self) -> dict:
        return {
            "schema_version": 1,
            "nodes": [
                {
                    "id": node.id,
                    "type": node.type,
                    "label": node.label,
                    "source": node.source,
                }
                for node in sorted(self.nodes.values(), key=lambda item: item.id)
            ],
            "edges": [
                {
                    "from": edge.source,
                    "to": edge.target,
                    "type": edge.type,
                    "evidence": edge.evidence,
                    "confidence": edge.confidence,
                }
                for edge in sorted(
                    self.edges.values(),
                    key=lambda item: (
                        item.source,
                        item.target,
                        item.type,
                        item.evidence,
                    ),
                )
            ],
            "coverage": self.coverage,
            "warnings": self.warnings,
        }


def clean_scalar(value: str) -> str:
    """移除 YAML 常見引號、註解與空集合。"""

    value = value.split(" #", 1)[0].strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value.strip()


def split_values(value: str) -> list[str]:
    """保守拆解 YAML/Markdown 的 list-like 欄位。"""

    value = clean_scalar(value)
    if not value or value in {"[]", "-", "null", "~"}:
        return []
    if value.startswith("[") and value.endswith("]"):
        value = value[1:-1]
    return [
        clean_scalar(item)
        for item in re.split(r"\s*,\s*|<br\s*/?>", value)
        if clean_scalar(item)
    ]


def rel_source(path: Path, root: Path, line: int) -> str:
    try:
        relative = path.resolve().relative_to(root.resolve())
    except ValueError:
        relative = path
    return f"{relative.as_posix()}:{line}"


def iter_text_files(root: Path, patterns: Iterable[str]) -> Iterable[Path]:
    seen: set[Path] = set()
    for pattern in patterns:
        for path in root.rglob(pattern):
            if path.is_file() and path not in seen:
                seen.add(path)
                yield path


def read_lines(path: Path, graph: Graph) -> list[str]:
    try:
        return path.read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as exc:
        graph.warnings.append(f"無法讀取 {path}: {exc}")
        return []


def parse_dbml(path: Path, root: Path, graph: Graph) -> None:
    lines = read_lines(path, graph)
    current_table: str | None = None
    brace_depth = 0

    for number, line in enumerate(lines, start=1):
        table_match = TABLE_RE.match(line)
        if table_match:
            current_table = table_match.group("name")
            brace_depth = line.count("{") - line.count("}")
            graph.add_node(
                f"table:{current_table}",
                "table",
                current_table,
                rel_source(path, root, number),
            )
            graph.coverage["dbml_tables"] += 1
            continue

        ref_match = DECLARED_REF_RE.match(line)
        if ref_match:
            left = ref_match.group("left")
            right = ref_match.group("right")
            for table in (left, right):
                graph.add_node(
                    f"table:{table}", "table", table, rel_source(path, root, number)
                )
            graph.add_edge(
                f"table:{left}",
                f"table:{right}",
                "table_rel",
                rel_source(path, root, number),
                "high",
            )
            graph.coverage["dbml_relationships"] += 1

        if current_table:
            inline_match = INLINE_REF_RE.search(line)
            if inline_match:
                target = inline_match.group("table")
                graph.add_node(
                    f"table:{target}",
                    "table",
                    target,
                    rel_source(path, root, number),
                )
                graph.add_edge(
                    f"table:{current_table}",
                    f"table:{target}",
                    "table_rel",
                    rel_source(path, root, number),
                    "high",
                )
                graph.coverage["dbml_relationships"] += 1

            brace_depth += line.count("{") - line.count("}")
            if brace_depth <= 0:
                current_table = None


def yaml_entries(path: Path, root: Path, graph: Graph) -> list[tuple[int, int, str, str]]:
    entries: list[tuple[int, int, str, str]] = []
    for number, line in enumerate(read_lines(path, graph), start=1):
        match = YAML_VALUE_RE.match(line)
        if not match:
            continue
        entries.append(
            (
                number,
                len(match.group("indent")),
                match.group("key"),
                clean_scalar(match.group("value")),
            )
        )
    return entries


def parse_haapi(path: Path, root: Path, graph: Graph) -> None:
    graph.coverage["haapi_files"] += 1
    entries = yaml_entries(path, root, graph)
    entities = [(line, value) for line, _, key, value in entries if key == "entity" and value]
    operations = [
        (line, value)
        for line, _, key, value in entries
        if key in {"operationId", "operation_id", "operation"} and value
    ]
    artifact_id = f"haapi-file:{path.stem}"
    graph.add_node(
        artifact_id, "haapi_file", path.stem, rel_source(path, root, 1)
    )

    if not operations:
        operations = [(1, path.stem)]

    for line, operation in operations:
        op_id = f"haapi:{operation}"
        graph.add_node(
            op_id, "haapi_operation", operation, rel_source(path, root, line)
        )
        graph.add_edge(
            artifact_id,
            op_id,
            "contains_operation",
            rel_source(path, root, line),
            "high",
        )
        for entity_line, entity in entities:
            table_id = f"table:{entity}"
            graph.add_node(
                table_id, "table", entity, rel_source(path, root, entity_line)
            )
            graph.add_edge(
                op_id,
                table_id,
                "entity_table",
                rel_source(path, root, entity_line),
                "high",
            )
            graph.coverage["haapi_entity_bindings"] += 1


def parse_hapdl(path: Path, root: Path, graph: Graph) -> None:
    graph.coverage["hapdl_files"] += 1
    entries = yaml_entries(path, root, graph)
    pages = [
        (line, value)
        for line, _, key, value in entries
        if key in {"page_id", "pageId"} and value
    ]
    if not pages:
        pages = [
            (line, value)
            for line, indent, key, value in entries
            if key == "id" and indent <= 4 and value
        ][:1]
    if not pages:
        pages = [(1, path.stem)]

    api_refs = [
        (line, value)
        for line, _, key, value in entries
        if key
        in {
            "operation",
            "operationId",
            "operation_id",
            "api",
            "endpoint",
            "query",
            "command",
        }
        and value
        and not value.startswith("{")
    ]

    for page_line, page in pages:
        page_id = f"hapdl:{page}"
        graph.add_node(
            page_id, "hapdl_page", page, rel_source(path, root, page_line)
        )
        for api_line, api_ref in api_refs:
            api_id = f"haapi:{api_ref}"
            graph.add_node(
                api_id, "haapi_operation", api_ref, rel_source(path, root, api_line)
            )
            graph.add_edge(
                page_id,
                api_id,
                "page_api",
                rel_source(path, root, api_line),
                "high" if "." in api_ref else "medium",
            )
            graph.coverage["page_api_bindings"] += 1


def parse_haarm(path: Path, root: Path, graph: Graph) -> None:
    graph.coverage["haarm_files"] += 1
    entries = yaml_entries(path, root, graph)
    permissions = [
        (line, value)
        for line, indent, key, value in entries
        if key in {"permission", "permission_id", "permissionId"}
        or (key == "id" and indent >= 2 and value and ":" in value)
    ]
    api_refs = [
        (line, value)
        for line, _, key, value in entries
        if key in {"api", "operation", "operationId", "operation_id"} and value
    ]
    page_refs = [
        (line, value)
        for line, _, key, value in entries
        if key in {"page", "page_id", "pageId"} and value
    ]

    for perm_line, permission in permissions:
        perm_id = f"haarm:{permission}"
        graph.add_node(
            perm_id,
            "haarm_permission",
            permission,
            rel_source(path, root, perm_line),
        )
        for api_line, api_ref in api_refs:
            api_id = f"haapi:{api_ref}"
            graph.add_node(
                api_id, "haapi_operation", api_ref, rel_source(path, root, api_line)
            )
            graph.add_edge(
                perm_id,
                api_id,
                "permission_api",
                rel_source(path, root, api_line),
                "medium",
            )
            graph.coverage["permission_bindings"] += 1
        for page_line, page_ref in page_refs:
            page_id = f"hapdl:{page_ref}"
            graph.add_node(
                page_id, "hapdl_page", page_ref, rel_source(path, root, page_line)
            )
            graph.add_edge(
                perm_id,
                page_id,
                "permission_page",
                rel_source(path, root, page_line),
                "medium",
            )
            graph.coverage["permission_bindings"] += 1


def parse_markdown_table(
    path: Path, root: Path, graph: Graph, heading_name: str
) -> list[tuple[dict[str, str], int]]:
    lines = read_lines(path, graph)
    in_section = False
    headers: list[str] = []
    rows: list[tuple[dict[str, str], int]] = []

    for number, line in enumerate(lines, start=1):
        heading = MARKDOWN_HEADING_RE.match(line)
        if heading:
            in_section = heading_name.lower() in heading.group("title").lower()
            headers = []
            continue
        if not in_section or not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not headers:
            headers = cells
            continue
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if len(cells) != len(headers):
            graph.warnings.append(
                f"{rel_source(path, root, number)} 表格欄位數不一致，已略過"
            )
            continue
        rows.append((dict(zip(headers, cells)), number))
    return rows


def parse_traceability(path: Path, root: Path, graph: Graph) -> None:
    if not path.exists():
        graph.warnings.append(f"traceability 不存在：{path}")
        return

    l2_rows = parse_markdown_table(path, root, graph, "L2 Scenario Data Mapping")
    graph.coverage["l2_rows"] = len(l2_rows)
    for row, number in l2_rows:
        scenario = row.get("scenario_id", "").strip()
        if not scenario:
            continue
        scenario_id = f"scenario:{scenario}"
        graph.add_node(
            scenario_id, "scenario", scenario, rel_source(path, root, number)
        )
        tables = split_values(row.get("read_tables", "")) + split_values(
            row.get("write_tables", "")
        )
        for table in tables:
            table_id = f"table:{table}"
            graph.add_node(
                table_id, "table", table, rel_source(path, root, number)
            )
            graph.add_edge(
                scenario_id,
                table_id,
                "scenario_table",
                rel_source(path, root, number),
                "medium",
            )
            graph.coverage["l2_table_mappings"] += 1

    l3_rows = parse_markdown_table(path, root, graph, "L3 Intent Mapping")
    graph.coverage["l3_rows"] = len(l3_rows)
    for row, number in l3_rows:
        scenario = row.get("scenario_id", "").strip()
        if not scenario:
            continue
        scenario_id = f"scenario:{scenario}"
        graph.add_node(
            scenario_id, "scenario", scenario, rel_source(path, root, number)
        )
        mappings = (
            ("haapi_operation", "haapi", "scenario_intent"),
            ("hapdl_page", "hapdl", "scenario_intent"),
            ("haarm_permissions", "haarm", "scenario_intent"),
        )
        for column, prefix, edge_type in mappings:
            for target in split_values(row.get(column, "")):
                target_id = f"{prefix}:{target}"
                graph.add_node(
                    target_id, column, target, rel_source(path, root, number)
                )
                graph.add_edge(
                    scenario_id,
                    target_id,
                    edge_type,
                    rel_source(path, root, number),
                    "high",
                )
                graph.coverage["l3_mappings"] += 1


def render_markdown(data: dict) -> str:
    lines = [
        "# RAPTor Impact Graph",
        "",
        "## Coverage",
        "",
        "| metric | value |",
        "|---|---:|",
    ]
    lines.extend(
        f"| {key} | {value} |" for key, value in data["coverage"].items()
    )
    lines.extend(
        [
            "",
            "## Edges",
            "",
            "| from | type | to | confidence | evidence |",
            "|---|---|---|---|---|",
        ]
    )
    lines.extend(
        "| {from_} | {type_} | {to} | {confidence} | {evidence} |".format(
            from_=edge["from"],
            type_=edge["type"],
            to=edge["to"],
            confidence=edge["confidence"],
            evidence=edge["evidence"],
        )
        for edge in data["edges"]
    )
    if data["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in data["warnings"])
    return "\n".join(lines) + "\n"


def build_graph(ssot_dir: Path, trace: Path | None) -> Graph:
    graph = Graph()
    root = ssot_dir.parent if ssot_dir.name == "ssot" else ssot_dir

    if not ssot_dir.exists():
        raise FileNotFoundError(f"SSoT 目錄不存在：{ssot_dir}")

    for path in iter_text_files(ssot_dir, ("*.dbml",)):
        parse_dbml(path, root, graph)

    for path in iter_text_files(
        ssot_dir, ("*.haapi.yaml", "*.haapi.yml")
    ):
        parse_haapi(path, root, graph)

    for path in iter_text_files(
        ssot_dir, ("*.hapdl.yaml", "*.hapdl.yml", "*.rui.yaml", "*.rui.yml")
    ):
        parse_hapdl(path, root, graph)

    for path in iter_text_files(
        ssot_dir, ("*.haarm.yaml", "*.haarm.yml")
    ):
        parse_haarm(path, root, graph)

    if trace:
        parse_traceability(trace, root, graph)
    return graph


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="抽取 RAPTor DBML/haAPI/haPDL/haARM/traceability 關係圖。"
    )
    parser.add_argument("--ssot-dir", required=True, type=Path)
    parser.add_argument("--trace", type=Path)
    parser.add_argument("--format", choices=("json", "md"), default="json")
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        data = build_graph(args.ssot_dir, args.trace).as_dict()
    except (FileNotFoundError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.format == "json":
        rendered = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
    else:
        rendered = render_markdown(data)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    else:
        sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
