# 02 Build Impact Graph SOP

**目的**：建立跨 DSL 關係圖，並明確標示每條關係的證據成熟度。

## 步驟 2.1：優先執行 deterministic extractor

### 2.1.1 檢查快取

先檢查 `${paths.impact_dir}/impact-graph-YYYYMMDD.json` 是否已存在（YYYYMMDD 為今日日期）：

- **存在且 SSoT 未變更**（檔案修改時間晚於所有 SSoT 與 traceability 的最後修改時間）→ 直接 READ 快取，跳至步驟 2.2。在報告 `analysis_warnings` 記錄 `graph_source: cached`。
- **不存在或 SSoT 已變更** → 執行 extractor。

### 2.1.2 執行 extractor 並持久化

若 `scripts/extract_impact_graph.py` 可執行：

```text
RUN: python {skill_dir}/scripts/extract_impact_graph.py \
  --ssot-dir ${paths.ssot_dir} \
  --trace ${paths.traceability_file} \
  --format json \
  --output ${paths.impact_dir}/impact-graph-YYYYMMDD.json
```

持久化規則：

- 輸出固定存到 `${paths.impact_dir}/impact-graph-YYYYMMDD.json`（與 IA 報告同目錄）。
- 同日重跑時覆蓋同一檔案（SSoT 可能已更新）。
- 不得寫入 SSoT 或 generated 目錄。
- 此檔案**非 SSoT**，是 deterministic 中間產物，可安全刪除與重建。

持久化的好處：

- **同日多次 what-if** 不必每次重跑 extractor（SSoT 沒變，graph 也不會變）。
- **可稽核**：事後可驗證 graph 是否正確反映當時的 SSoT 狀態。
- **跨 skill 複用**：`rapt-verify`、`rapt-RAscore` 未來可直接讀取這份 graph。

LOAD REF [rapt-impact::references/extractor-contract.md] 解讀輸出。

若腳本失敗：

- 保留錯誤摘要於報告的 `analysis_warnings`。
- 不產生 `impact-graph-YYYYMMDD.json`（避免存入壞資料）。
- 降級為直接讀取 SSoT。
- 不得因此停止整體分析。

## 步驟 2.2：補足 extractor 未涵蓋的語意

READ extractor 未能可靠解析的 artifact，補建下列節點與邊：

- `table_rel`：DBML table 外鍵關係。
- `entity_table`：haAPI `entity:` 到 DBML Table。
- `scenario_table`：traceability L2 read/write tables。
- `scenario_intent`：L3 scenario 到 haAPI operation、haPDL page、haARM permission。
- `page_api`：haPDL page 到 haAPI operation/endpoint。
- `permission_api` / `permission_page`：haARM permission 到 API/page。
- `decision_artifact`：Decision Traceability 或 impact-matrix 的既有傳播關係。

不得用檔名相似就建立 high-confidence 邊。檔名或自然語言相似只可作低信心候選。

## 步驟 2.3：套用證據優先序

每條邊使用：

| 來源 | confidence | 規則 |
|---|---|---|
| haAPI `entity:`、L3 精確列、DBML Ref | high | deterministic |
| L2 明確 read/write table | medium | intent 後衍生資料，仍需檢查來源 |
| glossary canonical/legacy alias | medium | 只證明命名對應 |
| LLM 讀全文推斷、檔名相似 | low | `evidence: inferred` 並提出 GAP/ASM |

若來源互相衝突，建立 `CON`，不要任選一個答案。

## 步驟 2.4：評估 evidence maturity

DERIVE：

```yaml
evidence_maturity:
  level: high | medium | low
  haapi_entity_bindings: {found: 0, files: 0}
  traceability_l2: {rows: 0, mapped_rows: 0, coverage: 0.0}
  traceability_l3: {rows: 0, mapped_rows: 0, coverage: 0.0}
  extractor_used: true
  limitations: []
```

建議判定：

- `high`：haAPI entity binding 存在，且 L3 有足以追蹤主要 scenario 的映射。
- `medium`：只有其中一項完整，或主要依賴 L2。
- `low`：haAPI/L3/L2 皆稀疏，主要靠全文推斷。

## 步驟 2.5：映射提案種子

依序將 `business_entities` 對應：

1. glossary canonical / legacy aliases。
2. haAPI entity binding。
3. DBML Table 精確名稱。
4. 低信心語意候選。

分類為：

- `existing_seed`：已有精確節點。
- `create_candidate`：提案明確但既有圖沒有節點。
- `unclear_seed`：可能對應多個節點或無足夠證據。

所有 `unclear_seed` 必須進入 missing evidence 與 proposed CiC。

