# RAscore Findings

## Medium

### RA-B5-001

- Criterion: B5
- Category: traceability-gap
- Artifact: `.raptor/traceability.md`
- Location: L2 Scenario Data Mapping
- Issue: 9 個 scenario 的 L2 mapping 仍為 low confidence，業務詞與資料詞對應尚未完全穩定。
- Recommendation: 補強這 9 個 row 的 read_tables、write_tables、fields 或 constraints，並將 confidence 提升為 medium/high。
- Owner Skill: `rapt-reconcile`
- Recommended Action Type: `traceability_mapping`

### RA-D2-001

- Criterion: D2
- Category: cross-spec-gap
- Artifact: `.raptor/traceability.md`
- Location: L2 Scenario Data Mapping
- Issue: 許多舊有 scenario 的 read_tables、write_tables、fields 仍空白，從 scenario 到 DBML 的欄位級可驗證性不足。
- Recommendation: 針對舊有 medium/low confidence rows 補入具體 tables 與 fields，讓情境可直接驅動資料層驗收。
- Owner Skill: `rapt-reconcile`
- Recommended Action Type: `traceability_mapping`

## Low

### RA-A3-001

- Criterion: A3
- Category: scope-creep
- Artifact: `docs/ssot/habdd`
- Location: membership-loyalty / return-refund / merchant-reporting
- Issue: 部分能力已接近完整產品範圍，尚未在 RAscore 階段重新確認 MVP 優先級。
- Recommendation: 在進入實作規劃前標註 MVP/next phase，避免將低優先能力納入首版交付。
- Owner Skill: `manual-review`
- Recommended Action Type: `manual_review`

### RA-C4-001

- Criterion: C4
- Category: dbml-quality
- Artifact: `docs/ssot/dbml/schema.dbml`
- Location: SalesOrder / InventoryItem / PointLedger
- Issue: 部分複合規則尚以 constraints 補充，欄位級計算來源與稽核欄位仍可更明確。
- Recommendation: 若後續要直接 codegen，補充金額計算、庫存預留釋放與點數折抵的稽核欄位或 rule metadata。
- Owner Skill: `rapt-modeling`
- Recommended Action Type: `modeling_revision`

### RA-E3-001

- Criterion: E3
- Category: process-gap
- Artifact: `docs/reports/rascore-precheck.json`
- Location: gherkin.scenario_count
- Issue: RAscore precheck 與 verify 的 scenario count 口徑不同，可能造成報告解讀混淆。
- Recommendation: 後續調整 precheck parser，使其沿用 verify 的 scenario metadata 口徑。
- Owner Skill: `manual-review`
- Recommended Action Type: `process_revision`

### RA-G1-001

- Criterion: G1
- Category: process-gap
- Artifact: `.agents/skills/rapt-RAscore/scripts/rascore_render.py`
- Location: render_report
- Issue: RAscore render 模板的部分固定文字與目前 reports_dir 不一致，且終端顯示有編碼雜訊。
- Recommendation: 修正 skill 模板與 render script 的文字，確保報告內容與 docs/reports 路徑一致。
- Owner Skill: `manual-review`
- Recommended Action Type: `process_revision`

