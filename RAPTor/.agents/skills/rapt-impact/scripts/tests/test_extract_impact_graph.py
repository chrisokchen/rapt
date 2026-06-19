"""extract_impact_graph.py 的核心行為測試。"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "extract_impact_graph.py"
SPEC = importlib.util.spec_from_file_location("extract_impact_graph", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ExtractImpactGraphTest(unittest.TestCase):
    def test_extracts_cross_dsl_edges_and_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ssot = root / "docs" / "ssot"
            (ssot / "dbml").mkdir(parents=True)
            (ssot / "haapi").mkdir()
            (ssot / "hapdl").mkdir()
            (ssot / "haarm").mkdir()
            trace = root / ".raptor" / "traceability.md"
            trace.parent.mkdir()

            (ssot / "dbml" / "schema.dbml").write_text(
                """
Table Product {
  id int [pk]
}
Table ProductReview {
  product_id int [ref: > Product.id]
}
""".strip(),
                encoding="utf-8",
            )
            (ssot / "haapi" / "product.haapi.yaml").write_text(
                """
entity: Product
operations:
  detail:
    operationId: product.detail
""".strip(),
                encoding="utf-8",
            )
            (ssot / "hapdl" / "product-detail.hapdl.yaml").write_text(
                """
page:
  id: product-detail
datasource:
  operationId: product.detail
""".strip(),
                encoding="utf-8",
            )
            (ssot / "haarm" / "product.haarm.yaml").write_text(
                """
permissions:
  - permission: product:read
    operationId: product.detail
""".strip(),
                encoding="utf-8",
            )
            trace.write_text(
                """
## L2 Scenario Data Mapping

| scenario_id | feature | scenario | entities | glossary_terms | read_tables | write_tables | fields | constraints | confidence | source |
|---|---|---|---|---|---|---|---|---|---|---|
| SCN-001 | product.feature | 瀏覽商品 | Product | 商品 | Product |  |  |  | high | product.feature |

## L3 Intent Mapping

| scenario_id | haapi_operation | hapdl_page | haarm_permissions | source |
|---|---|---|---|---|
| SCN-001 | product.detail | product-detail | product:read | product.haapi.yaml |
""".strip(),
                encoding="utf-8",
            )

            data = MODULE.build_graph(ssot, trace).as_dict()
            edge_types = {edge["type"] for edge in data["edges"]}

            self.assertIn("table_rel", edge_types)
            self.assertIn("entity_table", edge_types)
            self.assertIn("page_api", edge_types)
            self.assertIn("permission_api", edge_types)
            self.assertIn("scenario_table", edge_types)
            self.assertIn("scenario_intent", edge_types)
            self.assertEqual(data["coverage"]["l2_rows"], 1)
            self.assertEqual(data["coverage"]["l3_rows"], 1)
            self.assertGreaterEqual(
                data["coverage"]["haapi_entity_bindings"], 1
            )

    def test_missing_l2_mapping_is_not_fatal(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            ssot = root / "ssot"
            ssot.mkdir()
            (ssot / "schema.dbml").write_text(
                "Table Product {\n  id int [pk]\n}\n", encoding="utf-8"
            )
            trace = root / "traceability.md"
            trace.write_text(
                """
## L2 Scenario Data Mapping

| scenario_id | feature | scenario | entities | glossary_terms | read_tables | write_tables | fields | constraints | confidence | source |
|---|---|---|---|---|---|---|---|---|---|---|
| SCN-001 | product.feature | 瀏覽商品 | Product | 商品 |  |  |  |  | low | product.feature |
""".strip(),
                encoding="utf-8",
            )

            data = MODULE.build_graph(ssot, trace).as_dict()

            self.assertEqual(data["coverage"]["l2_rows"], 1)
            self.assertEqual(data["coverage"]["l2_table_mappings"], 0)


if __name__ == "__main__":
    unittest.main()
