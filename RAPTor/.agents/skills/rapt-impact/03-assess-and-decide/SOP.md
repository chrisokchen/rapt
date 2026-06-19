# 03 Assess and Decide SOP

**目的**：從提案種子遍歷受影響集合，評估回歸風險、價值與成本，收斂成單一決策建議。

LOAD REF [rapt-impact::references/impact-analysis-rules.md]。

## 步驟 3.1：遍歷 affected set

從每個 existing seed 雙向遍歷：

```text
table/entity ↔ haAPI operation ↔ L3 scenario ↔ haPDL page ↔ haARM permission
        ↕
    related table
```

每個節點分類：

- `create`：既有圖無對應，提案需要新增。
- `update`：提案會改變既有契約、欄位、行為或權限。
- `review_only`：有鄰接關係，但目前無足夠證據證明需要修改。

`update` 項必須有 `risk`；涉及 legacy/反正規化/相容性時必須有 `compensating_rule` 或 proposed CON。

## 步驟 3.2：判定 scope

READ `04-vision-kpi-scope.md` 的 In/Out/Deferred 與 KPI。

只選一個：

- `new_scope`：建立獨立能力，未改變既有行為。
- `scope_extension`：擴充既有能力，維持主要語意。
- `scope_change`：改變既有 scenario、資料契約、權限或邊界語意。
- `out_of_scope`：明確落在 Out。
- `unclear`：scope 文件或提案證據不足。

若同時符合 extension 與 change，選風險較高的 `scope_change`。

## 步驟 3.3：評估既有行為與回歸

對所有 `update` 與 scenario 鄰接的 `review_only`：

- 指出既有 scenario。
- 描述新提案可能改變的前置條件、結果、錯誤路徑、資料生命週期或授權邊界。
- 提供 evidence、severity、route、owner skill 與 mitigation。

severity 沿用 `blocker | high | medium | low | info`。無 evidence 的風險不得高於 `medium`，除非它是明確的安全/資料遺失政策缺口。

## 步驟 3.4：分面評估

至少檢查：

- Data：table、field、relation、migration、retention、compatibility。
- API：operation、request/response、error、idempotency、backward compatibility。
- UI：page、state、action、validation、empty/error/loading state。
- Permission：actor、role、permission、ownership、separation of duties。
- Behavior：happy path、alternative、error、existing scenario semantics。
- Traceability：L1/L2/L3 與 decision traceability 是否需更新。
- Generated：只列 `regenerate/review_only`，本 skill 不執行。

## 步驟 3.5：價值與成本

DERIVE：

```yaml
value_alignment:
  kpi_refs: []
  fit: high | medium | low | unknown
  rationale: ""
cost_risk:
  breadth: narrow | medium | wide
  regression: blocker | high | medium | low | info
  uncertainty: high | medium | low
  implementation_shape: small | medium | large | unknown
```

KPI 找不到時使用 `fit: unknown`，不得自行創造 KPI。

## 步驟 3.6：收斂 recommendation

依序套用：

1. 關鍵政策未定義、種子無法對應或有來源衝突 → `needs_clarification`。
2. blocker/high 風險且無可行 mitigation → `reject`；若可透過業務決策解除，改 `needs_clarification`。
3. `out_of_scope`，或 value fit low 且成本/風險高 → `defer` 或 `reject`；需說明兩者取捨。
4. value fit 為 high/medium、風險可控且 verification plan 可執行 → `accept`。

每份報告只允許一個 recommendation，並附可執行 handoff。

