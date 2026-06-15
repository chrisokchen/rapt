# 02 Classify Findings SOP

**目的**：將 binding_list 中的每個問題分類為機械性（can-fix）或語意性（need-human）。

---

## 分類標準

LOAD REF [rapt-reconcile::references/fix-policy.md]
LOAD REF [rapt-reconcile::references/rascore-finding-policy.md]

依 fix-policy.md 定義：

| 類型 | 定義 | 處理方式 |
|------|------|---------|
| `can-fix` | 機械性問題，正確值可從其他 SSoT 確定取得 | 直接修復 |
| `need-human` | 需要業務決策的語意性問題 | DELEGATE to rapt-clarify |
| `delegate-skill` | 需由 behavior/modeling/intent/verify/RAscore 重跑或補產物 | 記入下一步建議 |
| `skill-gap` | 重複 finding 顯示 skill SOP / rules 缺規則 | 記入 skill improvement backlog |

---

## 步驟

### 2.1 對每個 finding 判斷類型

```
機械性（can-fix）的例子：
  - entity: 大小寫不符（DBML 有精確值）
  - api: 引用錯誤（haAPI 有精確 id）
  - permission.id 拼寫不一致（haARM 有精確值）
  - source_evidence 欄位遺漏（可補上 file#location 格式）
  - filter.field 大小寫不符（DBML 有精確 column name）

語意性（need-human）的例子：
  - haARM 完全缺少某個 resource 的定義（需業務決策）
  - must-have story 無對應 Feature（需補寫 Gherkin）
  - permission 語意不明（needs clarification）
  - 業務流程有衝突（多處矛盾描述）

RAscore findings 的分類例子：
  - traceability L2 缺列，但 glossary + DBML + source_evidence 可精確定位 → can-fix
  - discovery CiC 未標 RESOLVED，但 decision log 有明確決策 → can-fix
  - Then 含「阻擋或警示」→ need-human
  - ref_code 值域未知 → need-human，delegate rapt-clarify 後由 rapt-modeling 更新 seeds.md
  - 共通能力缺 Scenario → delegate-skill: rapt-behavior
  - verify report 不存在 → delegate-skill: rapt-verify
```

### 2.2 OUTPUT classified_list

```yaml
can_fix:
  - id: F001
    type: entity-case
    fix: rename createdat → createdAt
    confidence: high

need_human:
  - id: F002
    type: missing-scenario-coverage
    reason: Scenario 無對應 haAPI，可能是遺漏的業務需求
    cic_type: GAP
    delegate_to: rapt-clarify

delegate_skill:
  - id: RA-B4-001
    delegate_to: rapt-behavior
    reason: 共通負向 Scenario 規則需由 behavior 補產物

skill_gap:
  - id: RA-D1-001
    target_skill: rapt-RAscore
    reason: precheck 需要 glossary-aware mapping
```
