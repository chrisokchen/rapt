#!/usr/bin/env python3
"""RAscore 靜態預檢：只產生 evidence，不直接評分。"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


UI_TERMS = [
    "點擊",
    "按下",
    "輸入框",
    "按鈕",
    "URL",
    "HTTP",
    "selector",
    "click",
    "button",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def line_no(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def scan_features(features_dir: Path) -> dict[str, Any]:
    files = sorted(features_dir.glob("*.feature")) if features_dir.exists() else []
    scenarios: list[dict[str, Any]] = []
    ui_hits: list[dict[str, Any]] = []
    missing_given: list[dict[str, str]] = []
    missing_when: list[dict[str, str]] = []
    missing_then: list[dict[str, str]] = []
    long_scenarios: list[dict[str, Any]] = []
    entity_hints: list[dict[str, Any]] = []
    terms: set[str] = set()

    for file in files:
        text = read_text(file)
        for term in UI_TERMS:
            for match in re.finditer(re.escape(term), text, flags=re.IGNORECASE):
                ui_hits.append({"file": str(file), "line": line_no(text, match.start()), "term": term})

        blocks = re.split(r"(?m)^\s*(?=Scenario(?: Outline)?:)", text)
        for block in blocks:
            header = re.match(r"\s*Scenario(?: Outline)?:\s*(.+)", block)
            if not header:
                continue
            name = header.group(1).strip()
            before_header = text[: text.find(block)] if block in text else ""
            scenario_id_match = re.search(r"(?m)^\s*#\s*scenario_id:\s*(.+)$", block)
            entities_match = re.search(r"(?m)^\s*#\s*entities:\s*(.+)$", block)
            if not entities_match:
                # comments may be immediately before the split block in some renderers
                tail = "\n".join(before_header.splitlines()[-5:])
                entities_match = re.search(r"(?m)^\s*#\s*entities:\s*(.+)$", tail)
            entities = []
            if entities_match:
                entities = [item.strip() for item in re.split(r"[,，]", entities_match.group(1)) if item.strip()]
                entity_hints.append(
                    {
                        "file": str(file),
                        "scenario": name,
                        "scenario_id": scenario_id_match.group(1).strip() if scenario_id_match else "",
                        "entities": entities,
                    }
                )
            steps = re.findall(r"(?m)^\s*(Given|When|Then|And|But)\b(.+)$", block)
            step_words = [step[0] for step in steps]
            entry = {"file": str(file), "name": name, "step_count": len(steps)}
            scenarios.append(entry)
            if "Given" not in step_words:
                missing_given.append({"file": str(file), "scenario": name})
            if "When" not in step_words:
                missing_when.append({"file": str(file), "scenario": name})
            if "Then" not in step_words:
                missing_then.append({"file": str(file), "scenario": name})
            if len(steps) > 8:
                long_scenarios.append(entry)
            for token in re.findall(r"[\w\u4e00-\u9fff]{2,}", name + "\n" + block):
                if token not in {"Given", "When", "Then", "And", "But", "Scenario", "Feature"}:
                    terms.add(token)
            for entity in entities:
                terms.add(entity)

    return {
        "feature_count": len(files),
        "scenario_count": len(scenarios),
        "scenarios": scenarios,
        "scenarios_without_given": missing_given,
        "scenarios_without_when": missing_when,
        "scenarios_without_then": missing_then,
        "ui_detail_terms": ui_hits,
        "long_scenarios": long_scenarios,
        "entity_hints": entity_hints,
        "entity_hint_coverage": {
            "with_entities": len(entity_hints),
            "total_scenarios": len(scenarios),
            "ratio": round(len(entity_hints) / len(scenarios), 4) if scenarios else 0,
        },
        "terms": sorted(terms),
    }


def scan_dbml(dbml_dir: Path) -> dict[str, Any]:
    files = sorted(dbml_dir.glob("*.dbml")) if dbml_dir.exists() else []
    tables: dict[str, dict[str, Any]] = {}
    enums: set[str] = set()
    refs: list[dict[str, str]] = []

    for file in files:
        text = read_text(file)
        for match in re.finditer(r"(?ms)Table\s+([A-Za-z_][\w]*)\s*\{(.*?)\}", text):
            name = match.group(1)
            body = match.group(2)
            columns = []
            has_pk = False
            for raw in body.splitlines():
                line = raw.strip()
                if not line or line.startswith("//"):
                    continue
                col_match = re.match(r"([A-Za-z_][\w]*)\s+", line)
                if col_match:
                    columns.append(col_match.group(1))
                if "[pk" in line.lower() or " primary key" in line.lower():
                    has_pk = True
            tables[name] = {"file": str(file), "columns": columns, "has_pk": has_pk}
        for match in re.finditer(r"Enum\s+([A-Za-z_][\w]*)\s*\{", text):
            enums.add(match.group(1))
        for match in re.finditer(r"(?m)^\s*Ref\s*:?(.+)$", text):
            refs.append({"file": str(file), "ref": match.group(1).strip()})

    tables_without_pk = [
        {"table": name, "file": meta["file"]} for name, meta in tables.items() if not meta["has_pk"]
    ]
    dbml_terms = set(tables.keys())
    for meta in tables.values():
        dbml_terms.update(meta["columns"])
    dbml_terms.update(enums)

    return {
        "file_count": len(files),
        "table_count": len(tables),
        "enum_count": len(enums),
        "refs_count": len(refs),
        "tables": tables,
        "enums": sorted(enums),
        "refs": refs,
        "tables_without_pk": tables_without_pk,
        "terms": sorted(dbml_terms),
    }


def build_cross_spec(gherkin: dict[str, Any], dbml: dict[str, Any]) -> dict[str, Any]:
    g_terms = set(gherkin.get("terms", []))
    d_terms = set(dbml.get("terms", []))
    g_lower = {term.lower(): term for term in g_terms}
    d_lower = {term.lower(): term for term in d_terms}

    matched = sorted(set(g_lower).intersection(d_lower))
    unmatched_g = sorted(term for key, term in g_lower.items() if key not in d_lower)

    scenario_text = " ".join(g_terms).lower()
    orphan_tables = []
    for table in dbml.get("tables", {}):
        if table.lower() not in scenario_text:
            orphan_tables.append(table)

    return {
        "matched_terms": matched,
        "unmatched_gherkin_terms": unmatched_g[:100],
        "orphan_dbml_tables": sorted(orphan_tables),
        "low_confidence_mappings": [],
    }


def parse_markdown_table(text: str) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if not line.strip().startswith("|") or index + 1 >= len(lines):
            continue
        separator = lines[index + 1]
        if "---" not in separator or not separator.strip().startswith("|"):
            continue
        headers = [cell.strip() for cell in line.strip().strip("|").split("|")]
        cursor = index + 2
        while cursor < len(lines) and lines[cursor].strip().startswith("|"):
            cells = [cell.strip() for cell in lines[cursor].strip().strip("|").split("|")]
            if len(cells) == len(headers):
                rows.append(dict(zip(headers, cells)))
            cursor += 1
    return rows


def scan_glossary(glossary_file: Path | None) -> dict[str, Any]:
    if not glossary_file or not glossary_file.exists():
        return {"exists": False, "mappings": [], "term_to_tables": {}, "table_to_terms": {}}
    text = read_text(glossary_file)
    rows = parse_markdown_table(text)
    mappings: list[dict[str, Any]] = []
    term_to_tables: dict[str, list[str]] = {}
    table_to_terms: dict[str, list[str]] = {}
    for row in rows:
        term = row.get("term") or row.get("術語（繁中）") or row.get("術語") or row.get("中文術語") or ""
        table = row.get("dbml_table") or row.get("DBML Table") or row.get("英文") or row.get("english") or ""
        columns = row.get("dbml_columns") or row.get("欄位") or ""
        aliases = row.get("gherkin_synonyms") or row.get("synonyms") or row.get("legacy_aliases") or ""
        if not term and not table:
            continue
        tables = [item.strip() for item in re.split(r"[,，/]", table) if item.strip()]
        mapping = {"term": term, "tables": tables, "columns": columns, "aliases": aliases}
        mappings.append(mapping)
        for candidate in [term] + [item.strip() for item in re.split(r"[,，/]", aliases) if item.strip()]:
            if candidate:
                term_to_tables.setdefault(candidate, [])
                for table_name in tables:
                    if table_name not in term_to_tables[candidate]:
                        term_to_tables[candidate].append(table_name)
        for table_name in tables:
            table_to_terms.setdefault(table_name, [])
            if term and term not in table_to_terms[table_name]:
                table_to_terms[table_name].append(term)
    return {
        "exists": True,
        "mapping_count": len(mappings),
        "mappings": mappings,
        "term_to_tables": term_to_tables,
        "table_to_terms": table_to_terms,
    }


def build_glossary_cross_spec(gherkin: dict[str, Any], dbml: dict[str, Any], glossary: dict[str, Any]) -> dict[str, Any]:
    if not glossary.get("exists"):
        return {
            "glossary_mappings": [],
            "scenario_table_candidates": [],
            "unmapped_entities": [],
            "orphan_dbml_tables_after_glossary": sorted(dbml.get("tables", {}).keys()),
        }
    term_to_tables = glossary.get("term_to_tables", {})
    dbml_tables = set(dbml.get("tables", {}).keys())
    scenario_candidates: list[dict[str, Any]] = []
    mapped_tables: set[str] = set()
    unmapped_entities: list[dict[str, str]] = []
    for hint in gherkin.get("entity_hints", []):
        tables: set[str] = set()
        for entity in hint.get("entities", []):
            matched = [table for table in term_to_tables.get(entity, []) if table in dbml_tables]
            if matched:
                tables.update(matched)
            else:
                unmapped_entities.append(
                    {"file": hint.get("file", ""), "scenario": hint.get("scenario", ""), "entity": entity}
                )
        mapped_tables.update(tables)
        scenario_candidates.append(
            {
                "file": hint.get("file", ""),
                "scenario": hint.get("scenario", ""),
                "scenario_id": hint.get("scenario_id", ""),
                "entities": hint.get("entities", []),
                "candidate_tables": sorted(tables),
            }
        )
    orphan_after = sorted(table for table in dbml_tables if table not in mapped_tables)
    return {
        "glossary_mappings": glossary.get("mappings", []),
        "scenario_table_candidates": scenario_candidates,
        "unmapped_entities": unmapped_entities,
        "orphan_dbml_tables_after_glossary": orphan_after,
    }


def scan_traceability_l2(trace_file: Path | None) -> dict[str, Any]:
    if not trace_file or not trace_file.exists():
        return {"exists": False, "l2_rows": [], "l2_row_count": 0, "low_confidence_rows": 0}
    text = read_text(trace_file)
    l2_section = ""
    match = re.search(r"(?ms)^##\s+L2 Scenario Data Mapping\s*(.*?)(?=^##\s+|\Z)", text)
    if match:
        l2_section = match.group(1)
    rows = parse_markdown_table(l2_section)
    low_confidence = sum(1 for row in rows if row.get("confidence", "").lower() == "low")
    return {"exists": True, "l2_rows": rows, "l2_row_count": len(rows), "low_confidence_rows": low_confidence}


def scan_support_doc(path: Path | None, label: str) -> dict[str, Any]:
    if not path or not path.exists():
        return {"exists": False, "label": label, "line_count": 0, "table_rows": 0, "sections": []}
    text = read_text(path)
    sections = re.findall(r"(?m)^##+\s+(.+)$", text)
    return {
        "exists": True,
        "label": label,
        "line_count": text.count("\n") + 1,
        "table_rows": len(parse_markdown_table(text)),
        "sections": sections,
    }


def scan_trace(trace_file: Path) -> dict[str, Any]:
    if not trace_file.exists():
        return {"has_traceability_file": False, "line_count": 0, "possible_links": 0}
    text = read_text(trace_file)
    possible_links = len(re.findall(r"->|→|Scenario|Feature|Table|Entity", text))
    return {"has_traceability_file": True, "line_count": text.count("\n") + 1, "possible_links": possible_links}


def main() -> int:
    parser = argparse.ArgumentParser(description="RAscore static precheck")
    parser.add_argument("--features", required=True)
    parser.add_argument("--dbml", required=True)
    parser.add_argument("--glossary")
    parser.add_argument("--seeds")
    parser.add_argument("--constraints")
    parser.add_argument("--trace")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    features_dir = Path(args.features)
    dbml_dir = Path(args.dbml)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    gherkin = scan_features(features_dir)
    dbml = scan_dbml(dbml_dir)
    trace = scan_trace(Path(args.trace)) if args.trace else {"has_traceability_file": False}
    glossary_path = Path(args.glossary) if args.glossary else None
    seeds_path = Path(args.seeds) if args.seeds else None
    constraints_path = Path(args.constraints) if args.constraints else None
    glossary = scan_glossary(glossary_path)
    trace_l2 = scan_traceability_l2(Path(args.trace)) if args.trace else {"exists": False}
    seeds = scan_support_doc(seeds_path, "seeds")
    constraints = scan_support_doc(constraints_path, "constraints")
    cross_spec = build_cross_spec(gherkin, dbml)
    cross_spec.update(build_glossary_cross_spec(gherkin, dbml, glossary))
    cross_spec["l2_traceability_coverage"] = {
        "l2_row_count": trace_l2.get("l2_row_count", 0),
        "low_confidence_rows": trace_l2.get("low_confidence_rows", 0),
        "scenario_count": gherkin.get("scenario_count", 0),
        "ratio": round(trace_l2.get("l2_row_count", 0) / gherkin.get("scenario_count", 1), 4)
        if gherkin.get("scenario_count")
        else 0,
    }

    result = {
        "inputs": {
            "features": str(features_dir),
            "dbml": str(dbml_dir),
            "glossary": str(glossary_path) if glossary_path else None,
            "seeds": str(seeds_path) if seeds_path else None,
            "constraints": str(constraints_path) if constraints_path else None,
            "trace": args.trace,
        },
        "missing_inputs": {
            "features": not features_dir.exists() or gherkin["feature_count"] == 0,
            "dbml": not dbml_dir.exists() or dbml["file_count"] == 0,
            "glossary": bool(glossary_path and not glossary_path.exists()),
            "seeds": bool(seeds_path and not seeds_path.exists()),
            "constraints": bool(constraints_path and not constraints_path.exists()),
            "trace": bool(args.trace and not Path(args.trace).exists()),
        },
        "gherkin": gherkin,
        "dbml": dbml,
        "glossary": glossary,
        "seeds": seeds,
        "constraints": constraints,
        "cross_spec": cross_spec,
        "traceability_l2": trace_l2,
        "trace": trace,
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    if result["missing_inputs"]["features"] or result["missing_inputs"]["dbml"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
