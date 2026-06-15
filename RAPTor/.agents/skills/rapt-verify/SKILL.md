---
name: rapt-verify
description: "RAPTor Phase 5 規格驗證。讀取所有 SSoT artifacts（DBML、haARM、Gherkin、haAPI、haPDL），執行完整性、一致性、可追蹤性、覆蓋率四項驗證，輸出驗證報告。Use when: /rapt-verify、需要驗證規格、Phase 5。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: verifier
---

# RAPTor Verify — Phase 5 規格驗證

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::ssot-definition.md]
- LOAD REF [rapt-core::dsl-cross-reference-v33.md]
- LOAD REF [rapt-core::phase-gates.md]
- LOAD REF [rapt-core::cic-note-policy.md]
- LOAD REF [rapt-core::finding-taxonomy.md]

## TRIGGER

- ??????? RAPTor artifacts?
- phase gate ????? completeness?consistency?traceability ? coverage report?

## SKIP

- ???????? kickoff?
- ????????? artifact?????? `rapt-reconcile` ? owner skill?


## PRINCIPLE: Artifact Output Contract（只寫 report，不修改 SSoT）
## PRINCIPLE: STRICT SOP

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| CREATE / UPDATE | `${paths.reports_dir}/verify-report.md` | 驗證報告 |
| CREATE / UPDATE | `${paths.reports_dir}/verify-report.yml` | machine-readable findings |
| UPDATE | `.raptor/session.md` | 更新 Phase 5 進度 |
| **DENY** | 任何 SSoT artifact | 只讀，不修改 |
| **DENY** | DBML / haARM / Gherkin / haAPI / haPDL | |

---

## SOP

### 步驟 0：READ arguments.yml

```
READ: .raptor/arguments.yml
ASSERT: .raptor/session.md Phase 4 閘門已通過（或 EMIT 警告）
```

### 步驟 1：EXECUTE `01-completeness/SOP.md`

驗證所有 SSoT 檔案存在。

### 步驟 2：EXECUTE `02-cross-dsl-consistency/SOP.md`

驗證跨 DSL 引用一致性。

### 步驟 3：EXECUTE `03-traceability/SOP.md`

驗證 Gherkin → haAPI / haPDL 可追蹤性。

### 步驟 4：EXECUTE `04-coverage/SOP.md`

計算故事覆蓋率指標。

### 步驟 5：LOAD report-schema

LOAD REF [rapt-verify::references/report-schema.md]

### 步驟 6：WRITE 驗證報告

依 report-schema.md 格式，將四項驗證結果彙整到 `${paths.reports_dir}/verify-report.md` ? `${paths.reports_dir}/verify-report.yml`。


## Finding Split Gate

ASSERT:
- verify ?????? `${paths.reports_dir}/verify-report.md` ? `${paths.reports_dir}/verify-report.yml`?
- ?? finding ???? `route`?`can_fix`?`owner_skill`?`artifact`?`location`?`evidence`?`suggested_action`?
- phase end ???? `NEED_TO_FIX`?`NEED_TO_CLARIFY`?`NOTE_ONLY`?
- `rapt-verify` ??????? SSoT????? `rapt-reconcile` ? owner skill?

### 步驟 7：EMIT 驗證摘要

```
✅ Phase 5 Verification 完成

結果：PASS / PARTIAL / FAIL
  - 完整性：PASS（所有 SSoT 檔案存在）
  - 跨 DSL 一致性：PARTIAL（2 項 WARNING）
  - 可追蹤性：FAIL（3 個 Scenario 無對應 haAPI）
  - 覆蓋率：78%（must-have 100%）

報告：${verify_report_file}

建議下一步：執行 /rapt-reconcile 修復 FAIL / WARNING 項目
```
