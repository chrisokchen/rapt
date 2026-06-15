# 修復政策（Fix Policy）

本文件定義 `rapt-reconcile` 能自動修復（can-fix）和需要人工決策（need-human）的邊界。

---

## Can-Fix（機械性，可自動修復）

這些修復不需要業務決策，正確值可從其他 SSoT 精確取得。

| 類型 | 說明 | 正確值來源 |
|------|------|----------|
| entity: 大小寫 | haAPI/haPDL entity: 與 DBML Table Name 大小寫不一致 | DBML Table Name（精確值）|
| filter field 大小寫 | haAPI list.filters[].field 與 DBML column 大小寫不一致 | DBML column name（精確值）|
| api: 引用更新 | haPDL api: 值需對應 haAPI logical id | haAPI api: 頂層值（精確值）|
| source_evidence 補全 | haAPI/haPDL source_evidence 遺漏（檔案已存在）| 對應 feature/scenario/table 路徑 |
| schema_version 更新 | 舊版 schema_version 需升級到 3.3 | 固定值 "3.3" |
| permission_ref typo | permission_refs 中 id 拼寫錯誤（haARM 有精確值）| haARM permission.id（精確值）|
| haARM 機械性補全 | haARM resource 缺少但 DBML Table 存在 | DBML Table Name → resource.id |
| traceability L2 補列 | Scenario 缺 L2 列，但 source_evidence / glossary / DBML 已能精確定位 | source_evidence + glossary + DBML |
| CiC 狀態回寫 | discovery 原文件 CiC 未標 RESOLVED，但 decision log 已有對應決策 | `.clarify/decisions/` 決策記錄 ID |
| story-index reference 補齊 | story-index feature/scenario link 缺漏但檔案已存在 | feature/scenario index |
| accepted deferred 註記 | decision 表示 deferred / MVP 外，但 traceability 未標 | decision log |

---

## Need-Human（語意性，需要人工決策）

這些問題需要業務判斷，不能自動修復。

| 類型 | 說明 | 委派對象 |
|------|------|---------|
| 缺少 must-have Feature | Story Index 中 must-have 無 Gherkin Feature | rapt-behavior |
| haAPI 缺少 operation | Gherkin Scenario 無對應 operation（業務需求未映射）| rapt-intent |
| haARM 語意缺口 | resource/role/permission 的業務意義不明 | rapt-clarify（CiC GAP）|
| DBML 欄位語意衝突 | 兩份文件對同欄位有不同描述 | rapt-clarify（CiC CON）|
| 存取控制策略 | 某個 Scenario 需要的 permission 業務規則不清 | rapt-clarify（CiC BDY）|
| deprecated 欄位存在 | `access.permissions:` / `security.permissions:` 存在 | 需人工判斷如何遷移（ASK）|

---

## 禁止（Deny）

`rapt-reconcile` 永遠不可做的事：

- 推斷業務邏輯（如猜測 permission 的適用場景）
- 新增 DBML Table / column（只能修改已有的 case）
- 修改 Gherkin Feature 內容
- 刪除任何 SSoT 欄位（即使疑似錯誤）
- 修改 haARM role / permission 的語意定義
- 自動裁決「阻擋或警示」或其他替代策略
- 自動決定 scope / MVP 邊界
- 以低信心 mapping 補精確 table / field

---

## 修復記錄標準

每次修復必須在 `.raptor/session.md` 記錄：

```
[{datetime}] reconcile: {finding_id} — {type}
  changed: {file}#{path} from "{old}" to "{new}"
  basis: {正確值來源}
```
