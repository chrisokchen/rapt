# 03 Plan Fixes SOP

**目的**：生成修復計畫並 EMIT 給使用者確認，不立即修改。

---

## 步驟

### 3.1 BUILD fix plan

```yaml
fix_plan:
  can_fix:
    - id: F001
      action: UPDATE order.haapi.yaml
      path: list.filters[0].field
      from: createdat
      to: createdAt
      basis: DBML Order.createdAt（case-sensitive）
    - id: F003
      action: UPDATE order.haapi.yaml
      path: access.operations[2].source_evidence[0]
      from: (missing)
      to: "features/order-checkout.feature#Scenario:客戶使用折扣碼結帳"
      basis: Gherkin scenario 已存在

  need_human:
    - id: F002
      action: CREATE CiC GAP，DELEGATE to rapt-clarify
      question: "order-checkout feature Scenario「客戶使用折扣碼結帳」是否需要對應的 haAPI operation？"

  delegate_skill:
    - id: RA-B4-001
      action: RUN /rapt-behavior
      reason: 補共通能力與負向 Scenario

  skill_gap:
    - id: RA-D1-001
      action: UPDATE skill backlog
      target_skill: rapt-RAscore
      reason: precheck 需要 glossary-aware mapping
```

### 3.2 EMIT 修復計畫

```
📋 修復計畫（待確認）

機械性修復（{N} 項，將自動套用）：
  F001: order.haapi.yaml#list.filters[0].field → createdAt
  F003: order.haapi.yaml 補上 source_evidence

語意性問題（{M} 項，委派給 rapt-clarify）：
  F002: Scenario 覆蓋缺口 → 需業務確認

需委派 skill（{K} 項）：
  RA-B4-001: 建議執行 /rapt-behavior 補 Scenario

skill 規則缺口（{S} 項）：
  RA-D1-001: rapt-RAscore precheck 需支援 glossary-aware mapping

繼續套用修復？（直接說「繼續」或提供調整意見）
```

> **注意**：步驟 3 EMIT 後，必須等使用者確認後才進入步驟 4（`04-apply-authorized-fixes`）。
