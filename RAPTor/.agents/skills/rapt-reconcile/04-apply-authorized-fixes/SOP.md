# 04 Apply Authorized Fixes SOP

**目的**：套用 fix_plan 中 can-fix 項目，並將 need-human 項目委派給 rapt-clarify。

---

## 步驟

### 4.1 APPLY can-fix 項目

對每個 can-fix：

```
UPDATE 目標檔案 {path}：from {from} → to {to}
記錄：修復時間、修復依據（basis）
```

**限制**：
- 只修改 fix_plan 中明確列出的欄位
- 不允許在修復過程中做推斷性補充
- traceability L2/L3 修補必須有 glossary/source_evidence/DBML 精確證據
- CiC 狀態回寫必須有 decision log 精確引用

### 4.2 DELEGATE need-human 項目

對每個 need-human：

```
CREATE CiC note（GAP 或 CON）
DELEGATE to rapt-clarify with:
  - cic_ref: {cic-id}
  - context: {finding 詳情}
  - question: {修復需要確認的問題}
```

### 4.3 RECORD delegate-skill / skill-gap 項目

對 `delegate-skill`：

```
RECORD 建議下一步，不直接修改 artifact。
```

對 `skill-gap`：

```
RECORD target_skill、finding_id、需要補的 SOP/rule。
```

### 4.4 UPDATE session.md

記錄本次修復摘要到 `.raptor/session.md`：

```markdown
## Reconcile Log — {datetime}

### 已修復（can-fix）
- [F001] order.haapi.yaml#list.filters[0].field: createdat → createdAt

### 委派釐清（need-human）
- [F002] CiC GAP-001：order-checkout Scenario 覆蓋缺口 → 委派給 rapt-clarify

### 委派 skill（delegate-skill）
- [RA-B4-001] 建議 /rapt-behavior 補共通負向 Scenario

### Skill 規則缺口（skill-gap）
- [RA-D1-001] rapt-RAscore precheck 需支援 glossary-aware mapping
```

### 4.5 EMIT 完成確認

```
✅ 修復完成

已修復：{N} 項
已建立 CiC 並委派釐清：{M} 項
已記錄委派 skill：{K} 項
已記錄 skill-gap：{S} 項

建議下一步：
  若有委派項目 → /rapt-clarify
  否則 → /rapt-verify 驗證修復結果
```
