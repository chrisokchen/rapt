#!/usr/bin/env python3
"""
hapdl2lofi.py
=============
Converts haPDL YAML + annotated DBML + haARM into a self-contained lo-fi wireframe HTML.

This is the reference implementation for the rapt-lofi skill.
It reads SSoT artifacts and generates a preview-only wireframe page.

Usage:
    python hapdl2lofi.py \
        --hapdl  docs/06-frontend-intent/ \
        --dbml   docs/02-data-model/schema.dbml \
        --haarm  docs/03-access-control/mjib-eis.haarm.yaml \
        --output docs/07-lofi-preview/index.html

    # With optional project title:
    python hapdl2lofi.py \
        --hapdl  docs/06-frontend-intent/ \
        --dbml   docs/02-data-model/schema.dbml \
        --haarm  docs/03-access-control/mjib-eis.haarm.yaml \
        --output docs/07-lofi-preview/index.html \
        --title  "My Project"

Origin: Projects/hapdl2lofi.py (mjib prototype, 2026-06-04)
"""

import argparse
import html
import re
import sys
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
# 1. DBML Parser
# ═══════════════════════════════════════════════════════════════════════════════

def parse_dbml(dbml_text: str) -> dict:
    """Returns { "TableName": { "fields": [...], "note": str } }"""
    tables = {}
    table_pattern = re.compile(r'Table\s+(\w+)\s*\{([^}]+)\}', re.DOTALL)
    field_pattern = re.compile(r'^\s*(\w+)\s+([\w\(\),]+)\s*(?:\[([^\]]*)\])?\s*$')
    note_pattern = re.compile(r"Note:\s*'([^']+)'")

    # Collect inline comments for ref_code enum values
    comment_pattern = re.compile(r'^\s*//\s*(\w+):\s*(.+)$')

    for table_match in table_pattern.finditer(dbml_text):
        table_name = table_match.group(1)
        body = table_match.group(2)
        note_m = note_pattern.search(body)
        note = note_m.group(1) if note_m else ""

        fields = []
        enum_values = {}  # field_name -> {code: label, ...}

        lines = body.splitlines()
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith("Note:") or stripped.startswith("indexes"):
                continue

            # Check if it's an inline comment describing enum values
            cm = comment_pattern.match(stripped)
            if cm:
                ref_key = cm.group(1)
                # Parse "N=description, E=description" format
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
                "name": fname,
                "type": ftype,
                "required": is_required,
                "pk": is_pk,
                "sensitive": is_sensitive,
                "label": label,
                "ref_code": ref_code,
                "group": group,
                "default": default,
            })

        # Link enum_values back to fields
        for f in fields:
            if f["ref_code"] and f["ref_code"] in enum_values:
                f["enum_values"] = enum_values[f["ref_code"]]
            else:
                # Check if field name matches any comment key
                if f["name"] in enum_values:
                    f["enum_values"] = enum_values[f["name"]]

        tables[table_name] = {"fields": fields, "note": note}
    return tables


# ═══════════════════════════════════════════════════════════════════════════════
# 2. haARM Loader
# ═══════════════════════════════════════════════════════════════════════════════

def load_haarm(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ═══════════════════════════════════════════════════════════════════════════════
# 3. haPDL Loader
# ═══════════════════════════════════════════════════════════════════════════════

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
# 4. Column notation parser
# ═══════════════════════════════════════════════════════════════════════════════

def parse_column_notation(col_spec) -> dict:
    """
    Parse a column spec. 支援兩種正式格式：
    - dict（format-anchor 標準）：{field: orderId, label: 訂單編號, link: true, format: badge, sortable: true}
    - string 簡寫（quick-ref）：'applicationId#', 'status:badge', 'submittedAt|date^'
    Returns: { name, pk, format, display, sortable, label? }
    """
    if isinstance(col_spec, dict):
        name = col_spec.get("field") or col_spec.get("name", "")
        return {
            "name": name,
            "pk": bool(col_spec.get("pk", False)),
            "format": col_spec.get("format"),
            "display": "badge" if col_spec.get("format") == "badge"
                       else ("link" if col_spec.get("link") else None),
            "sortable": bool(col_spec.get("sortable", False)),
            "label": col_spec.get("label"),
        }

    name = col_spec
    pk = False
    display = None  # badge, link, etc.
    fmt = None      # date, datetime, etc.
    sortable = False

    if name.endswith("^"):
        sortable = True
        name = name[:-1]

    if "#" in name:
        pk = True
        name = name.replace("#", "")

    if ":" in name:
        parts = name.split(":")
        name = parts[0]
        display = parts[1]

    if "|" in name:
        parts = name.split("|")
        name = parts[0]
        fmt = parts[1]

    return {
        "name": name,
        "pk": pk,
        "format": fmt,
        "display": display,
        "sortable": sortable,
    }


def parse_filter_notation(filter_spec) -> dict:
    """Parse a filter spec.

    支援兩種正式格式：
    - dict（format-anchor 標準）：{field: status, label: 狀態, type: eq}
    - string 簡寫（quick-ref）：'status=' / 'name~'
    """
    if isinstance(filter_spec, dict):
        name = filter_spec.get("field") or filter_spec.get("name", "")
        out = {"name": name}
        if filter_spec.get("label"):
            out["label"] = filter_spec["label"]
        return out
    name = str(filter_spec).rstrip("=~").strip()
    return {"name": name}


# ═══════════════════════════════════════════════════════════════════════════════
# 5. HTML Generator
# ═══════════════════════════════════════════════════════════════════════════════

def get_field_info(field_name: str, entity: str, dbml_tables: dict) -> dict:
    """Look up field metadata from DBML."""
    table = dbml_tables.get(entity, {})
    for f in table.get("fields", []):
        if f["name"] == field_name:
            return f
    return {"name": field_name, "label": field_name, "type": "string",
            "required": False, "sensitive": False, "enum_values": None, "ref_code": None}


def get_actor_label(actor_id: str, haarm: dict) -> str:
    """Get display name for an actor/role from haARM."""
    for actor in haarm.get("actors", []):
        if actor["id"] == actor_id:
            return actor.get("name", actor_id)
    for role in haarm.get("roles", []):
        if role["id"] == actor_id:
            return role.get("name", actor_id)
    return actor_id


def esc(s: str) -> str:
    return html.escape(str(s))


def page_fields(page: dict, section: str) -> list:
    """Return fields from the canonical page section, with legacy view fallback."""
    block = page.get(section) or {}
    fields = block.get("fields")
    if fields is not None:
        return fields
    return (page.get("view") or {}).get("fields", [])


def action_ids(page: dict, placement: str) -> list:
    actions = page.get("actions") or {}
    placed = (actions.get("placement") or {}).get(placement, [])
    if placed:
        return placed

    standard = actions.get("standard") or []
    custom = [item.get("name") for item in actions.get("custom") or [] if item.get("name")]
    if placement == "header":
        return standard + custom[:1]
    if placement == "footer":
        form_actions = (page.get("form") or {}).get("actions") or {}
        return [v for v in form_actions.values() if isinstance(v, str)] or standard + custom
    if placement == "row":
        return custom
    return []


def field_label(field_def: dict, fallback: dict, field_name: str) -> str:
    return field_def.get("label") or fallback.get("label") or field_name


def render_page_shell(page: dict, page_type: str, body_html: str, toolbar_html: str = "") -> str:
    title = esc(page.get("title", page.get("page_id", "")))
    page_id = esc(page.get("page_id", ""))
    badge_class = {
        "list": "list-badge",
        "form": "form-badge",
        "detail": "detail-badge",
        "dashboard": "dashboard-badge",
    }.get(page_type, "detail-badge")
    subtitle = esc(page.get("entity", page.get("api", "")))

    return f'''
    <section class="page-card" id="{page_id}">
      <div class="page-header">
        <div>
          <div class="page-title-row">
            <h2>{title}</h2>
            <span class="page-type-badge {badge_class}">{page_type.upper()}</span>
          </div>
          <div class="page-meta">
            <span class="actor-label">{subtitle}</span>
          </div>
        </div>
        {toolbar_html}
      </div>
      {body_html}
    </section>
    '''


# ── Widget Renderers ──────────────────────────────────────────────────────────

def render_widget_text(field_info: dict, is_sensitive: bool = False) -> str:
    label = esc(field_info.get("label", field_info["name"]))
    placeholder = "********" if is_sensitive else label
    icon = ' <span class="sensitive-icon" title="Sensitive">&#128274;</span>' if is_sensitive else ''
    return f'''<input type="text" class="lofi-input" placeholder="{placeholder}" disabled />{icon}'''


def render_widget_textarea(field_info: dict) -> str:
    label = esc(field_info.get("label", field_info["name"]))
    return f'''<textarea class="lofi-textarea" placeholder="{label}" disabled></textarea>'''


def render_widget_select(field_info: dict) -> str:
    enum_values = field_info.get("enum_values", None)
    opts = '<option value="">-- 請選擇 --</option>'
    if enum_values:
        for code, lbl in enum_values.items():
            opts += f'<option value="{esc(code)}">{esc(code)}={esc(lbl)}</option>'
    else:
        opts += '<option value="1">選項 1</option><option value="2">選項 2</option>'
    return f'<select class="lofi-select" disabled>{opts}</select>'


def render_widget_date(field_info: dict) -> str:
    return '<input type="date" class="lofi-input lofi-date" disabled />'


def render_widget_readonly(field_info: dict) -> str:
    label = esc(field_info.get("label", field_info["name"]))
    return f'<span class="lofi-readonly">{label}-001</span>'


WIDGET_RENDERERS = {
    "text": render_widget_text,
    "textarea": render_widget_textarea,
    "select": render_widget_select,
    "date": render_widget_date,
}


# ── Action label helper ──────────────────────────────────────────────────────

# Common action labels (fallback; haPDL may define its own)
DEFAULT_ACTION_LABELS = {
    "create": "+ 新增",
    "view": "檢視",
    "edit": "編輯",
    "delete": "刪除",
    "saveDraft": "暫存草稿",
    "submitApplication": "送出陳核",
    "approveNode": "核准",
    "rejectNode": "退回",
    "adjustNode": "調整流程",
    "executeDispatch": "執行投送",
    "downloadAttachment": "下載附件",
    "extractFeature": "抽取特徵值",
    "verifyFeature": "驗核特徵值",
    "createEmergencyApplication": "緊急調閱",
    "read": "檢視",
    "update": "更新",
    "submit": "送出",
    "approve": "核准",
    "reject": "退回",
}

def _action_label(action_id: str) -> str:
    return DEFAULT_ACTION_LABELS.get(action_id, action_id)


# ── Page Renderers ────────────────────────────────────────────────────────────

def render_list_page(page: dict, dbml_tables: dict, haarm: dict) -> str:
    entity = page.get("entity", "")
    title = esc(page.get("title", page.get("page_id", "")))
    page_id = esc(page.get("page_id", ""))
    actor = get_actor_label(page.get("primary_actor", ""), haarm)
    roles = page.get("auth_roles", [])

    view = page.get("view", {})
    filters_raw = view.get("filters", [])
    columns_raw = view.get("columns", [])

    filters = [parse_filter_notation(f) for f in filters_raw]
    columns = [parse_column_notation(c) for c in columns_raw]

    header_actions = action_ids(page, "header")
    row_actions = action_ids(page, "row")

    # ── Filter bar ──
    filter_html = ""
    for flt in filters:
        fi = get_field_info(flt["name"], entity, dbml_tables)
        label = esc(fi.get("label", flt["name"]))
        if fi.get("enum_values"):
            opts = '<option value="">全部</option>'
            for code, lbl in fi["enum_values"].items():
                opts += f'<option>{esc(code)}={esc(lbl)}</option>'
            widget = f'<select class="lofi-filter-select" disabled>{opts}</select>'
        else:
            widget = f'<input type="text" class="lofi-filter-input" placeholder="{label}" disabled />'
        filter_html += f'<div class="filter-group"><label>{label}</label>{widget}</div>\n'

    # ── Table header ──
    th_html = ""
    for col in columns:
        fi = get_field_info(col["name"], entity, dbml_tables)
        label = esc(fi.get("label", col["name"]))
        sort_icon = ' <span class="sort-icon">&#8597;</span>' if col["sortable"] else ""
        pk_icon = ' <span class="pk-icon">#</span>' if col["pk"] else ""
        th_html += f'<th>{label}{pk_icon}{sort_icon}</th>\n'
    if row_actions:
        th_html += '<th class="actions-col">操作</th>\n'

    # ── Sample rows ──
    rows_html = ""
    sample_data = _generate_sample_rows(columns, entity, dbml_tables, 5)
    for row in sample_data:
        tds = ""
        for i, col in enumerate(columns):
            fi = get_field_info(col["name"], entity, dbml_tables)
            val = row[i]
            if col["display"] == "badge":
                tds += f'<td><span class="lofi-badge">{esc(val)}</span></td>'
            elif col["pk"]:
                tds += f'<td><a class="lofi-link" href="#">{esc(val)}</a></td>'
            else:
                tds += f'<td>{esc(val)}</td>'
        if row_actions:
            btns = "".join(f'<button class="lofi-btn-sm">{esc(_action_label(a))}</button> ' for a in row_actions)
            tds += f'<td class="actions-col">{btns}</td>'
        rows_html += f'<tr>{tds}</tr>\n'

    # ── Header buttons ──
    header_btns = ""
    for act in header_actions:
        header_btns += f'<button class="lofi-btn-primary">{esc(_action_label(act))}</button> '

    # ── Role badges ──
    role_badges = "".join(
        f'<span class="role-badge">{esc(get_actor_label(r, haarm))}</span>' for r in roles
    )

    return f'''
    <section class="page-card" id="{page_id}">
      <div class="page-header">
        <div class="page-title-row">
          <h2>{title}</h2>
          <span class="page-type-badge list-badge">LIST</span>
        </div>
        <div class="page-meta">
          <span class="actor-label">&#128100; {esc(actor)}</span>
          <div class="role-badges">{role_badges}</div>
        </div>
      </div>

      <div class="page-toolbar">
        <div class="filter-bar">{filter_html}</div>
        <div class="toolbar-actions">{header_btns}</div>
      </div>

      <table class="lofi-table">
        <thead><tr>{th_html}</tr></thead>
        <tbody>{rows_html}</tbody>
      </table>

      <div class="pagination">
        <span class="page-info">1-5 / 128 筆</span>
        <div class="page-btns">
          <button class="lofi-btn-sm" disabled>&laquo;</button>
          <button class="lofi-btn-sm active">1</button>
          <button class="lofi-btn-sm">2</button>
          <button class="lofi-btn-sm">3</button>
          <button class="lofi-btn-sm">&raquo;</button>
        </div>
      </div>
    </section>
    '''


def render_form_page(page: dict, dbml_tables: dict, haarm: dict) -> str:
    entity = page.get("entity", "")
    title = esc(page.get("title", page.get("page_id", "")))
    page_id = esc(page.get("page_id", ""))
    actor = get_actor_label(page.get("primary_actor", ""), haarm)
    roles = page.get("auth_roles", [])

    fields = page_fields(page, "form")

    footer_actions = action_ids(page, "footer")

    # ── Form fields ──
    form_html = ""
    for field_def in fields:
        fname = field_def.get("field", "")
        widget_type = field_def.get("widget") or field_def.get("type", "text")
        is_sensitive = field_def.get("sensitive", False)

        fi = get_field_info(fname, entity, dbml_tables)
        fi["label"] = field_label(field_def, fi, fname)
        label = esc(fi["label"])
        required_mark = ' <span class="required">*</span>' if field_def.get("required", fi.get("required")) else ""

        # Merge enum_values from DBML into field_info for widget rendering
        if not fi.get("enum_values") and fi.get("ref_code"):
            fi["enum_values"] = None  # already set or not

        renderer = WIDGET_RENDERERS.get(widget_type, render_widget_text)
        if widget_type == "text" and is_sensitive:
            widget_html = render_widget_text(fi, is_sensitive=True)
        else:
            widget_html = renderer(fi)

        form_html += f'''
        <div class="form-group">
          <label class="form-label">{label}{required_mark}</label>
          <div class="form-widget">{widget_html}</div>
        </div>
        '''

    # ── Footer buttons ──
    footer_btns = ""
    for act in footer_actions:
        btn_class = "lofi-btn-primary" if act != "saveDraft" else "lofi-btn-secondary"
        footer_btns += f'<button class="{btn_class}">{esc(_action_label(act))}</button> '

    # ── Role badges ──
    role_badges = "".join(
        f'<span class="role-badge">{esc(get_actor_label(r, haarm))}</span>' for r in roles
    )

    return f'''
    <section class="page-card" id="{page_id}">
      <div class="page-header">
        <div class="page-title-row">
          <h2>{title}</h2>
          <span class="page-type-badge form-badge">FORM</span>
        </div>
        <div class="page-meta">
          <span class="actor-label">&#128100; {esc(actor)}</span>
          <div class="role-badges">{role_badges}</div>
        </div>
      </div>

      <div class="form-body">
        {form_html}
      </div>

      <div class="form-footer">
        {footer_btns}
      </div>
    </section>
    '''


def render_detail_page(page: dict, dbml_tables: dict, haarm: dict) -> str:
    entity = page.get("entity", "")
    title = esc(page.get("title", page.get("page_id", "")))
    page_id = esc(page.get("page_id", ""))
    actor = get_actor_label(page.get("primary_actor", ""), haarm)
    roles = page.get("auth_roles", [])

    fields = page_fields(page, "detail")

    header_actions = action_ids(page, "header")

    # ── Detail fields ──
    detail_html = ""
    for field_def in fields:
        fname = field_def.get("field", "")
        widget_type = field_def.get("widget", None)

        fi = get_field_info(fname, entity, dbml_tables)
        label = esc(field_label(field_def, fi, fname))

        if widget_type == "select" and fi.get("enum_values"):
            first_val = next(iter(fi["enum_values"].items()), ("?", "?"))
            val_html = f'<span class="lofi-badge">{esc(first_val[0])}={esc(first_val[1])}</span>'
        elif widget_type == "date":
            val_html = '<span class="lofi-readonly">2026-06-04</span>'
        else:
            val_html = f'<span class="lofi-readonly">{label}-001</span>'

        detail_html += f'''
        <div class="detail-row">
          <div class="detail-label">{label}</div>
          <div class="detail-value">{val_html}</div>
        </div>
        '''

    # ── Header action buttons ──
    header_btns = ""
    for act in header_actions:
        header_btns += f'<button class="lofi-btn-primary">{esc(_action_label(act))}</button> '

    # ── Role badges ──
    role_badges = "".join(
        f'<span class="role-badge">{esc(get_actor_label(r, haarm))}</span>' for r in roles
    )

    return f'''
    <section class="page-card" id="{page_id}">
      <div class="page-header">
        <div class="page-title-row">
          <h2>{title}</h2>
          <span class="page-type-badge detail-badge">DETAIL</span>
        </div>
        <div class="page-meta">
          <span class="actor-label">&#128100; {esc(actor)}</span>
          <div class="role-badges">{role_badges}</div>
        </div>
      </div>

      <div class="detail-toolbar">{header_btns}</div>

      <div class="detail-body">
        {detail_html}
      </div>
    </section>
    '''


# ── Helper functions ──────────────────────────────────────────────────────────

def render_dashboard_page(page: dict, dbml_tables: dict, haarm: dict) -> str:
    view = page.get("view") or {}
    filters = [parse_filter_notation(f) for f in view.get("filters", [])]
    cards = view.get("cards", [])

    filter_html = ""
    for flt in filters:
        fi = get_field_info(flt["name"], page.get("entity", ""), dbml_tables)
        label = esc(flt.get("label") or fi.get("label", flt["name"]))
        filter_html += f'<div class="filter-group"><label>{label}</label><select class="lofi-filter-select" disabled><option>全部</option><option>本館</option><option>分館 A</option></select></div>'

    kpis = ""
    for i, card in enumerate(cards, 1):
        label = esc(card.get("label") or card.get("field") or f"KPI {i}")
        value = [18, 42, 7, 5, 12, 96][(i - 1) % 6]
        tone = ["", "ok", "warn", "danger", "info", ""][(i - 1) % 6]
        kpis += f'<div class="kpi-card {tone}"><div class="kpi-value">{value}</div><div class="kpi-label">{label}</div></div>'

    body = f'''
      <div class="page-toolbar">
        <div class="filter-bar">{filter_html}</div>
      </div>
      <div class="dashboard-grid">{kpis}</div>
      <div class="dashboard-panels">
        <div class="panel">
          <div class="panel-title">待辦工作</div>
          <div class="todo-row"><span>候補遞補確認</span><span class="lofi-badge">12</span></div>
          <div class="todo-row"><span>補件審核</span><span class="lofi-badge warn">7</span></div>
          <div class="todo-row"><span>逾期繳費處理</span><span class="lofi-badge danger">5</span></div>
        </div>
        <div class="panel">
          <div class="panel-title">近期活動</div>
          <table class="lofi-table compact">
            <tbody>
              <tr><td>親子故事活動</td><td><span class="lofi-badge ok">報名中</span></td><td>12/20</td></tr>
              <tr><td>AI 入門講座</td><td><span class="lofi-badge">審核中</span></td><td>24/30</td></tr>
              <tr><td>閱讀推廣課</td><td><span class="lofi-badge warn">候補</span></td><td>8/8</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    '''
    return render_page_shell(page, "dashboard", body)


def _generate_sample_rows(columns: list, entity: str, dbml_tables: dict, count: int) -> list:
    """Generate sample data rows for preview."""
    rows = []
    for i in range(1, count + 1):
        row = []
        for col in columns:
            fi = get_field_info(col["name"], entity, dbml_tables)
            if col["pk"] or fi.get("pk"):
                row.append(f"ID-{i:04d}")
            elif fi.get("enum_values"):
                keys = list(fi["enum_values"].keys())
                val = keys[i % len(keys)]
                row.append(f"{val}")
            elif col["format"] == "date" or "At" in col["name"] or "Date" in col["name"]:
                row.append(f"2026-06-{i:02d}")
            elif col["display"] == "badge":
                row.append(f"Tag-{i}")
            else:
                label = fi.get("label", col["name"])
                row.append(f"{label}-{i}")
        rows.append(row)
    return rows


# ═══════════════════════════════════════════════════════════════════════════════
# 6. Full HTML Document
# ═══════════════════════════════════════════════════════════════════════════════

CSS = r"""
:root {
  --bg: #f5f5f0;
  --card-bg: #ffffff;
  --border: #d4d4d4;
  --border-light: #e8e8e8;
  --text: #333333;
  --text-muted: #888888;
  --primary: #4a6fa5;
  --primary-light: #e8eef5;
  --accent: #d4956a;
  --danger: #c0392b;
  --success: #27ae60;
  --badge-bg: #f0f0f0;
  --form-bg: #fafaf8;
  --shadow: 0 2px 12px rgba(0,0,0,0.06);
  --radius: 6px;
  --font: 'Noto Sans TC', 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: var(--font);
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  padding: 0;
}

/* ── Top Navigation ─────────────────────────────── */

.top-nav {
  background: #2c3e50;
  color: white;
  padding: 12px 32px;
  display: flex;
  align-items: center;
  gap: 20px;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.top-nav h1 {
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.top-nav .subtitle {
  font-size: 12px;
  color: #95a5a6;
  font-family: var(--font-mono);
}

.nav-links {
  display: flex;
  gap: 4px;
  margin-left: auto;
  flex-wrap: wrap;
}

.nav-link {
  color: #bdc3c7;
  text-decoration: none;
  font-size: 13px;
  padding: 4px 12px;
  border-radius: 4px;
  transition: all 0.2s;
}

.nav-link:hover, .nav-link.active {
  color: white;
  background: rgba(255,255,255,0.1);
}

/* ── Layout ─────────────────────────────────────── */

.container {
  max-width: 1100px;
  margin: 32px auto;
  padding: 0 24px;
}

.intro {
  background: var(--card-bg);
  border: 1px solid var(--border-light);
  border-radius: var(--radius);
  padding: 20px 28px;
  margin-bottom: 32px;
  box-shadow: var(--shadow);
}

.intro h2 {
  font-size: 15px;
  color: var(--text-muted);
  font-weight: 500;
  margin-bottom: 8px;
}

.intro p {
  font-size: 13px;
  color: var(--text-muted);
  line-height: 1.8;
}

.intro code {
  background: var(--badge-bg);
  padding: 1px 6px;
  border-radius: 3px;
  font-family: var(--font-mono);
  font-size: 12px;
}

/* ── Page Card ──────────────────────────────────── */

.page-card {
  background: var(--card-bg);
  border: 2px solid var(--border);
  border-radius: 8px;
  margin-bottom: 40px;
  overflow: hidden;
  box-shadow: var(--shadow);
  transition: box-shadow 0.3s;
}

.page-card:hover {
  box-shadow: 0 4px 24px rgba(0,0,0,0.1);
}

.page-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-bottom: 2px solid var(--border);
  padding: 16px 24px;
}

.page-title-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.page-title-row h2 {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
}

.page-type-badge {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1.5px;
  padding: 2px 10px;
  border-radius: 3px;
  font-family: var(--font-mono);
}

.list-badge   { background: #dbeafe; color: #1e40af; }
.form-badge   { background: #fef3c7; color: #92400e; }
.detail-badge { background: #d1fae5; color: #065f46; }

.page-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.actor-label {
  font-size: 13px;
  color: var(--text-muted);
}

.role-badges {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.role-badge {
  font-size: 10px;
  background: var(--primary-light);
  color: var(--primary);
  padding: 2px 8px;
  border-radius: 10px;
  font-weight: 500;
}

/* ── Filter & Toolbar ───────────────────────────── */

.page-toolbar {
  padding: 12px 24px;
  border-bottom: 1px solid var(--border-light);
  display: flex;
  align-items: flex-end;
  gap: 16px;
  flex-wrap: wrap;
  background: var(--form-bg);
}

.filter-bar {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  flex: 1;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.filter-group label {
  font-size: 11px;
  color: var(--text-muted);
  font-weight: 500;
}

.lofi-filter-input, .lofi-filter-select {
  border: 1px dashed var(--border);
  background: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  min-width: 110px;
  font-family: var(--font);
  color: var(--text-muted);
}

.toolbar-actions {
  display: flex;
  gap: 8px;
}

/* ── Table ──────────────────────────────────────── */

.lofi-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
}

.lofi-table th {
  text-align: left;
  padding: 10px 16px;
  background: #f8f9fa;
  border-bottom: 2px solid var(--border);
  font-weight: 600;
  font-size: 12px;
  color: var(--text-muted);
  white-space: nowrap;
}

.lofi-table td {
  padding: 10px 16px;
  border-bottom: 1px solid var(--border-light);
}

.lofi-table tbody tr:hover {
  background: #f8fafb;
}

.lofi-table .actions-col {
  text-align: right;
  white-space: nowrap;
}

.sort-icon {
  color: var(--border);
  font-size: 11px;
}

.pk-icon {
  color: var(--accent);
  font-size: 10px;
  font-weight: 700;
}

.lofi-badge {
  display: inline-block;
  background: var(--badge-bg);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 1px 8px;
  font-size: 11px;
  font-family: var(--font-mono);
  color: var(--text-muted);
}

.lofi-link {
  color: var(--primary);
  text-decoration: underline;
  cursor: pointer;
  font-family: var(--font-mono);
  font-size: 12px;
}

/* ── Pagination ─────────────────────────────────── */

.pagination {
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-top: 1px solid var(--border-light);
}

.page-info {
  font-size: 12px;
  color: var(--text-muted);
}

.page-btns {
  display: flex;
  gap: 4px;
}

/* ── Form ───────────────────────────────────────── */

.form-body {
  padding: 24px;
}

.form-group {
  display: grid;
  grid-template-columns: 160px 1fr;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px dotted var(--border-light);
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  padding-top: 6px;
  text-align: right;
}

.required {
  color: var(--danger);
}

.form-widget {
  position: relative;
}

.lofi-input {
  border: 1px dashed var(--border);
  background: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 13px;
  width: 100%;
  max-width: 400px;
  font-family: var(--font);
  color: var(--text-muted);
}

.lofi-textarea {
  border: 1px dashed var(--border);
  background: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 13px;
  width: 100%;
  max-width: 400px;
  min-height: 72px;
  resize: vertical;
  font-family: var(--font);
  color: var(--text-muted);
}

.lofi-select {
  border: 1px dashed var(--border);
  background: white;
  padding: 8px 12px;
  border-radius: 4px;
  font-size: 13px;
  min-width: 200px;
  font-family: var(--font);
  color: var(--text-muted);
}

.lofi-date {
  max-width: 180px;
}

.sensitive-icon {
  font-size: 14px;
  position: absolute;
  right: calc(100% - 412px);
  top: 8px;
  opacity: 0.5;
}

.lofi-readonly {
  font-size: 13px;
  color: var(--text-muted);
  font-family: var(--font-mono);
}

.form-footer {
  padding: 16px 24px;
  border-top: 2px solid var(--border);
  background: #f8f9fa;
  text-align: right;
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

/* ── Detail ─────────────────────────────────────── */

.detail-toolbar {
  padding: 12px 24px;
  border-bottom: 1px solid var(--border-light);
  background: var(--form-bg);
  display: flex;
  gap: 8px;
}

.detail-body {
  padding: 24px;
}

.detail-row {
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 12px;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px dotted var(--border-light);
}

.detail-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-muted);
  text-align: right;
}

.detail-value {
  font-size: 13px;
  color: var(--text);
}

/* ── Buttons ────────────────────────────────────── */

.lofi-btn-primary {
  background: var(--primary);
  color: white;
  border: none;
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 13px;
  font-family: var(--font);
  cursor: pointer;
  transition: opacity 0.2s;
}

.lofi-btn-primary:hover { opacity: 0.85; }

.lofi-btn-secondary {
  background: white;
  color: var(--text);
  border: 1px solid var(--border);
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 13px;
  font-family: var(--font);
  cursor: pointer;
}

.lofi-btn-sm {
  background: white;
  color: var(--text-muted);
  border: 1px solid var(--border);
  padding: 3px 10px;
  border-radius: 3px;
  font-size: 11px;
  font-family: var(--font);
  cursor: pointer;
  transition: all 0.2s;
}

.lofi-btn-sm:hover { border-color: var(--primary); color: var(--primary); }
.lofi-btn-sm.active { background: var(--primary); color: white; border-color: var(--primary); }

/* ── Footer ─────────────────────────────────────── */

.page-footer {
  text-align: center;
  padding: 32px;
  color: var(--text-muted);
  font-size: 12px;
  border-top: 1px solid var(--border-light);
  margin-top: 40px;
}

.page-footer code {
  font-family: var(--font-mono);
  background: var(--badge-bg);
  padding: 1px 6px;
  border-radius: 3px;
}

/* ── Lo-fi Watermark ────────────────────────────── */

.lofi-watermark {
  position: fixed;
  bottom: 16px;
  right: 16px;
  background: rgba(44, 62, 80, 0.8);
  color: white;
  font-size: 10px;
  font-family: var(--font-mono);
  padding: 4px 10px;
  border-radius: 4px;
  z-index: 200;
  letter-spacing: 1px;
}

/* ── Responsive ─────────────────────────────────── */

@media (max-width: 768px) {
  .form-group, .detail-row {
    grid-template-columns: 1fr;
  }
  .form-label, .detail-label {
    text-align: left;
  }
  .page-toolbar {
    flex-direction: column;
  }
}
"""


ADMIN_CSS = r"""
:root {
  --c-primary: #2C6ECB;
  --c-primary-d: #1F569F;
  --c-bg: #F4F6F9;
  --c-surface: #FFFFFF;
  --c-border: #E3E8EF;
  --c-text: #1F2933;
  --c-sub: #6B7785;
  --c-ok: #1F9D55;
  --c-warn: #E8A317;
  --c-danger: #D64545;
  --c-info: #1F569F;
  --radius: 8px;
  --shadow: 0 1px 3px rgba(16,24,40,.08);
}

body {
  background: var(--c-bg);
  color: var(--c-text);
  line-height: 1.5;
}

.app {
  display: flex;
  min-height: 100vh;
}

.top-nav {
  position: sticky;
  top: 0;
  width: 220px;
  height: 100vh;
  flex: 0 0 220px;
  display: block;
  overflow: auto;
  padding: 0;
  background: #13284a;
  box-shadow: none;
}

.top-nav .brand {
  padding: 18px 20px;
  border-bottom: 1px solid rgba(255,255,255,.08);
}

.top-nav h1 {
  font-size: 16px;
  line-height: 1.3;
  letter-spacing: 0;
}

.top-nav .subtitle {
  display: block;
  margin-top: 2px;
  color: #8aa0c0;
  font-family: var(--font);
}

.nav-links {
  display: block;
  margin: 0;
  padding: 10px 0;
}

.nav-link {
  display: block;
  padding: 10px 20px;
  border-radius: 0;
  color: #cdd7e6;
  font-size: 13px;
  text-decoration: none;
}

.nav-link:hover,
.nav-link.active {
  background: rgba(255,255,255,.08);
  color: #fff;
}

.main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.app-topbar {
  height: 56px;
  background: var(--c-surface);
  border-bottom: 1px solid var(--c-border);
  padding: 0 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.app-topbar h1 {
  font-size: 16px;
  margin: 0;
}

.topbar-tools {
  display: flex;
  gap: 8px;
  align-items: center;
}

.search {
  width: 220px;
  border: 1px solid var(--c-border);
  border-radius: 6px;
  padding: 7px 10px;
  font-size: 13px;
}

.container {
  max-width: none;
  margin: 0;
  padding: 24px;
  overflow: auto;
}

.intro,
.page-footer,
.lofi-watermark {
  display: none;
}

.page-card {
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  margin-bottom: 18px;
  box-shadow: var(--shadow);
  background: var(--c-surface);
}

.page-card:hover {
  box-shadow: var(--shadow);
}

.page-header {
  background: var(--c-surface);
  border-bottom: 1px solid var(--c-border);
  padding: 16px 18px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.page-title-row {
  margin: 0 0 4px;
}

.page-title-row h2 {
  font-size: 16px;
  letter-spacing: 0;
}

.page-type-badge,
.role-badge,
.lofi-badge {
  border: 0;
  border-radius: 12px;
  font-family: var(--font);
  font-size: 12px;
  letter-spacing: 0;
  padding: 2px 8px;
}

.dashboard-badge,
.list-badge,
.detail-badge,
.form-badge {
  background: #e4edfb;
  color: var(--c-primary-d);
}

.page-toolbar,
.detail-toolbar,
.form-footer {
  background: #fafbfc;
  border-color: var(--c-border);
}

.filter-group label,
.actor-label,
.page-info,
.detail-label {
  color: var(--c-sub);
}

.lofi-filter-input,
.lofi-filter-select,
.lofi-input,
.lofi-textarea,
.lofi-select {
  border: 1px solid var(--c-border);
  border-radius: 6px;
  color: var(--c-text);
  background: #fff;
}

.table-wrap {
  overflow: auto;
}

.lofi-table th {
  background: #fafbfc;
  border-bottom: 1px solid var(--c-border);
  color: var(--c-sub);
}

.lofi-table td {
  border-bottom: 1px solid var(--c-border);
}

.lofi-table tbody tr:hover td {
  background: #f7f9fb;
}

.lofi-link {
  color: var(--c-primary);
  font-family: var(--font);
  text-decoration: none;
  font-weight: 600;
}

.lofi-badge {
  background: #eef1f5;
  color: var(--c-sub);
}

.lofi-badge.ok,
.kpi-card.ok .kpi-value {
  color: var(--c-ok);
}

.lofi-badge.warn,
.kpi-card.warn .kpi-value {
  color: #9a6b00;
}

.lofi-badge.danger,
.kpi-card.danger .kpi-value {
  color: var(--c-danger);
}

.lofi-btn-primary {
  background: var(--c-primary);
  border-radius: var(--radius);
  padding: 8px 16px;
}

.lofi-btn-primary:hover {
  background: var(--c-primary-d);
  opacity: 1;
}

.lofi-btn-secondary,
.lofi-btn-sm {
  border: 1px solid var(--c-border);
  border-radius: 6px;
  color: var(--c-text);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(120px, 1fr));
  gap: 16px;
  padding: 18px;
}

.kpi-card {
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  padding: 16px;
  background: var(--c-surface);
}

.kpi-value {
  font-size: 24px;
  font-weight: 700;
}

.kpi-label {
  margin-top: 4px;
  color: var(--c-sub);
  font-size: 12px;
}

.dashboard-panels {
  display: grid;
  grid-template-columns: minmax(240px, .8fr) 1.2fr;
  gap: 16px;
  padding: 0 18px 18px;
}

.panel {
  border: 1px solid var(--c-border);
  border-radius: var(--radius);
  background: var(--c-surface);
  padding: 16px;
}

.panel-title {
  font-weight: 700;
  margin-bottom: 10px;
}

.todo-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid var(--c-border);
}

.todo-row:last-child {
  border-bottom: 0;
}

.compact td {
  padding: 9px 10px;
}

@media (max-width: 900px) {
  .app {
    display: block;
  }
  .top-nav {
    position: static;
    width: auto;
    height: auto;
    display: block;
  }
  .nav-links {
    display: flex;
    overflow-x: auto;
  }
  .nav-link {
    white-space: nowrap;
  }
  .dashboard-grid,
  .dashboard-panels {
    grid-template-columns: 1fr;
  }
  .app-topbar {
    align-items: flex-start;
    height: auto;
    padding: 12px 16px;
    flex-direction: column;
  }
}
"""


def generate_html(pages: list, dbml_tables: dict, haarm: dict, project_title: str = "Lo-Fi Preview") -> str:
    """Generate the complete HTML document."""

    # ── Render each page ──
    page_sections = ""
    nav_links = ""
    for page in pages:
        page_type = page.get("type", "list")
        page_id = page.get("page_id", "")
        page_title = page.get("title", page_id)

        nav_links += f'<a class="nav-link" href="#{esc(page_id)}">{esc(page_title)}</a>\n'

        if page_type == "list":
            page_sections += render_list_page(page, dbml_tables, haarm)
        elif page_type == "form":
            page_sections += render_form_page(page, dbml_tables, haarm)
        elif page_type == "detail":
            page_sections += render_detail_page(page, dbml_tables, haarm)
        elif page_type == "dashboard":
            page_sections += render_dashboard_page(page, dbml_tables, haarm)
        else:
            page_sections += f'<section class="page-card"><div class="page-header"><h2>Unknown: {esc(page_id)}</h2></div></section>'

    return f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(project_title)} Lo-Fi Wireframe Preview</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>{CSS}{ADMIN_CSS}</style>
</head>
<body>

  <div class="app">
    <nav class="top-nav">
      <div class="brand">
        <h1>{esc(project_title)}</h1>
        <span class="subtitle">Lo-Fi Preview</span>
      </div>
      <div class="nav-links">
        {nav_links}
      </div>
    </nav>

    <main class="main">
      <header class="app-topbar">
        <div>
          <h1>後台介面預覽</h1>
          <span class="subtitle">generated from haPDL + DBML + haARM</span>
        </div>
        <div class="topbar-tools">
          <input class="search" placeholder="搜尋頁面或欄位" disabled>
          <button class="lofi-btn-secondary" disabled>角色</button>
        </div>
      </header>

      <div class="container">
        <div class="intro">
          <h2>haPDL Lo-Fi Wireframe Preview</h2>
          <p>
            This preview is auto-generated from specs.
          </p>
        </div>

        {page_sections}
      </div>

      <footer class="page-footer">
        Generated by <code>hapdl2lofi.py</code> from haPDL v3.3 spec &middot;
        {len(pages)} pages &middot; {len(dbml_tables)} entities
      </footer>
    </main>
  </div>

</body>
</html>
'''


# ═══════════════════════════════════════════════════════════════════════════════
# 7. CLI
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="haPDL -> Lo-Fi HTML wireframe (rapt-lofi skill)")
    parser.add_argument("--hapdl", required=True, help="Directory with *.hapdl.yaml")
    parser.add_argument("--dbml", required=True, help="Path to annotated DBML")
    parser.add_argument("--haarm", required=True, help="Path to haARM YAML")
    parser.add_argument("--output", required=True, help="Output HTML path")
    parser.add_argument("--title", default=None, help="Project title (overrides arguments.yml)")
    args = parser.parse_args()

    hapdl_dir = Path(args.hapdl)
    dbml_path = Path(args.dbml)
    haarm_path = Path(args.haarm)
    output_path = Path(args.output)

    # Try to load project info from arguments.yml
    raptor_args = load_arguments_yml(Path.cwd())
    project_title = args.title
    if not project_title and raptor_args:
        project_title = raptor_args.get("project", {}).get("name", "Lo-Fi Preview")
    if not project_title:
        project_title = "Lo-Fi Preview"

    print(f"[1/4] Loading DBML from {dbml_path} ...")
    dbml_text = dbml_path.read_text(encoding="utf-8")
    dbml_tables = parse_dbml(dbml_text)
    print(f"      -> {len(dbml_tables)} tables")

    print(f"[2/4] Loading haARM from {haarm_path} ...")
    haarm = load_haarm(haarm_path)
    print(f"      -> {len(haarm.get('roles', []))} roles, {len(haarm.get('actors',[]))} actors")

    print(f"[3/4] Loading haPDL from {hapdl_dir} ...")
    pages = load_hapdl_dir(hapdl_dir)
    print(f"      -> {len(pages)} pages: {', '.join(p.get('page_id','?') for p in pages)}")

    print(f"[4/4] Generating lo-fi HTML ...")
    html_content = generate_html(pages, dbml_tables, haarm, project_title=project_title)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding="utf-8")
    size_kb = output_path.stat().st_size / 1024
    print(f"\n[OK] Lo-fi wireframe written to: {output_path} ({size_kb:.1f} KB)")
    print(f"     Preview: python -m http.server 8089 --directory {output_path.parent}")


if __name__ == "__main__":
    main()
