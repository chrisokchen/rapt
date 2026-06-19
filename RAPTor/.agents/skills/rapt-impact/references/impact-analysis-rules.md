# Impact Analysis Rules

## 1. Evidence 與 confidence

| evidence | confidence | 可做的結論 |
|---|---|---|
| DBML Ref、haAPI `entity:`、L3 精確映射 | high | 可列為 deterministic affected |
| L2 read/write table、glossary canonical alias | medium | 可列 affected，但需保留來源限制 |
| 自然語言推斷、檔名相似、未綁定 DSL 引用 | low | 只能列候選，必須提出 GAP/ASM |

- 每筆 graph edge、affected item、regression risk 都要有 evidence。
- evidence 使用 `path:line`、Markdown section、traceability row key或 DSL identifier。
- `evidence: inferred` 不能單獨支撐 `accept`。
- 來源衝突使用 `CON`，不以多數決解決。

## 2. Evidence maturity

| level | 條件 |
|---|---|
| high | 主要 entity 有 haAPI→DBML binding，主要 scenario 有 L3 |
| medium | haAPI 或 L3 只有一項完整，或主要依賴 L2 |
| low | haAPI/L2/L3 稀疏，主要靠全文推斷 |

低 maturity 報告必須：

- 在摘要顯示限制。
- 將不確定 affected item 標 `review_only`。
- recommendation 優先 `needs_clarification`，除非提案明確為 out-of-scope。

## 3. Affected classification

- `create`：提案明確要求新節點，既有 artifact 無精確對應。
- `update`：既有契約或語意必須改變。
- `review_only`：圖譜相鄰但是否修改尚未證實。
- 不得把「可能相關」直接列為 `update`。

## 4. Scope classification

- `new_scope`：新能力不改變既有行為。
- `scope_extension`：擴充既有能力，主要契約仍成立。
- `scope_change`：改變既有 scenario 結果、資料生命週期、API 契約、權限或產品邊界。
- `out_of_scope`：scope 文件明確排除。
- `unclear`：提案或 scope 文件不足。

多種類型同時成立時，優先：`scope_change > out_of_scope > scope_extension > new_scope > unclear`；但來源不足時必須回到 `unclear`。

## 5. Regression severity

沿用 finding taxonomy：

- `blocker`：可能造成資料遺失、未授權存取、法規違反，或核心流程無法成立。
- `high`：改變既有 must-have scenario 或公開 API 契約，且無補償。
- `medium`：需調整既有行為，但有明確 mitigation。
- `low`：局部 UI、非核心路徑或低風險相容調整。
- `info`：只需重產或檢閱。

每筆風險補：

```yaml
route: NEED_TO_FIX | NEED_TO_CLARIFY | NOTE_ONLY
can_fix: true | false
owner_skill: rapt-*
mitigation: <具體措施>
```

## 6. Recommendation

| decision | 使用條件 | handoff |
|---|---|---|
| `accept` | 價值可追蹤、風險可控、關鍵政策已定義 | behavior/modeling/intent/verify |
| `defer` | 有價值但非當前優先，或成本顯著高於近期收益 | clarify 更新 Deferred |
| `reject` | 明確 out-of-scope、價值低且成本高，或有不可接受風險 | clarify 記錄 Out/拒絕理由 |
| `needs_clarification` | 關鍵政策、scope、entity mapping 或風險 mitigation 未定 | clarify |

不得輸出多個並列 recommendation。可在 reason 中說明替代方案。

## 7. Proposed entries 邊界

- `proposed_cic` 與 `proposed_impact_entries` 只存在於 impact report。
- 不直接修改 `.raptor/impact-matrix.yml`、scope 文件或 SSoT。
- proposed impact entry 必須符合 impact-matrix schema，`status` 固定為 `open`。
- `source_ref` 指向本 impact report；待 accept 與正式 decision 後由 clarify/reconcile 重寫為 decision source。

