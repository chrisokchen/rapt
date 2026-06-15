# 高階 Gherkin 規則（High-Level Gherkin Rules）

本文件定義 RAPTor Phase 1.5 高階 Gherkin feature files 的**強制規則**與**反模式**。

`rapt-behavior` 和 `rapt-form-gherkin` 都必須遵守。

---

## 核心原則

高階 Gherkin 是**業務規格（SSoT）**，不是測試執行腳本。

```
高階 Gherkin 語言層級 = 業務行為
Low-level Gherkin 語言層級 = E2E 測試執行（含 selector / URL）
                  → 是 generated artifact，不在本 skill 範圍
```

---

## 強制規則

### 語彙層級規則（MUST）

| 規則 | 正確範例 | 錯誤範例 |
|------|---------|---------|
| 只用業務語言 | `When 客戶提交訂單` | `When 客戶點擊「送出」按鈕` |
| 只描述業務結果 | `Then 訂單狀態變為「待出貨」` | `Then 系統呼叫 POST /orders 回傳 201` |
| 不含 UI 元素 | `When 管理員審核退款申請` | `When 管理員在退款頁面填寫拒絕原因` |
| 不含 URL / API | `When 系統發送確認通知` | `When 系統呼叫 /api/v2/notify` |
| 不含 DB / 技術棧 | `Given 商品已上架` | `Given 商品 status='Y' 存在 DB` |

### 結構規則（MUST）

| 規則 | 說明 |
|------|------|
| Feature 有 3-row header | `Feature + In order to + As a + I want to` |
| 每個 Scenario 有 G-W-T | Given → When → Then 完整三段 |
| When 只有一個業務動作 | 多個動作拆成多個 Scenario |
| Background 只放角色和系統前提 | 不放特定業務資料 |
| source_evidence 有 Feature comment | 每個 Feature 頂部有 `# source: <ref>` |
| Then 只有單一可驗證結果 | 不用「或」連接兩種系統行為；未裁決時記 CiC `CON` |
| 資料依賴 Scenario 有本地 Given | Background 不取代特定測試資料或業務狀態 |
| 資料變更 / 授權 / 狀態轉換 Scenario 有 `# entities:` | 使用業務語言標註主要實體，供 traceability L2 精確化 |

### 術語一致性規則（MUST）

- Feature 中使用的業務術語必須與 `01-stakeholders.md` 和 `03-event-timeline.md` 一致
- actor 名稱引用 `stakeholders.md` 中的 `name`（非 `id`）
- 業務物件名稱（如「訂單」「客戶」）保持一致，不混用同義詞

---

## 反模式（lint 檢查項）

| 反模式 | 說明 | 嚴重度 |
|--------|------|-------|
| AP-G01 | `When` 步驟含 click / button / 點擊 / 按鈕 | ERROR |
| AP-G02 | `When` 步驟含 URL / api / http / POST / GET | ERROR |
| AP-G03 | `Then` 步驟含 status code / HTTP / response body | ERROR |
| AP-G04 | `Then` 步驟含 SQL / database / DB / Redis / Queue | ERROR |
| AP-G05 | `When` 有多個 `And`（>2 個動作） | WARNING |
| AP-G06 | Scenario 無 `Given` 段 | WARNING |
| AP-G07 | Feature 無 source_evidence comment | WARNING |
| AP-G08 | 同義詞不一致（如「用戶」vs「客戶」） | WARNING |
| AP-G09 | Then 含「或」「或者」「阻擋或警示」「拒絕或要求」等替代策略 | ERROR |
| AP-G10 | 資料依賴 Scenario 沒有本地 Given | WARNING |
| AP-G11 | 資料變更 / 授權 / 狀態轉換 Scenario 缺 `# entities:` | WARNING |
| AP-G12 | 資料變更型 Feature 無任何負向 Scenario | WARNING |
| AP-G13 | Then 只寫「處理成功」但無可觀察業務結果 | WARNING |

---

## 正確範例

```gherkin
# source: docs/01-discovery/02-user-journeys.md#customer-checkout
# stories: US-001
Feature: 訂單結帳
  In order to 完成購物並取得訂單確認
  As a 客戶
  I want to 提交訂單並完成付款

  Background:
    Given 我已登入為客戶
    And 購物車中有至少一件商品

  # scenario_id: SCN-ORDER-001
  # entities: 訂單, 客戶
  Scenario: 成功提交訂單
    Given 客戶確認收件地址
    When 客戶提交訂單
    Then 系統建立一筆新訂單
    And 客戶收到訂單確認通知

  Scenario: 付款失敗時保留訂單
    Given 客戶已提交訂單
    When 付款失敗
    Then 訂單保持「待付款」狀態
    And 系統通知客戶重試付款
```

---

## 錯誤範例

```gherkin
# ❌ 錯誤：含 UI 操作、API 路由、技術細節
Scenario: 客戶結帳
  Given 我在 /cart 頁面
  When 我點擊「結帳」按鈕
  And 我填寫表單並按「送出」
  Then 系統呼叫 POST /api/orders 並回傳 201
  And 資料庫寫入 orders 資料表
```
