# Test Readiness Gherkin Rules

本規則補強高階 Gherkin 的可驗證性，但不要求高階 Gherkin 變成低階 E2E 腳本。

## MUST

- Then 必須描述唯一且可觀察的業務結果。
- Then 不得使用「阻擋或警示」「拒絕或要求先清除」等替代策略。
- 資料依賴 Scenario 必須有本地 Given；Background 只放角色與全域前提。
- 資料變更、授權、狀態轉換 Scenario 必須有 `# entities:`。
- 建立、修改、刪除、匯入、批次操作至少要有拒絕、失敗或部分失敗情境；不適用需在 story-index matrix 註明。

## SHOULD

- 可用 `Examples` 表達核心邊界值。
- 可用 `# constraints:` 引用已知業務約束，但不得直接寫 SQL 或 DB 欄位斷言。

## 反模式

| 反模式 | 說明 | 嚴重度 |
|---|---|---|
| AP-G09 | Then 含「或」「或者」「阻擋或警示」「拒絕或要求」等替代策略 | ERROR |
| AP-G10 | 資料依賴 Scenario 沒有本地 Given | WARNING |
| AP-G11 | 資料變更 / 授權 / 狀態轉換 Scenario 缺 `# entities:` | WARNING |
| AP-G12 | 資料變更型 Feature 無任何負向 Scenario | WARNING |
| AP-G13 | Then 只寫「處理成功」但無可觀察業務結果 | WARNING |
