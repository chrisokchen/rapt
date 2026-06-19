# Impact Report Schema

YAML 與 Markdown 必須表達同一份分析。YAML 是 canonical machine-readable report；Markdown 不得引入 YAML 沒有的決策或風險。

## 目錄

- [YAML shape](#yaml-shape)
- [Required enums](#required-enums)
- [Consistency assertions](#consistency-assertions)

## YAML shape

```yaml
schema_version: 1
id: IA-20260619-001
revision: 1
generated_at: "2026-06-19T10:30:00+08:00"
advisory_only: true

proposal:
  title: 商品評論
  source_ref: whatif/product-review.md
  mode: existing
  summary: 允許顧客對已購商品評分與評論。
  entities: [Product, ProductReview]
  actions: [create_review, moderate_review]
  actors: [customer, moderator]

evidence_maturity:
  level: medium
  extractor_used: true
  haapi_entity_bindings: {found: 3, files: 2}
  traceability_l2: {rows: 12, mapped_rows: 4, coverage: 0.3333}
  traceability_l3: {rows: 8, mapped_rows: 6, coverage: 0.75}
  limitations: [評論尚無既有 intent mapping]

classification:
  type: scope_extension
  confidence: medium
  evidence: [docs/discovery/04-vision-kpi-scope.md#In]

graph_trace:
  - from: entity:Product
    to: table:Product
    edge_type: entity_table
    path: [haapi:product.detail, L3:SCN-BROWSE-001, hapdl:product-detail]
    evidence: docs/ssot/haapi/product.haapi.yaml:8
    confidence: high

affected:
  dbml:
    create:
      - artifact: docs/ssot/dbml/schema.dbml
        target: Table ProductReview
        evidence: inferred
        confidence: low
    update:
      - artifact: docs/ssot/dbml/schema.dbml
        target: Table Product
        risk: 評分聚合欄位可能形成衍生資料一致性問題
        compensating_rule: CON-REVIEW-001
        evidence: docs/ssot/haapi/product.haapi.yaml:8
        confidence: high
    review_only: []
  habdd: {create: [], update: [], review_only: []}
  haarm: {create: [], update: [], review_only: []}
  haapi: {create: [], update: [], review_only: []}
  hapdl: {create: [], update: [], review_only: []}
  traceability: {create: [], update: [], review_only: []}
  generated: {create: [], update: [], review_only: []}

regression_risks:
  - id: RISK-001
    scenario: SCN-BROWSE-001
    summary: 商品下架後評論顯示與保留策略未定義
    severity: medium
    route: NEED_TO_CLARIFY
    can_fix: false
    owner_skill: rapt-clarify
    evidence: docs/ssot/habdd/product-browsing.ha.feature:42
    mitigation: 先裁決刪除與保留政策

facets:
  data: []
  api: []
  ui: []
  permission: []
  behavior: []
  traceability: []
  generated: []

value_alignment:
  kpi_refs: [KPI-轉換率]
  fit: medium
  rationale: 評論可增加購買信心，但目前沒有直接量測設計。

cost_risk:
  breadth: medium
  regression: medium
  uncertainty: medium
  implementation_shape: medium
  summary: 需新增評論資料、審核權限與商品頁狀態。

verification:
  rerun:
    - skill: rapt-verify
      target: 跨 DSL 一致性與 L2/L3 覆蓋
    - skill: rapt-RAscore
      target: 新增需求品質與可追蹤性
  acceptance_evidence:
    - 評論建立、審核、下架保留的 scenario 全部可追蹤

recommendation:
  decision: needs_clarification
  reason: 評論審核與商品刪除時的保留政策未定義
  next_owner: rapt-clarify

confidence:
  overall: medium
  missing_evidence: [評論審核流程, 刪除保留政策]
  opened_cic: [CiC-260619-001]

proposed_cic:
  - id: CiC-260619-001
    type: BDY
    target: docs/discovery/04-vision-kpi-scope.md
    location: Deferred
    summary: 商品評論是否納入 scope_extension 待裁決
    route: NEED_TO_CLARIFY

clarify_payload:
  batch_id: CLR-BATCH-20260619-001
  source_skill: rapt-impact
  source_report: docs/reports/impact/IA-20260619-001.yml
  questions: []

proposed_impact_entries:
  - source_type: clarify_decision
    source_ref: docs/reports/impact/IA-20260619-001.yml
    target_artifact: docs/ssot/dbml/schema.dbml
    impact_type: create
    status: open
    owner_skill: rapt-modeling
    notes: 待提案 accept 與 decision apply 後正式 upsert。

analysis_warnings: []
```

## Required enums

- `classification.type`: `new_scope | scope_extension | scope_change | out_of_scope | unclear`
- confidence / maturity / fit: `high | medium | low`；fit 可另用 `unknown`
- `recommendation.decision`: `accept | defer | reject | needs_clarification`
- affected bucket: `create | update | review_only`
- severity: `blocker | high | medium | low | info`

## Consistency assertions

- `advisory_only` 必須為 `true`。
- `id` 與檔名一致。
- recommendation 只能有一個。
- Markdown 摘要的 classification、最高風險、fit 與 recommendation 必須等於 YAML。
- `accept` 不得仍有未處理 blocker 或關鍵 GAP/CON。
- `proposed_impact_entries` 不得宣稱已套用。
