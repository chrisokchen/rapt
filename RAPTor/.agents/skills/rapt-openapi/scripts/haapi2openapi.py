#!/usr/bin/env python3
"""
haapi2openapi.py
================
Converts haAPI + haARM + annotated DBML into OpenAPI 3.0.3 YAML.

This is the reference implementation for the rapt-openapi skill.
It reads SSoT artifacts and generates a preview-only OpenAPI spec.

Usage:
    python haapi2openapi.py \
        --haapi  docs/05-backend-intent/ \
        --haarm  docs/03-access-control/mjib-eis.haarm.yaml \
        --dbml   docs/02-data-model/schema.dbml \
        --output docs/06-openapi/openapi.yaml

    # With optional project info (auto-read from .raptor/arguments.yml if present):
    python haapi2openapi.py \
        --haapi  docs/05-backend-intent/ \
        --haarm  docs/03-access-control/mjib-eis.haarm.yaml \
        --dbml   docs/02-data-model/schema.dbml \
        --output docs/06-openapi/openapi.yaml \
        --title  "My API" \
        --description "My API description"

Origin: Projects/haapi2openapi.py (mjib prototype, 2026-06-04)
"""

import argparse
import re
import sys
from pathlib import Path

import yaml


# ── 0. arguments.yml loader ─────────────────────────────────────────────────

def load_arguments_yml(cwd: Path) -> dict | None:
    """Try to load .raptor/arguments.yml from CWD. Returns None if not found."""
    args_path = cwd / ".raptor" / "arguments.yml"
    if args_path.is_file():
        with open(args_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    return None


# ── 1. DBML Parser ───────────────────────────────────────────────────────────

def dbml_type_to_schema(raw_type: str) -> dict:
    """Convert a DBML column type string to an OpenAPI schema fragment."""
    raw = raw_type.strip().lower()

    if raw == "nvarchar(max)":
        return {"type": "string"}

    m = re.match(r"nvarchar\((\d+)\)", raw)
    if m:
        return {"type": "string", "maxLength": int(m.group(1))}

    m = re.match(r"nchar\((\d+)\)", raw)
    if m:
        return {"type": "string", "maxLength": int(m.group(1))}

    if raw in ("int",):
        return {"type": "integer", "format": "int32"}

    if raw == "bigint":
        return {"type": "integer", "format": "int64"}

    if raw == "bit":
        return {"type": "boolean"}

    if re.match(r"datetime2\(\d+\)", raw):
        return {"type": "string", "format": "date-time"}

    # Fallback
    return {"type": "string"}


def parse_dbml(dbml_text: str) -> dict:
    """
    Lightweight DBML parser.
    Returns: { "TableName": { "fields": [...], "note": str } }
    Each field: { name, schema, required, pk, sensitive, ref_code, label }
    """
    tables = {}
    # Find all Table blocks
    table_pattern = re.compile(
        r'Table\s+(\w+)\s*\{([^}]+)\}', re.DOTALL
    )
    # Field line pattern: name  type  [attrs]
    field_pattern = re.compile(
        r'^\s*(\w+)\s+([\w\(\),]+)\s*(?:\[([^\]]*)\])?\s*$'
    )
    note_pattern = re.compile(r"Note:\s*'([^']+)'")

    for table_match in table_pattern.finditer(dbml_text):
        table_name = table_match.group(1)
        body = table_match.group(2)

        note_m = note_pattern.search(body)
        note = note_m.group(1) if note_m else ""

        fields = []
        for line in body.splitlines():
            line = line.strip()
            # Skip comments, Note lines, empty lines
            if not line or line.startswith("//") or line.startswith("Note:"):
                continue
            fm = field_pattern.match(line)
            if not fm:
                continue

            fname = fm.group(1)
            ftype = fm.group(2)
            attrs_raw = fm.group(3) or ""

            # Parse attributes
            is_pk = "pk" in attrs_raw
            is_required = "not null" in attrs_raw or is_pk
            is_sensitive = "sensitive: true" in attrs_raw

            # Extract label
            label_m = re.search(r"label:\s*'([^']+)'", attrs_raw)
            label = label_m.group(1) if label_m else fname

            # Extract ref_code
            ref_code_m = re.search(r"ref_code:\s*'?(\w+)'?", attrs_raw)
            ref_code = ref_code_m.group(1) if ref_code_m else None

            # Build schema
            schema = dbml_type_to_schema(ftype)
            if ref_code:
                schema["x-ref-code"] = ref_code

            field_info = {
                "name": fname,
                "schema": schema,
                "required": is_required,
                "pk": is_pk,
                "sensitive": is_sensitive,
                "label": label,
                "ref_code": ref_code,
            }
            if is_sensitive:
                field_info["schema"]["x-sensitive"] = True

            fields.append(field_info)

        tables[table_name] = {"fields": fields, "note": note}

    return tables


# ── 2. haARM Loader ──────────────────────────────────────────────────────────

def load_haarm(path: Path) -> dict:
    """Load haARM YAML. Returns the parsed dict."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── 3. haAPI Loader ──────────────────────────────────────────────────────────

def load_haapi_dir(directory: Path) -> list:
    """Load all *.haapi.yaml files from a directory."""
    apis = []
    for p in sorted(directory.glob("*.haapi.yaml")):
        with open(p, encoding="utf-8") as f:
            data = yaml.safe_load(f)
            data["_file"] = str(p)
            apis.append(data)
    return apis


# ── 4. Operation Mapper ───────────────────────────────────────────────────────

# Verb → HTTP method heuristic
VERB_METHOD_MAP = {
    "list":    "get",
    "get":     "get",
    "create":  "post",
    "update":  "put",
    "delete":  "delete",
    "submit":  "post",
    "approve": "post",
    "reject":  "post",
    "confirm": "post",
    "close":   "post",
    "execute": "post",
    "upload":  "post",
    "download":"get",
    "manage":  "get",    # ambiguous; will expand separately
    "request": "post",
    "extract": "post",
    "verify":  "put",
    "adjust":  "put",
}


def infer_method(operation_id: str) -> str:
    """Infer HTTP method from operationId verb prefix."""
    lower = operation_id.lower()
    for verb, method in VERB_METHOD_MAP.items():
        if lower.startswith(verb):
            return method
    return "get"


def is_collection_op(operation_id: str) -> bool:
    """True if operationId starts with 'list'."""
    return operation_id.lower().startswith("list")


def path_has_id(path: str) -> bool:
    return "{" in path and "}" in path


def _build_segment_table_map(dbml_tables: dict) -> dict:
    """
    Dynamically build a mapping from pluralized URL path segments to DBML table names.
    e.g. 'applications' -> 'Application', 'users' -> 'UserAccount'
    """
    segment_map = {}
    for table_name in dbml_tables:
        # Simple pluralization heuristic: lowercase + 's'
        lower = table_name[0].lower() + table_name[1:]
        # CamelCase to kebab-case segments
        kebab = re.sub(r'([A-Z])', r'-\1', table_name).strip('-').lower()
        # Try multiple plural forms
        candidates = [
            lower + "s",
            lower + "es",
            kebab + "s",
            kebab + "es",
            kebab.replace("-", "") + "s",
        ]
        for candidate in candidates:
            if candidate not in segment_map:
                segment_map[candidate] = table_name
        # Also add exact lowercase
        segment_map[lower] = table_name
    return segment_map


# 標準操作 → (HTTP method, 是否帶 {id})。路徑 base = api（不做複數轉換，見 haapi-format-anchor 路徑推導規約）。
STANDARD_OPS = {
    "list":   ("get",    False),
    "create": ("post",   False),
    "read":   ("get",    True),
    "update": ("put",    True),
    "patch":  ("patch",  True),
    "delete": ("delete", True),
    "exists": ("head",   True),
}


def _entity_kebab(name: str) -> str:
    """CamelCase → kebab-case，不加複數。CustomerProfile → customer-profile。"""
    s = re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()
    return s.strip("-")


def _pascal(name: str) -> str:
    return "".join(part.capitalize() for part in re.split(r"[-_\s]+", name) if part)


def _camel(name: str) -> str:
    p = _pascal(name)
    return p[:1].lower() + p[1:] if p else name


def _assert_haapi_format(haapi: dict) -> None:
    """D3：偵測舊/自創格式直接報錯擋下，不做相容轉換。"""
    file = haapi.get("_file", haapi.get("api", "<haapi>"))
    if isinstance(haapi.get("endpoints"), list) or "endpoints" in haapi:
        sys.exit(
            f"✗ [HAAPI-SCHEMA-002] {file}\n"
            f"    出現頂層 `endpoints:`，DSLspec 無此結構。\n"
            f"    fix: 刪除頂層 endpoints；端點來自 exposes.standard + exposes.operations\n"
            f"         （路徑由 base=api 慣例推導）。先跑 dsl-lint.py 修正後再轉換。"
        )
    access = haapi.get("access", {}) or {}
    for key in ("endpoints", "operations"):
        if isinstance(access.get(key), list):
            sys.exit(
                f"✗ [HAAPI-SCHEMA-001] {file}\n"
                f"    access.{key} 是 array，DSLspec §2.3.1 要求 dict（key=操作名）。\n"
                f"    fix: 改為 dict；path/methods 移到 exposes。先跑 dsl-lint.py 修正後再轉換。"
            )
    if "permissions" in access:
        sys.exit(
            f"✗ [HAAPI-SCHEMA-004] {file}\n"
            f"    出現 deprecated `access.permissions:`。\n"
            f"    fix: 改用 access.endpoints.<op>.required_permissions[].id。"
        )


def _perm_ids(raw) -> list:
    """required_permissions 一律讀 {id: ...}；容忍裸字串但正式格式為 dict。"""
    out = []
    for p in raw or []:
        if isinstance(p, dict) and "id" in p:
            out.append(p["id"])
        elif isinstance(p, str):
            out.append(p)
    return out


def build_path_items(haapi: dict, haarm: dict, dbml_tables: dict, segment_table_map: dict) -> dict:
    """
    Given one haAPI module, build an OpenAPI `paths` dict fragment — exposes-driven。
    路由來源：exposes.standard（慣例展開）+ exposes.operations（顯式 method/path）；
    授權來源：access.endpoints.<op> / access.operations.<op>（dict）。
    """
    _assert_haapi_format(haapi)

    api_name = haapi.get("api", "unknown")
    entity = haapi.get("entity", "")
    base = (api_name if api_name and api_name != "unknown" else _entity_kebab(entity)).strip("/")

    access = haapi.get("access", {}) or {}
    access_endpoints = access.get("endpoints", {}) or {}
    access_operations = access.get("operations", {}) or {}

    exposes = haapi.get("exposes", {}) or {}
    standard = exposes.get("standard", [])
    if isinstance(standard, str):
        standard = {"crud": ["create", "read", "update", "delete"],
                    "all": list(STANDARD_OPS)}.get(standard, [])
    exp_operations = exposes.get("operations", []) or []

    list_cfg = exposes.get("list", {}) or {}
    filters = [f.get("field") if isinstance(f, dict) else f for f in list_cfg.get("filters", [])]
    pg = list_cfg.get("pagination", {})
    pagination = pg.get("style", "offset") if isinstance(pg, dict) else (pg or "offset")

    paths: dict = {}

    def emit(path: str, method: str, op_id: str, roles: list, perms: list,
             description: str, is_custom: bool) -> None:
        paths.setdefault(path, {})
        has_id = path_has_id(path)

        parameters = []
        if has_id:
            for p_name in re.findall(r"\{([^}]+)\}", path):
                parameters.append({
                    "name": p_name, "in": "path",
                    "required": True, "schema": {"type": "string"},
                })
        if method == "get" and not has_id and not is_custom:
            for f in filters:
                parameters.append({
                    "name": f, "in": "query", "required": False,
                    "schema": {"type": "string"},
                })
            if pagination == "offset":
                parameters.append({"$ref": "#/components/parameters/OffsetParam"})
                parameters.append({"$ref": "#/components/parameters/LimitParam"})

        request_body = None
        if method in ("post", "put", "patch"):
            schema_name = _infer_entity_schema(path, entity, dbml_tables, segment_table_map)
            if schema_name:
                request_body = {
                    "required": True,
                    "content": {"application/json": {
                        "schema": {"$ref": f"#/components/schemas/{schema_name}Request"}}},
                }

        resp_schema = _build_response_schema(method, path, op_id, entity, dbml_tables, segment_table_map)

        operation = {
            "operationId": op_id,
            "summary": _make_summary(op_id, haapi.get("title", ""), description),
            "tags": [haapi.get("title", api_name)],
            "security": [{"bearerAuth": []}],
            "x-required-roles": roles,
            "x-required-permissions": perms,
        }
        if description and is_custom:
            operation["description"] = description
        if parameters:
            operation["parameters"] = parameters
        if request_body:
            operation["requestBody"] = request_body

        operation["responses"] = {
            "200": {"description": "成功", "content": {"application/json": {"schema": resp_schema}}},
            "400": {"description": "請求參數錯誤"},
            "401": {"description": "未授權"},
            "403": {"description": "權限不足"},
            "404": {"description": "資源不存在"},
            "500": {"description": "伺服器錯誤"},
        }
        if method == "post" and not has_id and not is_custom:
            operation["responses"]["201"] = operation["responses"].pop("200")
            operation["responses"]["201"]["description"] = "建立成功"

        paths[path][method] = operation

    # ── 標準 CRUD：base=api，不做複數轉換 ──
    for op in standard:
        if op not in STANDARD_OPS:
            continue
        method, has_id = STANDARD_OPS[op]
        path = f"/{base}/{{id}}" if has_id else f"/{base}"
        auth = access_endpoints.get(op, {}) if isinstance(access_endpoints, dict) else {}
        emit(
            path, method,
            op_id=f"{op}{_pascal(entity or base)}",
            roles=auth.get("required_roles", []) if isinstance(auth, dict) else [],
            perms=_perm_ids(auth.get("required_permissions") if isinstance(auth, dict) else []),
            description=haapi.get("description", ""),
            is_custom=False,
        )

    # ── 自訂業務操作：exposes.operations 帶 method/path ──
    for o in exp_operations:
        if isinstance(o, str):
            name, method, rel = o, infer_method(o), f"/{{id}}/{_entity_kebab(o).replace('_', '-')}"
            desc = ""
        elif isinstance(o, dict) and "name" in o:
            name = o["name"]
            method = (o.get("method") or "post").lower()
            rel = o.get("path") or f"/{{id}}/{_entity_kebab(name).replace('_', '-')}"
            desc = o.get("description", "")
        else:
            continue
        rel = rel if rel.startswith("/") else f"/{rel}"
        path = f"/{base}{rel}"
        auth = access_operations.get(name, {}) if isinstance(access_operations, dict) else {}
        emit(
            path, method,
            op_id=_camel(f"{api_name}_{name}"),
            roles=auth.get("required_roles", []) if isinstance(auth, dict) else [],
            perms=_perm_ids(auth.get("required_permissions") if isinstance(auth, dict) else []),
            description=desc,
            is_custom=True,
        )

    return paths


def _extract_id_param(path: str) -> str:
    """Extract the first path parameter name from a path string."""
    m = re.search(r"\{([^}]+)\}", path)
    return m.group(1) if m else "id"


def _find_operation_id(path, method, api_name, entity, op_meta, custom_op_names):
    """
    Heuristic: match (path, method) → operation_id.

    Strategy:
    1. If path ends with a known custom_op verb, check custom_op_names.
    2. Otherwise, use list/get/create/update/delete prefix + entity name.
    """
    # Check if path ends with a verb segment (custom action)
    last_segment = path.rstrip("/").split("/")[-1]
    if last_segment and not last_segment.startswith("{"):
        # e.g. /applications/{id}/submit → "submit"
        # Match to custom op names that contain the segment
        for op_name in custom_op_names:
            if last_segment.lower() in op_name.lower():
                return op_name

    # Standard CRUD heuristic
    has_id = path_has_id(path)
    if method == "get":
        if has_id:
            candidate = f"get{entity}"
        else:
            candidate = f"list{entity}s"
    elif method == "post":
        candidate = f"create{entity}"
    elif method == "put":
        candidate = f"update{entity}"
    elif method == "delete":
        candidate = f"delete{entity}"
    else:
        candidate = f"{method}{entity}"

    # Try direct match first
    if candidate in op_meta:
        return candidate

    # Try fuzzy match: find op_id that starts with same verb
    verb_from_method = {
        "get": ["get", "list", "download"],
        "post": ["create", "submit", "approve", "reject", "confirm", "close",
                 "execute", "upload", "request", "extract", "manage"],
        "put": ["update", "verify", "adjust", "manage"],
        "delete": ["delete", "manage"],
    }.get(method, [])

    # Narrow by path: if path contains entity-like name
    path_parts = [p for p in path.split("/") if p and not p.startswith("{")]
    path_hint = path_parts[-1] if path_parts else ""

    for op_id in op_meta:
        op_lower = op_id.lower()
        for verb in verb_from_method:
            if op_lower.startswith(verb):
                # Check if op_id relates to current path hint
                if path_hint.lower().rstrip("s") in op_lower or \
                   op_lower in path_hint.lower() or \
                   len(op_meta) == 1:
                    return op_id

    # Last resort: return first matching verb op
    for op_id in op_meta:
        op_lower = op_id.lower()
        for verb in verb_from_method:
            if op_lower.startswith(verb):
                return op_id

    return candidate  # may not exist in op_meta, that's OK


def _infer_entity_schema(path: str, entity: str, dbml_tables: dict, segment_table_map: dict) -> str | None:
    """Infer the primary entity schema name from a path."""
    path_parts = [p for p in path.split("/") if p and not p.startswith("{")]
    if not path_parts:
        return entity

    # Use dynamic segment map built from DBML table names
    for segment in reversed(path_parts):
        if segment in segment_table_map:
            table_name = segment_table_map[segment]
            if table_name in dbml_tables:
                return table_name

    return entity if entity in dbml_tables else None


def _build_response_schema(method, path, op_id, entity, dbml_tables, segment_table_map):
    """Build the response schema for an operation."""
    schema_name = _infer_entity_schema(path, entity, dbml_tables, segment_table_map)
    op_lower = (op_id or "").lower()

    if method == "delete":
        return {
            "type": "object",
            "properties": {
                "message": {"type": "string", "example": "刪除成功"},
            },
        }

    if op_lower.startswith("list"):
        if schema_name:
            return {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "array",
                        "items": {"$ref": f"#/components/schemas/{schema_name}"},
                    },
                    "total": {"type": "integer"},
                    "offset": {"type": "integer"},
                    "limit": {"type": "integer"},
                },
            }
        return {"type": "object"}

    if op_lower.startswith("download"):
        return {"type": "string", "format": "binary"}

    if schema_name:
        return {"$ref": f"#/components/schemas/{schema_name}"}

    return {
        "type": "object",
        "properties": {
            "message": {"type": "string"},
        },
    }


def _make_summary(op_id, api_title, description):
    """Generate a human-readable summary for an operation."""
    if description:
        return description
    if not op_id:
        return api_title

    # Convert camelCase → human readable
    s = re.sub(r"([A-Z])", r" \1", op_id).strip()
    return s


# ── 5. Schema Builder ─────────────────────────────────────────────────────────

def build_schemas(dbml_tables: dict) -> dict:
    """
    Convert DBML tables into OpenAPI components/schemas.
    Each table generates two schemas:
      - <Name>         : full entity (response)
      - <Name>Request  : writable fields only (request body)
    """
    schemas = {}

    for table_name, table in dbml_tables.items():
        fields = table["fields"]
        note = table.get("note", "")

        properties = {}
        required_fields = []
        request_properties = {}
        request_required = []

        for f in fields:
            prop = dict(f["schema"])
            prop["description"] = f["label"]

            properties[f["name"]] = prop

            # For Request schema: exclude PK and system-generated fields
            system_fields = {"createdAt", "updatedAt", "createdBy", "updatedBy",
                             "uploadedAt", "uploadedBy", "actionAt", "syncedAt",
                             "processedAt", "receivedAt", "dispatchedAt",
                             "submittedAt", "closedAt", "completedAt", "startedAt",
                             "confirmedAt", "approvedAt", "assignedAt", "verifiedAt"}
            if not f["pk"] and f["name"] not in system_fields:
                request_properties[f["name"]] = prop
                if f["required"] and f["name"] not in system_fields:
                    request_required.append(f["name"])

            if f["required"]:
                required_fields.append(f["name"])

        # Full entity schema
        entity_schema = {
            "type": "object",
            "description": note,
            "properties": properties,
        }
        if required_fields:
            entity_schema["required"] = required_fields

        # Request schema (write-only fields)
        request_schema = {
            "type": "object",
            "description": f"{note} 請求體",
            "properties": request_properties,
        }
        if request_required:
            request_schema["required"] = request_required

        schemas[table_name] = entity_schema
        schemas[f"{table_name}Request"] = request_schema

    return schemas


# ── 6. OpenAPI Assembler ──────────────────────────────────────────────────────

def assemble_openapi(haapis: list, haarm: dict, dbml_tables: dict,
                     title: str = "API Documentation",
                     description: str = "") -> dict:
    """Assemble the full OpenAPI 3.0.3 document."""

    segment_table_map = _build_segment_table_map(dbml_tables)

    all_paths = {}
    for haapi in haapis:
        path_items = build_path_items(haapi, haarm, dbml_tables, segment_table_map)
        for path, item in path_items.items():
            if path in all_paths:
                # Merge methods
                all_paths[path].update(item)
            else:
                all_paths[path] = item

    schemas = build_schemas(dbml_tables)

    if not description:
        description = (
            f"{title} REST API 規格。\n\n"
            "本文件由 haAPI + haARM + annotated DBML 自動生成。\n\n"
            "**角色與權限說明** 請參見 `x-required-roles` / `x-required-permissions` extension。"
        )

    doc = {
        "openapi": "3.0.3",
        "info": {
            "title": f"{title} API",
            "version": "1.0.0",
            "description": description,
        },
        "servers": [
            {"url": "http://localhost:8080/api/v1", "description": "本機開發"},
        ],
        "security": [{"bearerAuth": []}],
        "tags": _build_tags(haapis),
        "paths": all_paths,
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT",
                    "description": "JWT Bearer Token",
                }
            },
            "parameters": {
                "OffsetParam": {
                    "name": "offset",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "integer", "default": 0, "minimum": 0},
                    "description": "分頁起始位置",
                },
                "LimitParam": {
                    "name": "limit",
                    "in": "query",
                    "required": False,
                    "schema": {"type": "integer", "default": 20, "minimum": 1, "maximum": 100},
                    "description": "每頁筆數",
                },
            },
            "schemas": schemas,
        },
    }

    return doc


def _build_tags(haapis: list) -> list:
    """Build OpenAPI tags from haAPI modules."""
    tags = []
    for h in haapis:
        tags.append({
            "name": h.get("title", h.get("api", "")),
            "description": h.get("description", ""),
        })
    return tags


# ── 7. YAML output with block style ─────────────────────────────────────────

class BlockStyleDumper(yaml.Dumper):
    """Custom YAML dumper that uses block style for all collections."""
    pass


def _str_representer(dumper, data):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


BlockStyleDumper.add_representer(str, _str_representer)


def dump_yaml(doc: dict) -> str:
    return yaml.dump(
        doc,
        Dumper=BlockStyleDumper,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        indent=2,
        width=120,
    )


# ── 8. CLI entrypoint ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="haAPI -> OpenAPI 3.0.3 converter (rapt-openapi skill)"
    )
    parser.add_argument(
        "--haapi", required=True,
        help="Directory containing *.haapi.yaml files"
    )
    parser.add_argument(
        "--haarm", required=True,
        help="Path to haARM YAML file"
    )
    parser.add_argument(
        "--dbml", required=True,
        help="Path to annotated DBML file"
    )
    parser.add_argument(
        "--output", required=True,
        help="Output path for openapi.yaml"
    )
    parser.add_argument(
        "--title", default=None,
        help="API title (overrides arguments.yml project.name)"
    )
    parser.add_argument(
        "--description", default=None,
        help="API description (overrides arguments.yml project.description)"
    )
    args = parser.parse_args()

    haapi_dir = Path(args.haapi)
    haarm_path = Path(args.haarm)
    dbml_path = Path(args.dbml)
    output_path = Path(args.output)

    # Try to load project info from arguments.yml
    raptor_args = load_arguments_yml(Path.cwd())
    title = args.title
    desc = args.description
    if not title and raptor_args:
        title = raptor_args.get("project", {}).get("name", "API Documentation")
    if not title:
        title = "API Documentation"
    if not desc and raptor_args:
        desc = raptor_args.get("project", {}).get("description", "")
    if not desc:
        desc = ""

    if not haapi_dir.is_dir():
        print(f"[ERROR] haapi directory not found: {haapi_dir}", file=sys.stderr)
        sys.exit(1)
    if not haarm_path.is_file():
        print(f"[ERROR] haarm file not found: {haarm_path}", file=sys.stderr)
        sys.exit(1)
    if not dbml_path.is_file():
        print(f"[ERROR] dbml file not found: {dbml_path}", file=sys.stderr)
        sys.exit(1)

    print(f"[1/5] Loading haARM from {haarm_path} ...")
    haarm = load_haarm(haarm_path)
    print(f"      -> {len(haarm.get('roles', []))} roles, "
          f"{len(haarm.get('permissions', []))} permissions")

    print(f"[2/5] Parsing DBML from {dbml_path} ...")
    dbml_text = dbml_path.read_text(encoding="utf-8")
    dbml_tables = parse_dbml(dbml_text)
    print(f"      -> {len(dbml_tables)} tables: {', '.join(dbml_tables.keys())}")

    print(f"[3/5] Loading haAPI modules from {haapi_dir} ...")
    haapis = load_haapi_dir(haapi_dir)
    print(f"      -> {len(haapis)} modules: "
          f"{', '.join(h.get('api', '?') for h in haapis)}")

    print(f"[4/5] Assembling OpenAPI document ...")
    doc = assemble_openapi(haapis, haarm, dbml_tables, title=title, description=desc)
    total_paths = len(doc["paths"])
    total_ops = sum(
        len([k for k in v.keys() if k in ("get","post","put","delete","patch")])
        for v in doc["paths"].values()
    )
    total_schemas = len(doc["components"]["schemas"])
    print(f"      -> {total_paths} paths, {total_ops} operations, "
          f"{total_schemas} schemas")

    print(f"[5/5] Writing to {output_path} ...")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(dump_yaml(doc), encoding="utf-8")
    print(f"\n[OK] Done! openapi.yaml written to: {output_path}")
    print(f"\n   Preview with:")
    print(f"   npx @redocly/cli preview-docs {output_path}")
    print(f"   # or")
    print(f"   npx swagger-ui-watcher {output_path}")


if __name__ == "__main__":
    main()
