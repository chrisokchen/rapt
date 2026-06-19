# Impact Graph Extractor Contract

`scripts/extract_impact_graph.py` 是可選的 deterministic context condenser，不是完整 DSL parser，也不負責決策。

## CLI

```text
python extract_impact_graph.py --ssot-dir <dir> [--trace <file>] \
  [--format json|md] [--output <file>]
```

## Output

```yaml
schema_version: 1
nodes:
  - {id: "table:Product", type: table, label: Product, source: "schema.dbml:1"}
edges:
  - from: "haapi:product.detail"
    to: "table:Product"
    type: entity_table
    evidence: "product.haapi.yaml:8"
    confidence: high
coverage:
  dbml_tables: 1
  dbml_relationships: 0
  haapi_files: 1
  haapi_entity_bindings: 1
  l2_rows: 0
  l2_table_mappings: 0
  l3_rows: 1
  l3_mappings: 1
warnings: []
```

## Guarantees

- 只讀輸入。
- 使用 Python stdlib。
- 所有 edge 附 evidence 與 confidence。
- 無法解析時略過並記 warning，不臆造關係。
- L2 空白是合法狀態，coverage 必須反映，不視為 fatal error。

## Non-goals

- 不做模糊 entity matching。
- 不執行 `--affected-by` 決策查詢。
- 不判斷 create/update/review_only。
- 不產生 recommendation。

