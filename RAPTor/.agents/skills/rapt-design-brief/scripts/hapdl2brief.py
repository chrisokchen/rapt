#!/usr/bin/env python3
"""
hapdl2brief.py
==============
Converts haPDL YAML + annotated DBML + haARM into a structured
"Design Brief" markdown document that can be directly fed to
Claude Design (or any AI design tool) to generate Hi-Fi UI.

This is the reference implementation for the rapt-design-brief skill.

Usage:
    python hapdl2brief.py \
        --hapdl  docs/06-frontend-intent/ \
        --dbml   docs/02-data-model/schema.dbml \
        --haarm  docs/03-access-control/mjib-eis.haarm.yaml \
        --output docs/08-design-brief/design-brief.md

    # With optional project info:
    python hapdl2brief.py \
        --hapdl  docs/06-frontend-intent/ \
        --dbml   docs/02-data-model/schema.dbml \
        --haarm  docs/03-access-control/mjib-eis.haarm.yaml \
        --output docs/08-design-brief/design-brief.md \
        --title  "My Project" \
        --description "My project description" \
        --language "zh-hant"

Output:
    A single markdown file containing:
    1. Design System specification (colors, typography, spacing)
    2. Per-page component specifications
    3. Field definitions with types, labels, enum values, sample data
    4. Action button definitions
    5. Role-based access annotations
    6. Sample data for each page

Origin: Projects/hapdl2brief.py (mjib prototype, 2026-06-04)
"""

import argparse
import re
import sys
import json
from pathlib import Path

import yaml


# ═══════════════════════════════════════════════════════════════════════════════
# 0. arguments.yml loader
# ═══════════════════════════════════════════════════════════════════════════════

def load_arguments_yml(cwd: Path) -> dict | None:
    """Try to load .raptor/arguments.yml from CWD. Returns None if not found."""
    args_path = cwd / ".raptor" / "arguments.yml"
    if args_path.is_file():
        with open(args_path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    return None


# ═══════════════════════════════════════════════════════════════════════════════
# 1. DBML Parser (reused)
# ═══════════════════════════════════════════════════════════════════════════════

def parse_dbml(dbml_text: str) -> dict:
    tables = {}
    table_pattern = re.compile(r'Table\s+(\w+)\s*\{([^}]+)\}', re.DOTALL)
    field_pattern = re.compile(r'^\s*(\w+)\s+([\w\(\),]+)\s*(?:\[([^\]]*)\])?\s*$')
    note_pattern = re.compile(r"Note:\s*'([^']+)'")
    comment_pattern = re.compile(r'^\s*//\s*(\w+):\s*(.+)$')

    for table_match in table_pattern.finditer(dbml_text):
        table_name = table_match.group(1)
        body = table_match.group(2)
        note_m = note_pattern.search(body)
        note = note_m.group(1) if note_m else ""

        fields = []
        enum_values = {}

        for line in body.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("Note:") or stripped.startswith("indexes"):
                continue
            cm = comment_pattern.match(stripped)
            if cm:
                ref_key = cm.group(1)
                pairs = cm.group(2).split(",")
                vals = {}
                for pair in pairs:
                    pair = pair.strip()
                    if "=" in pair:
                        code, label = pair.split("=", 1)
                        vals[code.strip()] = label.strip()
                enum_values[ref_key] = vals
                continue
            fm = field_pattern.match(stripped)
            if not fm:
                continue
            fname = fm.group(1)
            ftype = fm.group(2)
            attrs_raw = fm.group(3) or ""
            is_pk = "pk" in attrs_raw
            is_required = "not null" in attrs_raw or is_pk
            is_sensitive = "sensitive: true" in attrs_raw
            label_m = re.search(r"label:\s*'([^']+)'", attrs_raw)
            label = label_m.group(1) if label_m else fname
            ref_code_m = re.search(r"ref_code:\s*'?(\w+)'?", attrs_raw)
            ref_code = ref_code_m.group(1) if ref_code_m else None
            group_m = re.search(r"group:\s*'?(\w+)'?", attrs_raw)
            group = group_m.group(1) if group_m else "basic"
            default_m = re.search(r"default:\s*'?([^',\]]+)'?", attrs_raw)
            default = default_m.group(1).strip() if default_m else None

            fields.append({
                "name": fname, "type": ftype, "required": is_required,
                "pk": is_pk, "sensitive": is_sensitive, "label": label,
                "ref_code": ref_code, "group": group, "default": default,
            })

        for f in fields:
            if f["ref_code"] and f["ref_code"] in enum_values:
                f["enum_values"] = enum_values[f["ref_code"]]
            elif f["name"] in enum_values:
                f["enum_values"] = enum_values[f["name"]]
            else:
                f["enum_values"] = None

        tables[table_name] = {"fields": fields, "note": note}
    return tables


def load_haarm(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_hapdl_dir(directory: Path) -> list:
    pages = []
    for p in sorted(directory.glob("*.hapdl.yaml")):
        with open(p, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            sys.exit(f"✗ [DSL-PARSE-002] {p.name}\n    檔案頂層不是 mapping。")
        # D3：偵測 meta/pages 多頁打包 → 報錯擋下，不展開相容
        if "meta" in data or "pages" in data:
            sys.exit(
                f"✗ [HAPDL-SCHEMA-001] {p.name}\n"
                f"    出現 meta/pages 多頁打包，違反一檔一頁。\n"
                f"    fix: 拆成多個檔案，每檔頂層為 `page: <kebab-id>`。先跑 dsl-lint.py。"
            )
        data["_file"] = str(p.name)
        # 正式鍵 → 既有讀取點 normalize（page_id ← page；auth_roles ← auth.roles）
        data.setdefault("page_id", data.get("page", ""))
        data.setdefault("auth_roles", (data.get("auth") or {}).get("roles", []))
        pages.append(data)
    return pages


# ═══════════════════════════════════════════════════════════════════════════════
# 2. Field info helpers
# ═══════════════════════════════════════════════════════════════════════════════

def get_field_info(field_name: str, entity: str, dbml_tables: dict) -> dict:
    table = dbml_tables.get(entity, {})
    for f in table.get("fields", []):
        if f["name"] == field_name:
            return f
    return {"name": field_name, "label": field_name, "type": "string",
            "required": False, "sensitive": False, "enum_values": None,
            "ref_code": None, "pk": False, "group": "basic", "default": None}


def get_actor_label(actor_id: str, haarm: dict) -> str:
    for actor in haarm.get("actors", []):
        if actor["id"] == actor_id:
            return actor.get("name", actor_id)
    for role in haarm.get("roles", []):
        if role["id"] == actor_id:
            return role.get("name", actor_id)
    return actor_id


def dbml_type_to_ui_type(ftype: str) -> str:
    """Map DBML type to a human-friendly UI input type."""
    ftype_lower = ftype.strip().lower()
    if re.match(r"nvarchar\(\d+\)", ftype_lower) or re.match(r"nchar\(\d+\)", ftype_lower):
        return "text"
    if ftype_lower in ("int", "bigint"):
        return "number"
    if ftype_lower == "bit":
        return "checkbox"
    if re.match(r"datetime2\(\d+\)", ftype_lower):
        return "datetime"
    if ftype_lower == "nvarchar(max)":
        return "textarea"
    return "text"


def dbml_type_to_max_length(ftype: str) -> int | None:
    m = re.match(r"n(?:var)?char\((\d+)\)", ftype.strip().lower())
    return int(m.group(1)) if m else None


ACTION_LABELS = {
    "create": "+ 新增", "view": "檢視", "edit": "編輯", "delete": "刪除",
    "saveDraft": "暫存草稿", "submitApplication": "送出陳核",
    "approveNode": "核准", "rejectNode": "退回", "adjustNode": "調整流程",
    "executeDispatch": "執行投送", "downloadAttachment": "下載附件",
    "extractFeature": "抽取特徵值", "verifyFeature": "驗核特徵值",
    "createEmergencyApplication": "緊急調閱",
    "read": "檢視", "update": "更新",
    "submit": "送出", "approve": "核准", "reject": "退回",
}

ACTION_STYLES = {
    "create": "primary", "saveDraft": "secondary", "submitApplication": "primary",
    "approveNode": "success", "rejectNode": "danger", "adjustNode": "warning",
    "executeDispatch": "primary", "downloadAttachment": "secondary",
    "extractFeature": "primary", "verifyFeature": "primary",
    "view": "ghost", "edit": "ghost", "delete": "danger-ghost",
    "read": "ghost", "update": "primary",
    "submit": "primary", "approve": "success", "reject": "danger",
}

# Column notation parser
def parse_column_notation(col_spec) -> dict:
    # dict（format-anchor 標準）：{field, label, link, format, sortable}
    if isinstance(col_spec, dict):
        return {
            "name": col_spec.get("field") or col_spec.get("name", ""),
            "pk": bool(col_spec.get("pk", False)),
            "format": col_spec.get("format"),
            "display": "badge" if col_spec.get("format") == "badge"
                       else ("link" if col_spec.get("link") else None),
            "sortable": bool(col_spec.get("sortable", False)),
            "label": col_spec.get("label"),
        }
    name = col_spec
    pk = False; display = None; fmt = None; sortable = False
    if name.endswith("^"):
        sortable = True; name = name[:-1]
    if "#" in name:
        pk = True; name = name.replace("#", "")
    if ":" in name:
        parts = name.split(":"); name = parts[0]; display = parts[1]
    if "|" in name:
        parts = name.split("|"); name = parts[0]; fmt = parts[1]
    return {"name": name, "pk": pk, "format": fmt, "display": display, "sortable": sortable}


def parse_filter_notation(filter_spec) -> dict:
    # dict（format-anchor 標準）：{field, label, type}
    if isinstance(filter_spec, dict):
        out = {"name": filter_spec.get("field") or filter_spec.get("name", "")}
        if filter_spec.get("label"):
            out["label"] = filter_spec["label"]
        return out
    return {"name": str(filter_spec).rstrip("=~").strip()}


# ═══════════════════════════════════════════════════════════════════════════════
# 3. Sample data generator
# ═══════════════════════════════════════════════════════════════════════════════

def get_sample_value(field_name: str, fi: dict, idx: int = 0) -> str:
    """Generate a generic sample value from field metadata."""
    if fi.get("enum_values"):
        keys = list(fi["enum_values"].keys())
        return keys[idx % len(keys)]
    if fi.get("sensitive"):
        return "********"
    if fi.get("pk"):
        return f"ID-{idx+1:04d}"
    if "At" in field_name or "Date" in field_name:
        return f"2026-06-{(idx+1):02d} 09:00"
    if "Id" in field_name and field_name != field_name:
        return f"REF-{idx+1:04d}"
    return f"{fi.get('label', field_name)}-{idx+1}"


# ═══════════════════════════════════════════════════════════════════════════════
# 4. Brief Generator
# ═══════════════════════════════════════════════════════════════════════════════

def generate_design_system_section() -> str:
    return """
## Design System

> Use this as the global design language for all pages.

### Color Palette

| Token | Value | Usage |
|:---|:---|:---|
| `--primary` | `#2563eb` (Blue 600) | Primary buttons, links, active states |
| `--primary-hover` | `#1d4ed8` (Blue 700) | Hover state |
| `--success` | `#16a34a` (Green 600) | Approve actions, success states |
| `--danger` | `#dc2626` (Red 600) | Delete, reject actions |
| `--warning` | `#d97706` (Amber 600) | Warnings, adjust actions |
| `--bg-page` | `#f8fafc` (Slate 50) | Page background |
| `--bg-card` | `#ffffff` | Card/panel backgrounds |
| `--bg-header` | `#1e293b` (Slate 800) | Top navigation / sidebar |
| `--border` | `#e2e8f0` (Slate 200) | Borders, dividers |
| `--text-primary` | `#0f172a` (Slate 900) | Headings, labels |
| `--text-secondary` | `#64748b` (Slate 500) | Descriptions, hints |
| `--badge-blue` | `#dbeafe` bg / `#1e40af` text | Status badges (info) |
| `--badge-green` | `#dcfce7` bg / `#166534` text | Status badges (success) |
| `--badge-amber` | `#fef3c7` bg / `#92400e` text | Status badges (warning) |
| `--badge-red` | `#fee2e2` bg / `#991b1b` text | Status badges (danger) |
| `--badge-gray` | `#f1f5f9` bg / `#475569` text | Status badges (neutral) |

### Typography

| Element | Font | Size | Weight |
|:---|:---|:---|:---|
| Page title | Noto Sans TC | 20px | 700 |
| Section heading | Noto Sans TC | 16px | 600 |
| Table header | Noto Sans TC | 13px | 600 |
| Body text | Noto Sans TC | 14px | 400 |
| Label | Noto Sans TC | 13px | 600 |
| Badge | JetBrains Mono | 12px | 500 |
| Button | Noto Sans TC | 14px | 500 |
| Hint/caption | Noto Sans TC | 12px | 400 |

### Spacing

| Token | Value |
|:---|:---|
| Page padding | 24px |
| Card padding | 20px |
| Form field gap | 16px |
| Table cell padding | 12px 16px |
| Button padding | 8px 20px |
| Border radius (card) | 8px |
| Border radius (button) | 6px |
| Border radius (input) | 6px |
| Border radius (badge) | 4px |

### Component Library (reference)

Use **Ant Design** or **shadcn/ui** component patterns:
- Table: sortable headers, row hover, row actions menu
- Form: label-left layout (label 120px, input flex-1), validation messages
- Select: searchable dropdown with Chinese labels
- DatePicker: range selector for date fields
- Badge: colored status badge with icon
- Button: primary / secondary / ghost / danger variants
- Modal: confirmation dialogs for destructive actions
- Breadcrumb: for navigation context
- Sidebar: collapsible left navigation

### Layout Structure

```
+------------------------------------------+
| Top Nav (dark bg, logo, user menu)       |
+--------+---------------------------------+
| Side   | Breadcrumb                      |
| Nav    +---+-----------------------------+
|        |   | Page Title        [Actions]  |
|        |   +-+---------------------------+
|        |   | | Filter Bar                 |
|        |   | +---------------------------+
|        |   | | Content (Table/Form/Detail)|
|        |   | +---------------------------+
|        |   | | Pagination / Footer        |
+--------+---+-----------------------------+
```
"""


def generate_page_brief(page: dict, dbml_tables: dict, haarm: dict, page_idx: int) -> str:
    """Generate a complete page design brief."""
    entity = page.get("entity", "")
    title = page.get("title", page.get("page_id", ""))
    page_id = page.get("page_id", "")
    page_type = page.get("type", "list")
    actor = get_actor_label(page.get("primary_actor", ""), haarm)
    roles = page.get("auth_roles", [])
    source = page.get("_file", "")

    sections = []

    # ── Header ──
    sections.append(f"### Page {page_idx}: {title}")
    sections.append("")
    sections.append(f"| Property | Value |")
    sections.append(f"|:---|:---|")
    sections.append(f"| Page ID | `{page_id}` |")
    sections.append(f"| Type | **{page_type.upper()}** |")
    sections.append(f"| Entity | `{entity}` |")
    sections.append(f"| Primary Actor | {actor} |")
    sections.append(f"| Allowed Roles | {', '.join(get_actor_label(r, haarm) for r in roles)} |")
    sections.append(f"| Source | `{source}` |")
    sections.append("")

    if page_type == "list":
        sections.extend(_generate_list_brief(page, entity, dbml_tables, haarm))
    elif page_type == "form":
        sections.extend(_generate_form_brief(page, entity, dbml_tables, haarm))
    elif page_type == "detail":
        sections.extend(_generate_detail_brief(page, entity, dbml_tables, haarm))

    sections.append("")
    sections.append("---")
    sections.append("")

    return "\n".join(sections)


def _generate_list_brief(page, entity, dbml_tables, haarm) -> list:
    lines = []
    view = page.get("view", {})
    actions = page.get("actions", {})
    filters_raw = view.get("filters", [])
    columns_raw = view.get("columns", [])
    header_actions = actions.get("placement", {}).get("header", [])
    row_actions = actions.get("placement", {}).get("row", [])

    # ── Filters ──
    filters = [parse_filter_notation(f) for f in filters_raw]
    lines.append("#### Filter Bar")
    lines.append("")
    lines.append("| Field | Label | Widget | Options |")
    lines.append("|:---|:---|:---|:---|")
    for flt in filters:
        fi = get_field_info(flt["name"], entity, dbml_tables)
        label = fi.get("label", flt["name"])
        if fi.get("enum_values"):
            opts = ", ".join(f"`{k}`={v}" for k, v in fi["enum_values"].items())
            widget = "Select (dropdown)"
        else:
            opts = "Free text"
            widget = "Text input"
        lines.append(f"| `{flt['name']}` | {label} | {widget} | {opts} |")
    lines.append("")

    # ── Columns ──
    columns = [parse_column_notation(c) for c in columns_raw]
    lines.append("#### Table Columns")
    lines.append("")
    lines.append("| # | Field | Label | Display | Sortable | Sample Values |")
    lines.append("|:---|:---|:---|:---|:---|:---|")
    for i, col in enumerate(columns):
        fi = get_field_info(col["name"], entity, dbml_tables)
        label = fi.get("label", col["name"])
        display = col["display"] or ("link" if col["pk"] else "text")
        if fi.get("enum_values"):
            display = "badge"
        sortable = "Yes" if col["sortable"] else "-"
        samples = ", ".join(f"`{get_sample_value(col['name'], fi, j)}`" for j in range(3))
        lines.append(f"| {i+1} | `{col['name']}` | {label} | {display} | {sortable} | {samples} |")
    lines.append("")

    # ── Badge mapping ──
    badge_fields = [col for col in columns if col.get("display") == "badge" or
                    get_field_info(col["name"], entity, dbml_tables).get("enum_values")]
    if badge_fields:
        lines.append("#### Status Badge Color Mapping")
        lines.append("")
        for col in badge_fields:
            fi = get_field_info(col["name"], entity, dbml_tables)
            if fi.get("enum_values"):
                lines.append(f"**{fi.get('label', col['name'])}** (`{col['name']}`):")
                lines.append("")
                lines.append("| Code | Label | Badge Color |")
                lines.append("|:---|:---|:---|")
                for code, lbl in fi["enum_values"].items():
                    color = _suggest_badge_color(code, col["name"])
                    lines.append(f"| `{code}` | {lbl} | {color} |")
                lines.append("")

    # ── Actions ──
    lines.append("#### Actions")
    lines.append("")
    if header_actions:
        lines.append("**Header actions** (top-right of table):")
        lines.append("")
        for act in header_actions:
            label = ACTION_LABELS.get(act, act)
            style = ACTION_STYLES.get(act, "primary")
            lines.append(f"- `{act}`: **{label}** (Button style: `{style}`)")
        lines.append("")
    if row_actions:
        lines.append("**Row actions** (right side of each row, or overflow menu `...`):")
        lines.append("")
        for act in row_actions:
            label = ACTION_LABELS.get(act, act)
            style = ACTION_STYLES.get(act, "ghost")
            lines.append(f"- `{act}`: **{label}** (Button style: `{style}`)")
        lines.append("")

    # ── Pagination ──
    lines.append("#### Pagination")
    lines.append("")
    lines.append("- Style: `offset` (page numbers + prev/next)")
    lines.append("- Default page size: 20")
    lines.append("- Show: `1-20 / 128 筆` format")
    lines.append("")

    # ── Sample Data ──
    lines.extend(_generate_sample_data_json(columns, entity, dbml_tables))

    return lines


def _generate_form_brief(page, entity, dbml_tables, haarm) -> list:
    lines = []
    view = page.get("view", {})
    actions = page.get("actions", {})
    fields = view.get("fields", [])
    footer_actions = actions.get("placement", {}).get("footer", [])

    lines.append("#### Form Fields")
    lines.append("")
    lines.append("| # | Field | Label | Widget | Required | Sensitive | Options / Constraints | Sample Value |")
    lines.append("|:---|:---|:---|:---|:---|:---|:---|:---|")

    for i, field_def in enumerate(fields):
        fname = field_def.get("field", "")
        widget = field_def.get("widget", "text")
        is_sensitive = field_def.get("sensitive", False)
        fi = get_field_info(fname, entity, dbml_tables)
        label = fi.get("label", fname)
        required = "Yes" if fi.get("required") else "-"
        sensitive = "Yes (mask `********`)" if is_sensitive else "-"
        max_len = dbml_type_to_max_length(fi.get("type", ""))

        constraints = []
        if fi.get("enum_values"):
            constraints.append("Options: " + ", ".join(f"`{k}`={v}" for k, v in fi["enum_values"].items()))
        if max_len:
            constraints.append(f"Max length: {max_len}")
        if fi.get("default"):
            constraints.append(f"Default: `{fi['default']}`")
        constraints_str = "; ".join(constraints) if constraints else "-"

        sample = get_sample_value(fname, fi, 0)
        if is_sensitive:
            sample = "********"

        lines.append(f"| {i+1} | `{fname}` | {label} | `{widget}` | {required} | {sensitive} | {constraints_str} | `{sample}` |")

    lines.append("")

    # ── Form layout hint ──
    lines.append("#### Form Layout")
    lines.append("")
    lines.append("- **Layout**: Label-left, 2-column for short fields (text, select, date), full-width for textarea")
    lines.append("- **Grouping**: Group by DBML `group` attribute if available")
    lines.append("- **Validation**: Show inline error messages below each field")
    lines.append("- **Sensitive fields**: Show a lock icon and mask input by default, with a toggle to reveal")
    lines.append("")

    # ── Actions ──
    lines.append("#### Footer Actions")
    lines.append("")
    for act in footer_actions:
        label = ACTION_LABELS.get(act, act)
        style = ACTION_STYLES.get(act, "primary")
        lines.append(f"- `{act}`: **{label}** (Button style: `{style}`)")
    lines.append("")

    # ── Interaction notes ──
    lines.append("#### Interaction Notes")
    lines.append("")
    if "saveDraft" in [a for a in footer_actions]:
        lines.append("- **Save Draft**: Saves without validation, shows success toast")
    if "submitApplication" in [a for a in footer_actions]:
        lines.append("- **Submit**: Validates all required fields, shows confirmation modal before submit")
    if "approveNode" in [a for a in footer_actions]:
        lines.append("- **Approve/Reject/Adjust**: Show confirmation modal with reason textarea")
    lines.append("")

    return lines


def _generate_detail_brief(page, entity, dbml_tables, haarm) -> list:
    lines = []
    view = page.get("view", {})
    actions = page.get("actions", {})
    fields = view.get("fields", [])
    header_actions = actions.get("placement", {}).get("header", [])

    lines.append("#### Detail Fields")
    lines.append("")
    lines.append("| # | Field | Label | Display | Sample Value |")
    lines.append("|:---|:---|:---|:---|:---|")

    for i, field_def in enumerate(fields):
        fname = field_def.get("field", "")
        widget = field_def.get("widget", None)
        fi = get_field_info(fname, entity, dbml_tables)
        label = fi.get("label", fname)
        sample = get_sample_value(fname, fi, 0)

        if widget == "select" and fi.get("enum_values"):
            display = "Badge (colored status)"
        elif widget == "date":
            display = "Formatted date"
        elif fi.get("pk"):
            display = "Monospace, bold"
        else:
            display = "Plain text"

        lines.append(f"| {i+1} | `{fname}` | {label} | {display} | `{sample}` |")

    lines.append("")

    # ── Layout ──
    lines.append("#### Detail Layout")
    lines.append("")
    lines.append("- **Layout**: 2-column key-value grid (label left-aligned, value right)")
    lines.append("- **Section dividers**: Group related fields with subtle horizontal rules")
    lines.append("- **Related data**: Show related tables below (e.g., attachments list, audit history)")
    lines.append("")

    # ── Actions ──
    if header_actions:
        lines.append("#### Header Actions")
        lines.append("")
        for act in header_actions:
            label = ACTION_LABELS.get(act, act)
            style = ACTION_STYLES.get(act, "primary")
            lines.append(f"- `{act}`: **{label}** (Button style: `{style}`)")
        lines.append("")

    return lines


def _suggest_badge_color(code: str, field_name: str) -> str:
    """Suggest a badge color based on status code semantics."""
    code_upper = code.upper()
    if code_upper in ("DR", "PN", "W", "P", "N"):
        return "gray (neutral/pending)"
    if code_upper in ("PA", "DS"):
        return "blue (in progress)"
    if code_upper in ("AP", "D", "C", "A"):
        return "green (completed/approved)"
    if code_upper in ("RJ", "R", "E"):
        return "red (rejected/error)"
    if code_upper in ("CL",):
        return "gray (closed)"
    if code_upper in ("CN",):
        return "amber (cancelled)"
    return "gray (default)"


def _generate_sample_data_json(columns, entity, dbml_tables) -> list:
    """Generate sample JSON data for the table."""
    lines = []
    lines.append("#### Sample Data (JSON)")
    lines.append("")
    lines.append("```json")
    rows = []
    for i in range(3):
        row = {}
        for col in columns:
            fi = get_field_info(col["name"], entity, dbml_tables)
            row[col["name"]] = get_sample_value(col["name"], fi, i)
        rows.append(row)
    lines.append(json.dumps(rows, ensure_ascii=False, indent=2))
    lines.append("```")
    lines.append("")
    return lines


# ═══════════════════════════════════════════════════════════════════════════════
# 5. Navigation map (dynamic)
# ═══════════════════════════════════════════════════════════════════════════════

def generate_navigation_map(pages: list, haarm: dict) -> str:
    lines = []
    lines.append("## Page Navigation Map")
    lines.append("")
    lines.append("```")
    lines.append("Sidebar Navigation:")
    lines.append("")

    # Group by API module
    groups = {}
    for page in pages:
        api = page.get("api", "other")
        groups.setdefault(api, []).append(page)

    for api, api_pages in groups.items():
        lines.append(f"  [{api}]")
        for p in api_pages:
            icon = {"list": "☰", "form": "✏", "detail": "📄"}.get(p.get("type", ""), "·")
            lines.append(f"    {icon} {p.get('title', p.get('page_id', ''))}")
    lines.append("```")
    lines.append("")

    # Page flow (dynamic based on page types)
    lines.append("### Page Flow")
    lines.append("")
    lines.append("```")
    list_pages = [p for p in pages if p.get("type") == "list"]
    form_pages = [p for p in pages if p.get("type") == "form"]
    detail_pages = [p for p in pages if p.get("type") == "detail"]

    for lp in list_pages:
        title = lp.get("title", lp.get("page_id", ""))
        lines.append(f"{title} (list)")
        lines.append(f"  ├── [+ 新增] → (form)")
        lines.append(f"  ├── [檢視]   → (detail)")
        lines.append(f"  └── [編輯]   → (form, edit mode)")
        lines.append("")

    for fp in form_pages:
        title = fp.get("title", fp.get("page_id", ""))
        lines.append(f"{title} (form)")
        lines.append(f"  └── [送出/核准] → back to list")
        lines.append("")

    for dp in detail_pages:
        title = dp.get("title", dp.get("page_id", ""))
        lines.append(f"{title} (detail)")
        actions = dp.get("actions", {}).get("placement", {}).get("header", [])
        for act in actions:
            label = ACTION_LABELS.get(act, act)
            lines.append(f"  ├── [{label}] → action")
        lines.append("")

    lines.append("```")
    lines.append("")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════════════════════
# 6. Assemble full document
# ═══════════════════════════════════════════════════════════════════════════════

def generate_brief(pages: list, dbml_tables: dict, haarm: dict,
                   title: str = "UI Design Brief",
                   description: str = "",
                   language: str = "zh-hant") -> str:
    doc = []

    lang_display = {
        "zh-hant": "Traditional Chinese (zh-TW)",
        "zh-hans": "Simplified Chinese (zh-CN)",
        "en": "English",
    }.get(language, language)

    # Title
    doc.append(f"# {title} UI Design Brief")
    doc.append("")
    doc.append("> **Purpose**: This document is a structured design brief auto-generated from")
    doc.append("> `haPDL` (page intent specs) + `schema.dbml` (data model) + `haARM` (access control).")
    doc.append("> Feed this entire document to **Claude Design** or any AI design tool to generate")
    doc.append("> Hi-Fi mockups, HTML, or React component code.")
    doc.append(">")
    if description:
        doc.append(f"> **System**: {description}")
    doc.append(f"> **Language**: {lang_display}")
    doc.append("> **Target framework**: React + Ant Design (or shadcn/ui)")
    doc.append("")
    doc.append("---")
    doc.append("")

    # Design system
    doc.append(generate_design_system_section())

    # Navigation
    doc.append(generate_navigation_map(pages, haarm))

    # Per-page briefs
    doc.append("## Page Specifications")
    doc.append("")
    for i, page in enumerate(pages, 1):
        doc.append(generate_page_brief(page, dbml_tables, haarm, i))

    # Closing prompt
    doc.append("")
    doc.append("## Generation Instructions")
    doc.append("")
    doc.append("When generating UI from this brief:")
    doc.append("")
    doc.append("1. **Use the Design System** above for all colors, typography, and spacing")
    doc.append(f"2. **Render all text in {lang_display}** as specified in each page")
    doc.append("3. **Include the sidebar navigation** as shown in the Navigation Map")
    doc.append("4. **Use the sample data** provided for each page to populate the preview")
    doc.append("5. **Apply badge colors** as specified in the Status Badge Color Mapping")
    doc.append("6. **Include responsive layout** that works on 1280px+ screens")
    doc.append("7. **For forms**: show validation states, required field markers (*), and sensitive field masks")
    doc.append("8. **For tables**: include sortable column headers, hover states, and row action buttons")
    doc.append("9. **For detail pages**: use a clean key-value layout with grouped sections")
    doc.append("10. Generate as **React + TypeScript** with **Ant Design** components, or as standalone **HTML + CSS**")
    doc.append("")

    return "\n".join(doc)


# ═══════════════════════════════════════════════════════════════════════════════
# 7. CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="haPDL -> Design Brief for Claude Design (rapt-design-brief skill)")
    parser.add_argument("--hapdl", required=True, help="Directory with *.hapdl.yaml")
    parser.add_argument("--dbml", required=True, help="Path to annotated DBML")
    parser.add_argument("--haarm", required=True, help="Path to haARM YAML")
    parser.add_argument("--output", required=True, help="Output markdown path")
    parser.add_argument("--title", default=None, help="Project title (overrides arguments.yml)")
    parser.add_argument("--description", default=None, help="Project description (overrides arguments.yml)")
    parser.add_argument("--language", default=None, help="Project language: zh-hant, en, zh-hans (overrides arguments.yml)")
    args = parser.parse_args()

    hapdl_dir = Path(args.hapdl)
    dbml_path = Path(args.dbml)
    haarm_path = Path(args.haarm)
    output_path = Path(args.output)

    # Try to load project info from arguments.yml
    raptor_args = load_arguments_yml(Path.cwd())
    title = args.title
    desc = args.description
    lang = args.language
    if raptor_args:
        proj = raptor_args.get("project", {})
        if not title:
            title = proj.get("name", "UI Design Brief")
        if not desc:
            desc = proj.get("description", "")
        if not lang:
            lang = proj.get("language", "zh-hant")
    if not title:
        title = "UI Design Brief"
    if not desc:
        desc = ""
    if not lang:
        lang = "zh-hant"

    print(f"[1/4] Loading DBML from {dbml_path} ...")
    dbml_text = dbml_path.read_text(encoding="utf-8")
    dbml_tables = parse_dbml(dbml_text)
    print(f"      -> {len(dbml_tables)} tables")

    print(f"[2/4] Loading haARM from {haarm_path} ...")
    haarm = load_haarm(haarm_path)
    print(f"      -> {len(haarm.get('roles', []))} roles, {len(haarm.get('actors', []))} actors")

    print(f"[3/4] Loading haPDL from {hapdl_dir} ...")
    pages = load_hapdl_dir(hapdl_dir)
    print(f"      -> {len(pages)} pages: {', '.join(p.get('page_id', '?') for p in pages)}")

    print(f"[4/4] Generating design brief ...")
    brief = generate_brief(pages, dbml_tables, haarm,
                           title=title, description=desc, language=lang)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(brief, encoding="utf-8")
    size_kb = output_path.stat().st_size / 1024
    print(f"\n[OK] Design brief written to: {output_path} ({size_kb:.1f} KB)")
    print(f"     Copy this file to Claude Design to generate Hi-Fi UI!")


if __name__ == "__main__":
    main()
