#!/usr/bin/env python3
"""
dsl-lint.py — RAPTor 四層 DSL 驗證器（L1 YAML / L2 JSON Schema / L3 DSL Lint / L4 Cross-DSL）

SSoT：RAPTor/DSLspec/*v3.3.md、dsl-cross-reference-v33.md、hapdl-canonical-keys.md。
設計：單一實作、多階段呼叫（--levels）。違規一律 ERROR（hard fail），附 fix 修正指引；不做相容轉換。

用法：
  python dsl-lint.py --haapi DIR --hapdl DIR --dbml FILE --haarm FILE --levels all
  python dsl-lint.py --file path/to/x.haapi.yaml --levels 1,2,3
  python dsl-lint.py --haapi DIR --levels 1,2 --format json

exit code：有任何 ERROR → 1；否則 0。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

import yaml

try:
    import jsonschema
    _HAS_JSONSCHEMA = True
except ImportError:  # pragma: no cover
    _HAS_JSONSCHEMA = False


# ═══════════════════════════════════════════════════════════════════════════════
# Finding model + error catalog
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class Finding:
    file: str
    code: str
    severity: str  # ERROR | WARN
    message: str
    fix: str = ""
    loc: str = ""

    def render_text(self) -> str:
        mark = "✗" if self.severity == "ERROR" else "⚠"
        out = [f"{mark} [{self.code}] {self.file}" + (f" ({self.loc})" if self.loc else "")]
        out.append(f"    {self.message}")
        if self.fix:
            for i, line in enumerate(self.fix.splitlines()):
                out.append(f"    fix: {line}" if i == 0 else f"         {line}")
        return "\n".join(out)


# ═══════════════════════════════════════════════════════════════════════════════
# Schema location
# ═══════════════════════════════════════════════════════════════════════════════

def find_schema_dir(explicit: str | None) -> Path | None:
    if explicit:
        p = Path(explicit)
        return p if p.is_dir() else None
    candidates = []
    here = Path(__file__).resolve()
    for base in [Path.cwd(), *here.parents]:
        candidates.append(base / "RAPTor" / "DSLspec" / "schemas")
        candidates.append(base / "DSLspec" / "schemas")
    for c in candidates:
        if c.is_dir():
            return c
    return None


def load_schema(schema_dir: Path | None, name: str) -> dict | None:
    if not schema_dir:
        return None
    p = schema_dir / name
    if not p.is_file():
        return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# L1 — YAML parse
# ═══════════════════════════════════════════════════════════════════════════════

def load_yaml(path: Path, findings: list[Finding]) -> dict | None:
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            findings.append(Finding(
                file=str(path), code="DSL-PARSE-002", severity="ERROR",
                message="檔案頂層不是 mapping（dict）。",
                fix="確認 YAML 頂層為 key: value 結構，而非 list 或 scalar。",
            ))
            return None
        return data
    except yaml.YAMLError as e:
        loc = ""
        if hasattr(e, "problem_mark") and e.problem_mark is not None:
            loc = f"line {e.problem_mark.line + 1}, col {e.problem_mark.column + 1}"
        findings.append(Finding(
            file=str(path), code="DSL-PARSE-001", severity="ERROR",
            message=f"YAML 語法錯誤：{getattr(e, 'problem', str(e))}",
            fix="檢查該行：型別標記如 `string[]` 需加引號；中文括號/冒號裸值需加引號；flow mapping `{` 後需空格。",
            loc=loc,
        ))
        return None


# ═══════════════════════════════════════════════════════════════════════════════
# L2 — JSON Schema (explicit high-value checks + generic jsonschema)
# ═══════════════════════════════════════════════════════════════════════════════

def check_l2_haapi(doc: dict, file: str, schema: dict | None, findings: list[Finding]) -> None:
    access = doc.get("access")

    # HAAPI-SCHEMA-002: top-level bare endpoints
    if "endpoints" in doc:
        findings.append(Finding(
            file=file, code="HAAPI-SCHEMA-002", severity="ERROR",
            message="出現頂層 `endpoints:`，DSLspec 無此結構。",
            fix="刪除頂層 endpoints；端點來自 exposes.standard + exposes.operations（路徑由 base=api 慣例推導）。",
        ))

    if isinstance(access, dict):
        # HAAPI-SCHEMA-004: deprecated access.permissions
        if "permissions" in access:
            findings.append(Finding(
                file=file, code="HAAPI-SCHEMA-004", severity="ERROR",
                message="出現 `access.permissions:`（v3.1 dead-letter，已棄用）。",
                fix="改用 access.endpoints.<op>.required_permissions[].id 雙軌格式。",
            ))
        # HAAPI-SCHEMA-001: endpoints/operations must be dict
        for key in ("endpoints", "operations"):
            val = access.get(key)
            if isinstance(val, list):
                findings.append(Finding(
                    file=file, code="HAAPI-SCHEMA-001", severity="ERROR",
                    message=f"access.{key} 是 array，DSLspec §2.3.1 要求 dict（key=操作名）。",
                    fix=(f"將 access.{key} 改為 dict：\n"
                         "  access:\n"
                         f"    {key}:\n"
                         "      list:                       # key=操作名，非 array\n"
                         "        required_roles: [admin, staff]\n"
                         "        required_permissions:\n"
                         "          - id: <perm_id>\n"
                         "（path/methods 不放 access；端點由 exposes 推導）"),
                ))
            elif isinstance(val, dict):
                # HAAPI-SCHEMA-003: required_permissions items must be {id:...}
                for op_name, op_val in val.items():
                    if not isinstance(op_val, dict):
                        continue
                    rp = op_val.get("required_permissions")
                    if isinstance(rp, list):
                        for item in rp:
                            if not isinstance(item, dict) or "id" not in item:
                                findings.append(Finding(
                                    file=file, code="HAAPI-SCHEMA-003", severity="ERROR",
                                    message=f"access.{key}.{op_name}.required_permissions 含裸字串或缺 id。",
                                    fix="每個 permission 改為 `- id: <perm_id>`。",
                                ))
                                break

    _run_jsonschema(doc, file, schema, findings, "HAAPI")


def check_l2_hapdl(doc: dict, file: str, schema: dict | None, findings: list[Finding]) -> None:
    # HAPDL-SCHEMA-001: meta/pages wrapper
    for bad in ("meta", "pages"):
        if bad in doc:
            findings.append(Finding(
                file=file, code="HAPDL-SCHEMA-001", severity="ERROR",
                message=f"出現頂層 `{bad}:`（多頁打包包裝），違反一檔一頁。",
                fix="拆成多個檔案，每檔頂層為 `page: <kebab-id>`，移除 meta/pages 包裝。",
            ))
    # HAPDL-SCHEMA-002: missing/incorrect page key
    if "page" not in doc:
        if "page_id" in doc:
            findings.append(Finding(
                file=file, code="HAPDL-SCHEMA-002", severity="ERROR",
                message="使用 `page_id`，正式鍵為 `page`。",
                fix="把 `page_id:` 改名為 `page:`。",
            ))
        elif "meta" not in doc and "pages" not in doc:
            findings.append(Finding(
                file=file, code="HAPDL-SCHEMA-002", severity="ERROR",
                message="缺頂層 `page`。",
                fix="頂層加 `page: <kebab-id>`（非 page_id、非 pages[]）。",
            ))
    # legacy security.permissions
    sec = doc.get("security")
    if isinstance(sec, dict) and "permissions" in sec:
        findings.append(Finding(
            file=file, code="HAPDL-LINT-003", severity="ERROR",
            message="出現 `security.permissions:`（v3.1 legacy，已棄用）。",
            fix="改用 security.permission_refs.{action}[].id。",
        ))

    _run_jsonschema(doc, file, schema, findings, "HAPDL")


def _run_jsonschema(doc: dict, file: str, schema: dict | None, findings: list[Finding], prefix: str) -> None:
    """Generic structural validation for anything the explicit checks didn't catch."""
    if not schema or not _HAS_JSONSCHEMA:
        return
    validator = jsonschema.Draft7Validator(schema)
    code = f"{prefix}-SCHEMA-GENERIC"
    seen_paths = set()
    for err in validator.iter_errors(doc):
        # `not` 違規（頂層 endpoints / meta / pages / page_id）已由 explicit 檢查精準涵蓋，
        # 且 jsonschema 會把整份 instance 印進 message，故略過避免噪音。
        if err.validator == "not":
            continue
        path = ".".join(str(p) for p in err.absolute_path) or "<root>"
        raw = err.message
        msg = f"{path}: {raw[:200]}{'…' if len(raw) > 200 else ''}"
        key = (path, raw[:80])
        if key in seen_paths:
            continue
        seen_paths.add(key)
        findings.append(Finding(
            file=file, code=code, severity="ERROR",
            message=msg,
            fix="依 DSLspec schema 修正該欄位的型別/必填/列舉值。",
            loc=path,
        ))


# ═══════════════════════════════════════════════════════════════════════════════
# L3 — DSL single-file semantic lint  (Phase 2)
# ═══════════════════════════════════════════════════════════════════════════════

_KEBAB = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
_STD_OPS = {"list", "create", "read", "update", "patch", "delete", "exists"}


def check_l3_haapi(doc: dict, file: str, findings: list[Finding]) -> None:
    api = doc.get("api", "")
    if api and not _KEBAB.match(str(api)):
        findings.append(Finding(
            file=file, code="HAAPI-LINT-001", severity="ERROR",
            message=f"api `{api}` 不是 kebab-case。",
            fix="改為小寫 kebab-case，例 order-item。",
        ))

    exposes = doc.get("exposes", {}) or {}
    access = doc.get("access", {}) or {}
    std = exposes.get("standard", [])
    if isinstance(std, str):
        std = {"crud": ["create", "read", "update", "delete"],
               "all": list(_STD_OPS)}.get(std, [])
    exp_ops = exposes.get("operations", []) or []
    exp_op_names = set()
    for o in exp_ops:
        if isinstance(o, str):
            exp_op_names.add(o)
        elif isinstance(o, dict) and "name" in o:
            exp_op_names.add(o["name"])

    ep = access.get("endpoints", {}) or {}
    ao = access.get("operations", {}) or {}
    ep_keys = set(ep.keys()) if isinstance(ep, dict) else set()
    ao_keys = set(ao.keys()) if isinstance(ao, dict) else set()

    # HAAPI-LINT-002: access keys must correspond to exposes
    for k in ep_keys:
        if k not in set(std) and k not in _STD_OPS:
            findings.append(Finding(
                file=file, code="HAAPI-LINT-002", severity="ERROR",
                message=f"access.endpoints.{k} 不在 exposes.standard 也非標準操作名。",
                fix=f"確認 `{k}` 是 exposes.standard 列出的操作；自訂操作請放 access.operations。",
            ))
    for k in ao_keys:
        if k not in exp_op_names:
            findings.append(Finding(
                file=file, code="HAAPI-LINT-002", severity="ERROR",
                message=f"access.operations.{k} 沒有對應的 exposes.operations 宣告。",
                fix=f"在 exposes.operations 加入 `{k}`（字串或 {{name: {k}, method, path}}）。",
            ))

    # HAAPI-LINT-003: exposed op missing access entry → WARN
    for op in std:
        if op not in ep_keys:
            findings.append(Finding(
                file=file, code="HAAPI-LINT-003", severity="WARN",
                message=f"exposes.standard 的 `{op}` 在 access.endpoints 無授權 entry。",
                fix=f"在 access.endpoints 補 `{op}:` 授權；預設視為需登入、無特定 permission。",
            ))
    for op in exp_op_names:
        if op not in ao_keys:
            findings.append(Finding(
                file=file, code="HAAPI-LINT-003", severity="WARN",
                message=f"exposes.operations 的 `{op}` 在 access.operations 無授權 entry。",
                fix=f"在 access.operations 補 `{op}:` 授權。",
            ))

    # HAAPI-LINT-005: ext.<service> must be declared in integrations
    declared = set((doc.get("integrations") or {}).keys()) if isinstance(doc.get("integrations"), dict) else set()
    for svc in _collect_ext_services(doc):
        if svc not in declared:
            findings.append(Finding(
                file=file, code="HAAPI-LINT-005", severity="ERROR",
                message=f"使用 ext.{svc}.* 但 `{svc}` 未在 integrations 宣告。",
                fix=f"在頂層 integrations 宣告 `{svc}` 及其 capabilities。",
            ))


def _collect_ext_services(node) -> set[str]:
    found: set[str] = set()
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "action" and isinstance(v, str) and v.startswith("ext."):
                parts = v.split(".")
                if len(parts) >= 2:
                    found.add(parts[1])
            found |= _collect_ext_services(v)
    elif isinstance(node, list):
        for item in node:
            found |= _collect_ext_services(item)
    return found


def check_l3_hapdl(doc: dict, file: str, findings: list[Finding]) -> None:
    page = doc.get("page", "")
    if page and not _KEBAB.match(str(page)):
        findings.append(Finding(
            file=file, code="HAPDL-LINT-001", severity="ERROR",
            message=f"page `{page}` 不是 kebab-case。",
            fix="改為小寫 kebab-case，例 order-list。",
        ))
    ptype = doc.get("type", "")
    if ptype and ptype not in {"list", "form", "detail", "dashboard", "wizard"}:
        findings.append(Finding(
            file=file, code="HAPDL-LINT-002", severity="ERROR",
            message=f"type `{ptype}` 不是合法頁面類型。",
            fix="type ∈ list|form|detail|dashboard|wizard。",
        ))


# ═══════════════════════════════════════════════════════════════════════════════
# L4 — Cross-DSL reference  (Phase 3)
# ═══════════════════════════════════════════════════════════════════════════════


_IMPLEMENTATION_LITERAL = re.compile(
    r"(#[A-Za-z0-9_-]+|\.[A-Za-z0-9_-]+|data-testid|https?://|/api/|\bGET\b|\bPOST\b|\bPUT\b|\bPATCH\b|\bDELETE\b)"
)


def check_l3_habdd_text(text: str, file: str, findings: list[Finding]) -> None:
    """Lint high-level haBDD feature text."""

    path = Path(file)
    stem = path.name.removesuffix(".ha.feature").removesuffix(".feature")
    if stem and not _KEBAB.match(stem):
        findings.append(Finding(
            file=file, code="HABDD-LINT-001", severity="ERROR",
            message=f"feature file `{path.name}` should use kebab-case",
            fix="Rename the feature file to kebab-case, for example `case-review.ha.feature`.",
        ))

    if "# source:" not in text:
        findings.append(Finding(
            file=file, code="HABDD-LINT-002", severity="ERROR",
            message="missing `# source:` evidence comment",
            fix="Add `# source: <discovery/story/decision ref>` before Feature.",
        ))

    if "# feature-id:" not in text:
        findings.append(Finding(
            file=file, code="HABDD-LINT-003", severity="WARN",
            message="missing `# feature-id:` comment",
            fix="Add a stable feature id, for example `# feature-id: F-001`.",
        ))

    if not re.search(r"(?m)^Feature:\s+\S", text):
        findings.append(Finding(
            file=file, code="HABDD-LINT-004", severity="ERROR",
            message="missing Feature heading",
            fix="Add `Feature: <business capability>`.",
        ))

    scenario_blocks = re.split(r"(?m)^\s*Scenario(?: Outline)?:", text)[1:]
    for index, block in enumerate(scenario_blocks, start=1):
        if not re.search(r"(?m)^\s*When\s+", block):
            findings.append(Finding(
                file=file, code="HABDD-LINT-005", severity="ERROR",
                message=f"Scenario #{index} has no When step",
                fix="Each scenario should contain one business action in a When step.",
            ))

    for line_no, line in enumerate(text.splitlines(), start=1):
        if line.lstrip().startswith("#"):
            continue
        if _IMPLEMENTATION_LITERAL.search(line):
            findings.append(Finding(
                file=file, code="HABDD-LINT-006", severity="ERROR",
                message="haBDD contains implementation literal",
                fix="Move selectors, API URLs, HTTP methods, and test ids to generated isaBDD/e2e artifacts.",
                loc=f"line {line_no}",
            ))


def parse_dbml_tables(dbml_path: Path | None) -> set[str]:
    tables: set[str] = set()
    if not dbml_path or not dbml_path.is_file():
        return tables
    text = dbml_path.read_text(encoding="utf-8")
    for m in re.finditer(r'(?mi)^\s*Table\s+"?([A-Za-z_][A-Za-z0-9_]*)"?', text):
        tables.add(m.group(1))
    return tables


def load_haarm_ids(haarm_path: Path | None) -> tuple[set[str], set[str], set[str]]:
    roles: set[str] = set()
    perms: set[str] = set()
    constraints: set[str] = set()
    if not haarm_path or not haarm_path.is_file():
        return roles, perms, constraints
    try:
        data = yaml.safe_load(haarm_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError:
        return roles, perms, constraints
    for r in data.get("roles", []) or []:
        if isinstance(r, dict) and "id" in r:
            roles.add(r["id"])
    for p in data.get("permissions", []) or []:
        if isinstance(p, dict) and "id" in p:
            perms.add(p["id"])
    for c in data.get("constraints", []) or []:
        if isinstance(c, dict) and "id" in c:
            constraints.add(c["id"])
    return roles, perms, constraints


def check_l4(haapis: list[tuple[str, dict]], hapdls: list[tuple[str, dict]],
             tables: set[str], roles: set[str], perms: set[str], constraints: set[str],
             findings: list[Finding]) -> None:
    haapi_ids = {d.get("api") for _, d in haapis if d.get("api")}

    for file, doc in haapis:
        ent = doc.get("entity")
        if ent and tables and ent not in tables:
            findings.append(Finding(
                file=file, code="XREF-001", severity="ERROR",
                message=f"entity `{ent}` 在 DBML 找不到對應 Table（case-sensitive）。",
                fix="entity 必須完全等於 DBML Table Name（含大小寫）。",
            ))
        access = doc.get("access", {}) or {}
        for sect in ("endpoints", "operations"):
            block = access.get(sect, {})
            if not isinstance(block, dict):
                continue
            for op, cfg in block.items():
                if not isinstance(cfg, dict):
                    continue
                for role in cfg.get("required_roles", []) or []:
                    if roles and role not in roles:
                        findings.append(Finding(
                            file=file, code="XREF-002" if sect == "endpoints" else "XREF-004",
                            severity="ERROR",
                            message=f"access.{sect}.{op}.required_roles 的 `{role}` 不在 haARM roles。",
                            fix="修正拼字或經 rapt-reconcile 在 haARM backfill 該 role。",
                        ))
                for p in cfg.get("required_permissions", []) or []:
                    pid = p.get("id") if isinstance(p, dict) else p
                    if perms and pid not in perms:
                        findings.append(Finding(
                            file=file, code="XREF-003", severity="ERROR",
                            message=f"access.{sect}.{op}.required_permissions `{pid}` 不在 haARM permissions。",
                            fix="修正拼字或經 rapt-reconcile backfill 該 permission。",
                        ))
                for cond in cfg.get("conditions", []) or []:
                    cid = cond.get("haarm_constraint") if isinstance(cond, dict) else None
                    if cid and constraints and cid not in constraints:
                        findings.append(Finding(
                            file=file, code="XREF-005", severity="WARN",
                            message=f"conditions.haarm_constraint `{cid}` 不在 haARM constraints。",
                            fix="補 haARM constraint 定義或修正 id。",
                        ))

    for file, doc in hapdls:
        ent = doc.get("entity")
        if ent and tables and ent not in tables:
            findings.append(Finding(
                file=file, code="XREF-007", severity="ERROR",
                message=f"entity `{ent}` 在 DBML 找不到對應 Table（case-sensitive）。",
                fix="entity 必須完全等於 DBML Table Name。",
            ))
        api = doc.get("api")
        if api and haapi_ids and api not in haapi_ids:
            findings.append(Finding(
                file=file, code="XREF-006", severity="ERROR",
                message=f"api `{api}` 找不到對應的 haAPI（頂層 api id）。",
                fix="確認對應 {api}.haapi.yaml 存在且 api id 一致。",
            ))
        for role in (doc.get("auth", {}) or {}).get("roles", []) or []:
            if roles and role not in roles:
                findings.append(Finding(
                    file=file, code="XREF-008", severity="ERROR",
                    message=f"auth.roles 的 `{role}` 不在 haARM roles。",
                    fix="修正 role id。",
                ))
        pref = (doc.get("security", {}) or {}).get("permission_refs", {}) or {}
        if isinstance(pref, dict):
            for action, items in pref.items():
                for item in items or []:
                    pid = item.get("id") if isinstance(item, dict) else item
                    if perms and pid not in perms:
                        findings.append(Finding(
                            file=file, code="XREF-009", severity="ERROR",
                            message=f"security.permission_refs.{action} `{pid}` 不在 haARM permissions。",
                            fix="修正 permission id 或 backfill。",
                        ))


# ═══════════════════════════════════════════════════════════════════════════════
# Drivers
# ═══════════════════════════════════════════════════════════════════════════════

def collect_files(arg: str | None, suffix: str) -> list[Path]:
    if not arg:
        return []
    p = Path(arg)
    if p.is_dir():
        return sorted(p.glob(f"*{suffix}"))
    if p.is_file():
        return [p]
    return []


def run(args) -> int:
    levels = {"1", "2", "3", "4"} if args.levels == "all" else set(args.levels.split(","))
    schema_dir = find_schema_dir(args.schema_dir)
    haapi_schema = load_schema(schema_dir, "haapi-v3.3.schema.json")
    hapdl_schema = load_schema(schema_dir, "hapdl-v3.3.schema.json")

    findings: list[Finding] = []
    haapi_docs: list[tuple[str, dict]] = []
    hapdl_docs: list[tuple[str, dict]] = []

    # single-file mode: route by suffix; else use --haapi / --hapdl dirs
    if args.file:
        fp = Path(args.file)
        haapi_files = [fp] if fp.name.endswith(".haapi.yaml") else []
        hapdl_files = [fp] if fp.name.endswith(".hapdl.yaml") else []
        habdd_files = [fp] if fp.name.endswith((".ha.feature", ".feature")) else []
    else:
        haapi_files = collect_files(args.haapi, ".haapi.yaml")
        hapdl_files = collect_files(args.hapdl, ".hapdl.yaml")
        habdd_files = sorted(set(collect_files(args.habdd, ".ha.feature") + collect_files(args.habdd, ".feature")))

    for path in haapi_files:
        doc = load_yaml(path, findings)  # L1 always runs (parse needed for any level)
        if doc is None:
            continue
        haapi_docs.append((str(path), doc))
        if "2" in levels:
            check_l2_haapi(doc, str(path), haapi_schema, findings)
        if "3" in levels:
            check_l3_haapi(doc, str(path), findings)

    for path in hapdl_files:
        doc = load_yaml(path, findings)
        if doc is None:
            continue
        hapdl_docs.append((str(path), doc))
        if "2" in levels:
            check_l2_hapdl(doc, str(path), hapdl_schema, findings)
        if "3" in levels:
            check_l3_hapdl(doc, str(path), findings)

    for path in habdd_files:
        try:
            feature_text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            findings.append(Finding(
                file=str(path), code="HABDD-PARSE-001", severity="ERROR",
                message=f"cannot read haBDD feature: {exc}",
                fix="Ensure the feature file is UTF-8 text.",
            ))
            continue
        if "3" in levels:
            check_l3_habdd_text(feature_text, str(path), findings)

    if "4" in levels:
        tables = parse_dbml_tables(Path(args.dbml) if args.dbml else None)
        roles, perms, constraints = load_haarm_ids(Path(args.haarm) if args.haarm else None)
        check_l4(haapi_docs, hapdl_docs, tables, roles, perms, constraints, findings)

    _report(findings, args.format)
    return 1 if any(f.severity == "ERROR" for f in findings) else 0


def _report(findings: list[Finding], fmt: str) -> None:
    if fmt == "json":
        print(json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2))
        return
    errors = [f for f in findings if f.severity == "ERROR"]
    warns = [f for f in findings if f.severity == "WARN"]
    for f in findings:
        print(f.render_text())
        print()
    print(f"── dsl-lint：{len(errors)} ERROR, {len(warns)} WARN ──")
    if not findings:
        print("✓ 全部通過")


def main() -> int:
    # Windows 主控台預設 cp950 無法輸出 ✗/⚠/中文；強制 stdout/stderr 為 UTF-8
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (ValueError, OSError):
                pass
    ap = argparse.ArgumentParser(description="RAPTor 四層 DSL 驗證器")
    ap.add_argument("--haapi", help="haAPI 目錄或檔案")
    ap.add_argument("--habdd", help="haBDD feature directory")
    ap.add_argument("--hapdl", help="haPDL 目錄或檔案")
    ap.add_argument("--dbml", help="DBML 檔（L4 用）")
    ap.add_argument("--haarm", help="haARM 檔（L4 用）")
    ap.add_argument("--file", help="單一檔案模式（生成當下用）")
    ap.add_argument("--levels", default="all", help="1,2,3,4 或 all")
    ap.add_argument("--schema-dir", help="schema 目錄（預設自動尋找）")
    ap.add_argument("--format", default="text", choices=["text", "json"])
    args = ap.parse_args()
    return run(args)


if __name__ == "__main__":
    sys.exit(main())
