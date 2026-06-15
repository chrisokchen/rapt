# Prompt Migration Map

本文件記錄 `RAPTor/0_prompts/` 目錄中現有 prompt 與新 rapt-* skill sub-SOP 的對應關係。

**原則**：
- `0_prompts/` 目錄的 prompt 保持**不動**（不刪除、不修改）。
- skill sub-SOP 是更新的實作方式，但現有 prompt 仍可直接使用。
- 本表提供雙向對應，方便使用者決定用 skill 還是手動 prompt。

---

## Planner Prompts → rapt-* skills 對應

| 舊 Prompt 檔案 | 對應 skill / sub-SOP | 說明 |
|--------------|---------------------|------|
| `0_prompts/processPrompts.md` | `rapt-discovery` + `rapt-behavior` | 整體流程，Phase 1~1.5 |
| `0_prompts/processPrompts_Opus.md` | `rapt-discovery` + `rapt-behavior` | Opus 版，同上 |
| `0_prompts/Common/` | `rapt-core` references | 共用原則 |
| `0_prompts/Pipeline/` | 整體 rapt-* skill 流程 | Pipeline 整合 |
| `0_prompts/QualityGates/` | `rapt-verify` | 品質閘門 |
| `0_prompts/tools/` | `rapt-core::paths-and-arguments.md` | 工具鏈相關 |

---

## 需求文件 Prompts → sub-SOP 對應

| 舊 Prompt 路徑 | 對應 skill / sub-SOP |
|--------------|---------------------|
| `0_prompts/SDD/` | `rapt-modeling/02-annotated-dbml/SOP.md` |
| `0_prompts/PageDL/` | `rapt-intent/02-page-intent-slicing/SOP.md` + `rapt-form-hapdl` |
| `0_prompts/Automation/` | Wave 7（deferred；TypeSpec/PDL 生成）|

---

## 審查清單文件 → rapt-verify 對應

| 舊文件 | 對應 rapt-* skill |
|--------|-----------------|
| `RAPTor/需求發展與審查清單/bdd-GherkinCheckList.md` | `rapt-behavior/rules/high-level-gherkin-rules.md` |
| `RAPTor/需求發展與審查清單/bdd-GherkinCheckLog.md` | `rapt-clarify/01-gap-scan/SOP.md` |
| `RAPTor/需求發展與審查清單/bdd-GherkinCheckSuggest.md` | `rapt-clarify/02-question-packaging/SOP.md` |
| `RAPTor/認證授權代碼管理/rbac_checkSuggest.md` | `rapt-modeling/rules/haarm-v33-rules.md` |

---

## Templates → arguments / form-* 對應

| 舊 Template | 對應 |
|-----------|------|
| `0_reqDevProcess/templates/` | `rapt-kickoff/references/arguments-schema.md` (path defaults) |
| `0_reqDevProcess/spec.md` | `rapt-core::ssot-definition.md` |

---

## 重要說明

1. **skill 不取代 prompt**：技術上 skill 是更可重複執行的方式，但現有 prompt 對熟悉流程的用戶仍有價值。
2. **雙軌並存**：使用者可選擇直接呼叫 skill（`/rapt-discovery`）或手動貼 prompt，兩者結果應一致。
3. **Wave 7 延後項目**：`0_prompts/Automation/` 的 TypeSpec/PDL 生成 prompt 對應到 Wave 7，本版 v1 不實作。
