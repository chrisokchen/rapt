"""Unit tests for dsl-lint.py — L1/L2/L3/L4 + path-convention regression."""
import importlib.util
import sys
from pathlib import Path

import yaml

_HERE = Path(__file__).resolve().parent
_LINT = _HERE.parent / "dsl-lint.py"
spec = importlib.util.spec_from_file_location("dsl_lint", _LINT)
dsl = importlib.util.module_from_spec(spec)
sys.modules["dsl_lint"] = dsl
spec.loader.exec_module(dsl)

SCHEMA_DIR = dsl.find_schema_dir(None)
HAAPI_SCHEMA = dsl.load_schema(SCHEMA_DIR, "haapi-v3.3.schema.json")
HAPDL_SCHEMA = dsl.load_schema(SCHEMA_DIR, "hapdl-v3.3.schema.json")


def codes(findings):
    return {f.code for f in findings}


def lint_haapi(doc, levels=("2", "3")):
    f = []
    if "2" in levels:
        dsl.check_l2_haapi(doc, "x.haapi.yaml", HAAPI_SCHEMA, f)
    if "3" in levels:
        dsl.check_l3_haapi(doc, "x.haapi.yaml", f)
    return f


def lint_hapdl(doc, levels=("2", "3")):
    f = []
    if "2" in levels:
        dsl.check_l2_hapdl(doc, "x.hapdl.yaml", HAPDL_SCHEMA, f)
    if "3" in levels:
        dsl.check_l3_hapdl(doc, "x.hapdl.yaml", f)
    return f


# ── L1 ───────────────────────────────────────────────────────────────────────

def test_l1_yaml_parse_error(tmp_path):
    p = tmp_path / "bad.haapi.yaml"
    p.write_text("api: order\n  bad: : :\n", encoding="utf-8")
    f = []
    assert dsl.load_yaml(p, f) is None
    assert "DSL-PARSE-001" in codes(f)


def test_l1_top_level_not_dict(tmp_path):
    p = tmp_path / "list.hapdl.yaml"
    p.write_text("- a\n- b\n", encoding="utf-8")
    f = []
    assert dsl.load_yaml(p, f) is None
    assert "DSL-PARSE-002" in codes(f)


# ── L2 haAPI ─────────────────────────────────────────────────────────────────

GOOD_HAAPI = {
    "api": "order", "entity": "Order", "schema_version": "3.3",
    "exposes": {"standard": ["list", "read"], "operations": [{"name": "apply_refund", "method": "POST"}]},
    "access": {
        "endpoints": {
            "list": {"required_roles": ["admin"], "required_permissions": [{"id": "order_read"}]},
            "read": {"required_roles": ["admin"], "required_permissions": [{"id": "order_read"}]},
        },
        "operations": {
            "apply_refund": {"required_roles": ["customer"], "required_permissions": [{"id": "order_refund"}]},
        },
    },
}


def test_l2_good_haapi_clean():
    assert lint_haapi(GOOD_HAAPI) == []


def test_l2_array_endpoints():
    doc = {"api": "order", "entity": "Order", "exposes": {"standard": ["list"]},
           "access": {"endpoints": [{"path": "/orders", "methods": ["GET"]}]}}
    assert "HAAPI-SCHEMA-001" in codes(lint_haapi(doc, levels=("2",)))


def test_l2_top_level_endpoints():
    doc = {"api": "order", "entity": "Order", "exposes": {"standard": ["list"]},
           "access": {"endpoints": {}}, "endpoints": [{"id": "order.list"}]}
    assert "HAAPI-SCHEMA-002" in codes(lint_haapi(doc, levels=("2",)))


def test_l2_bare_string_permission():
    doc = {"api": "order", "entity": "Order", "exposes": {"standard": ["list"]},
           "access": {"endpoints": {"list": {"required_permissions": ["order_read"]}}}}
    assert "HAAPI-SCHEMA-003" in codes(lint_haapi(doc, levels=("2",)))


def test_l2_deprecated_access_permissions():
    doc = {"api": "order", "entity": "Order", "exposes": {"standard": ["list"]},
           "access": {"permissions": ["order_read"], "endpoints": {}}}
    assert "HAAPI-SCHEMA-004" in codes(lint_haapi(doc, levels=("2",)))


# ── L2 haPDL ─────────────────────────────────────────────────────────────────

GOOD_HAPDL = {
    "page": "order-list", "type": "list", "title": "訂單列表", "entity": "Order", "api": "order",
    "schema_version": "3.3",
    "view": {"columns": [{"field": "orderId", "label": "訂單編號"}]},
    "auth": {"roles": ["admin"]},
    "security": {"permission_refs": {"view": [{"id": "order_read"}]}, "datasource_scope": "own"},
}


def test_l2_good_hapdl_clean():
    assert lint_hapdl(GOOD_HAPDL) == []


def test_l2_meta_pages_wrapper():
    doc = {"meta": {"module": "order"}, "pages": [{"id": "order-list"}]}
    c = codes(lint_hapdl(doc, levels=("2",)))
    assert "HAPDL-SCHEMA-001" in c


def test_l2_page_id_instead_of_page():
    doc = {"page_id": "order-list", "type": "list", "title": "x", "entity": "Order"}
    assert "HAPDL-SCHEMA-002" in codes(lint_hapdl(doc, levels=("2",)))


def test_l2_legacy_security_permissions():
    doc = dict(GOOD_HAPDL)
    doc["security"] = {"permissions": ["order_read"]}
    assert "HAPDL-LINT-003" in codes(lint_hapdl(doc, levels=("2",)))


# ── L3 ───────────────────────────────────────────────────────────────────────

def test_l3_access_op_not_in_exposes():
    doc = {"api": "order", "entity": "Order",
           "exposes": {"standard": ["list"], "operations": []},
           "access": {"endpoints": {"list": {}}, "operations": {"ghost_op": {}}}}
    assert "HAAPI-LINT-002" in codes(lint_haapi(doc, levels=("3",)))


def test_l3_exposed_op_missing_access_warns():
    doc = {"api": "order", "entity": "Order",
           "exposes": {"standard": ["list", "delete"]},
           "access": {"endpoints": {"list": {}}}}
    f = lint_haapi(doc, levels=("3",))
    assert "HAAPI-LINT-003" in codes(f)
    assert any(x.severity == "WARN" for x in f)


def test_l3_ext_service_not_declared():
    doc = {"api": "order", "entity": "Order", "exposes": {"standard": ["list"]},
           "access": {"endpoints": {"list": {}}},
           "logic": {"steps": [{"action": "ext.smtp.send_email"}]}}
    assert "HAAPI-LINT-005" in codes(lint_haapi(doc, levels=("3",)))


def test_l3_bad_kebab_api():
    doc = dict(GOOD_HAAPI)
    doc["api"] = "OrderItem"
    assert "HAAPI-LINT-001" in codes(lint_haapi(doc, levels=("3",)))


def test_l3_bad_page_type():
    doc = dict(GOOD_HAPDL)
    doc["type"] = "carousel"
    assert "HAPDL-LINT-002" in codes(lint_hapdl(doc, levels=("3",)))


# ── L4 ───────────────────────────────────────────────────────────────────────

def test_l4_entity_not_in_dbml():
    f = []
    dsl.check_l4([("x.haapi.yaml", {"api": "order", "entity": "Ordr", "access": {}})], [],
                 {"Order"}, {"admin"}, {"order_read"}, set(), f)
    assert "XREF-001" in codes(f)


def test_l4_role_not_in_haarm():
    doc = {"api": "order", "entity": "Order",
           "access": {"endpoints": {"list": {"required_roles": ["ghost"]}}}}
    f = []
    dsl.check_l4([("x.haapi.yaml", doc)], [], {"Order"}, {"admin"}, set(), set(), f)
    assert "XREF-002" in codes(f)


def test_l4_permission_not_in_haarm():
    doc = {"api": "order", "entity": "Order",
           "access": {"endpoints": {"list": {"required_permissions": [{"id": "ghost_perm"}]}}}}
    f = []
    dsl.check_l4([("x.haapi.yaml", doc)], [], {"Order"}, set(), {"order_read"}, set(), f)
    assert "XREF-003" in codes(f)


def test_l4_hapdl_api_not_found():
    pdl = {"page": "order-list", "entity": "Order", "api": "ghost-api"}
    f = []
    dsl.check_l4([("o.haapi.yaml", {"api": "order", "entity": "Order", "access": {}})],
                 [("p.hapdl.yaml", pdl)], {"Order"}, set(), set(), set(), f)
    assert "XREF-006" in codes(f)


def test_l4_hapdl_permission_ref_not_in_haarm():
    pdl = {"page": "order-list", "entity": "Order", "api": "order",
           "security": {"permission_refs": {"view": [{"id": "ghost"}]}}}
    f = []
    dsl.check_l4([("o.haapi.yaml", {"api": "order", "entity": "Order", "access": {}})],
                 [("p.hapdl.yaml", pdl)], {"Order"}, set(), {"order_read"}, set(), f)
    assert "XREF-009" in codes(f)
