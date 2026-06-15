# Cross-Cutting Scenario Checklist

本規則用於 `rapt-behavior` 將 discovery scope 轉成 Gherkin 前，掃描跨模組共通能力，避免範圍已明列但沒有 Scenario 或延期記錄。

## 掃描項目

若 discovery、scope、KPI、NFR 或管理能力列表提到以下能力，必須在 `story-index.md` 的 Cross-Cutting Capability Matrix 中記錄承接方式：

- 匯入
- 匯出
- 篩選
- 排序
- 分頁
- 批次處理
- 錯誤格式
- 授權不足
- 部分成功 / 部分失敗
- 稽核記錄
- 清理 / 保留政策

## 承接方式

| handling | 說明 |
|---|---|
| `scenario` | 已展開為 Gherkin Scenario。 |
| `common-dsl` | 由共通規格或非功能規格承接。 |
| `deferred` | 延後，需有 decision reference。 |
| `out-of-scope` | 明確列為範圍外，需有理由。 |
| `open-cic` | 尚未決定，需建立 CiC。 |

## Matrix 格式

```markdown
## Cross-Cutting Capability Matrix

| module | capability | handling | feature/scenario | decision_ref | notes |
|---|---|---|---|---|---|
| 使用者管理 | 匯出 | scenario | user-management.feature#匯出使用者清單套用篩選條件 |  |  |
| 稽核管理 | 清理 | deferred |  | CLR-260609-01#Q4 | MVP 外 |
```

## 規則

- 不能只在 scope 提到能力而不在 matrix 中記錄。
- `deferred` 必須有 decision reference 或 OPEN CiC。
- `scenario` 必須能連到具體 Feature / Scenario。
