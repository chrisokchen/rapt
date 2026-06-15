# E-Commerce Minimal — 測試輸入（Before）

本文件是 rapt-* skill 家族的最小電商場景測試輸入。
用於驗證完整的 Phase 1 → Phase 5 流程是否正常運作。

---

## 背景

一個簡單的 B2C 電商系統，支援客戶購物和基本訂單管理。

## 關鍵 Stakeholders

- **客戶（Customer）**：瀏覽商品、下訂單、申請退款
- **店員（Staff）**：管理訂單、處理退款申請
- **管理員（Admin）**：系統管理、全數據存取

## 業務事件（初步識別）

1. 客戶將商品加入購物車
2. 客戶結帳並產生訂單
3. 系統通知付款完成
4. 店員備貨並出貨
5. 客戶申請退款
6. 店員審核退款申請

## 初步資料識別

- 商品（Product）：品名、價格、庫存
- 訂單（Order）：訂單編號、客戶、狀態、總金額
- 訂單明細（OrderItem）：商品、數量、單價
- 退款申請（RefundRequest）：申請原因、申請金額、狀態

## 初步業務規則（模糊，待釐清）

- 折扣：不確定是訂單層或商品明細層
- 退款審核：不確定是誰有資格審核
- 庫存扣減：不確定在哪個時間點觸發

## 已知限制

- 不包含商品搜尋功能（scope out）
- 不包含物流追蹤（scope out）
- 僅支援台灣本地（scope boundary）

---

## 使用說明

1. 使用 `/rapt-kickoff` 初始化專案
2. 提供此文件內容作為業務描述輸入
3. 依序執行各 Phase：discovery → behavior → modeling → clarify → intent → verify
4. 預期產出結構：

```
.raptor/
  arguments.yml
  session.md
discovery/
  01-stakeholders.md
  02-story-index.md
  03-ubiquitous-language.md
  04-vision-kpi.md
high-gherkin/
  product.feature
  order.feature
  refund.feature
schema/
  ecommerce.dbml
access-control/
  ecommerce.haarm.yaml
backend-intent/
  product.haapi.yaml
  order.haapi.yaml
  refund-request.haapi.yaml
frontend-intent/
  product-list.hapdl.yaml
  order-list.hapdl.yaml
  order-form.hapdl.yaml
  refund-form.hapdl.yaml
reports/
  verify-report.md
```
