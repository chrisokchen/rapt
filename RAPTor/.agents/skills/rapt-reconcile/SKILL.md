---
name: rapt-reconcile
description: "RAPTor 規格調和修復。讀取 rapt-verify 報告，將問題分類為機械性（可自動修復）或語意性（需人工決策），對機械性問題直接修復，對語意性問題委派 rapt-clarify。Use when: /rapt-reconcile、rapt-verify 報告有 FAIL/PARTIAL、修復 SSoT 不一致。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: planner
---

# RAPTor Reconcile — 規格調和修復

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::dsl-cross-reference-v33.md]
- LOAD REF [rapt-core::planner-worker-contract.md]
- LOAD REF [rapt-core::cic-note-policy.md]
- LOAD REF [rapt-core::traceability-schema.md]
- LOAD REF [rapt-core::rascore-feedback-policy.md]
- LOAD REF [rapt-core::finding-taxonomy.md]
- LOAD REF [rapt-core::impact-matrix-schema.md]
- LOAD REF [rapt-core::clarify-payload-schema.md]
- LOAD REF [rapt-reconcile::references/fix-policy.md]
- LOAD REF [rapt-reconcile::references/rascore-finding-policy.md]
- LOAD REF [rapt-reconcile::references/reconcile-session-schema.md]

## TRIGGER

- 使用者執行或指定 `rapt-reconcile` 進入此 RAPTor phase。
- 上一階段 artifact 已備妥，需要產出本 phase 對應的 SSoT 規格。

## SKIP

- `.raptor/arguments.yml` 不存在時，停止並建議改用 `/rapt-kickoff`。
- 屬於 worker 的 DSL 純渲染工作，應改用 `rapt-form-*` skill。
- 請求寫入的內容超出本 skill 的 Artifact Output Contract。


## PRINCIPLE: Artifact Output Contract（只改被授權修復的 artifacts）
## PRINCIPLE: STRICT SOP

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| UPDATE | 任何 SSoT artifact | 僅限 fix-policy 定義的「機械性修復」|
| UPDATE | `${paths.traceability_file}` | 僅限有精確 evidence 的 L2/L3 / decision traceability 修補 |
| CREATE / UPDATE | `.raptor/reconcile/sessions/*.yml` | reconcile session record |
| CREATE | `.raptor/reconcile/archive/**` | 修復前 snapshot |
| UPDATE | `.raptor/impact-matrix.yml` | 登錄修復傳播 |
| UPDATE | `.raptor/session.md` | 記錄修復摘要 |
| **DENY** | 語意性變更（需人工決策） | 改委派 rapt-clarify |
| **DENY** | 業務邏輯推斷 | 不自行決定語意 |

---

## SOP

### 步驟 0：READ reports

```

## Reconcile Session Gate

ASSERT:
- 讀取 `verify-report.yml` 時優先使用 machine-readable findings。
- 每次修改 SSoT 前先建立 `.raptor/reconcile/archive/<session-id>/...` snapshot。
- 每次 reconcile 必須建立 `.raptor/reconcile/sessions/<session-id>.yml`。
- phase end 必須列出 `NEED_TO_FIX`、`NEED_TO_CLARIFY`、`NOTE_ONLY`。
- 對下游 artifact 有影響的修復必須更新 `.raptor/impact-matrix.yml`。
READ if exists: ${paths.reports_dir}/verify-report.yml
READ if exists: ${paths.reports_dir}/verify-report.md
READ if exists: ${paths.reports_dir}/rascore-findings.json
READ if exists: ${paths.reports_dir}/rascore-findings.md
READ if exists: ${paths.reports_dir}/rascore-scorecard.yml
若 verify report 不存在但 RAscore findings 存在 → 不停止，標記 verify_missing=true，並建議後續執行 /rapt-verify
```

### 步驟 1：EXECUTE `01-bind-target/SOP.md`

識別需要修復的項目。

### 步驟 2：EXECUTE `02-classify-findings/SOP.md`

分類：機械性（can-fix）vs 語意性（need-human）。

### 步驟 3：EXECUTE `03-plan-fixes/SOP.md`

生成修復計畫（先 EMIT，不立即修改）。

### 步驟 4：EXECUTE `04-apply-authorized-fixes/SOP.md`

套用機械性修復，委派語意性問題到 rapt-clarify。

### 步驟 5：EMIT 修復摘要

```
✅ rapt-reconcile 完成

已修復（機械性）：{N} 項
委派給 rapt-clarify（語意性）：{M} 項
跳過（already OK）：{K} 項

建議下一步：執行 /rapt-verify 驗證修復結果
```
