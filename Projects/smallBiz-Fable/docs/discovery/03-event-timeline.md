# Event Timeline

> 來源：01-stakeholders.md、02-user-journeys.md、PRD §1-§8
> 方法：Event Storming 輕量版（先廣後收；分群為草圖，Phase 2 才確立 Bounded Context）

## Domain Events（時序排列）

### 開店與商品準備

| # | 事件 | Actor | 前置條件 | 後置狀態 |
|---|------|-------|---------|---------|
| 1 | 商家註冊了帳號 | merchant | — | 商家帳號待開通 |
| 2 | 平台開通了商家店面 | platform-admin | 商家已註冊 | 店面可營運 |
| 3 | 商家建立了商品 | merchant | 店面可營運 | 商品為草稿狀態 |
| 4 | 商家設定了規格組合與 SKU | merchant | 商品已建立 | 每個 SKU 有獨立售價（>0） |
| 5 | 商家上架了商品 | merchant | 商品資料完整 | 商品於前台可見 |
| 6 | 商家設定了 SKU 庫存量 | merchant | SKU 已建立 | 庫存可供扣減 |
| 7 | 商家設定了低庫存水位 | merchant | SKU 已建立 | 低於水位將通知 |
| 8 | 商家下架了商品 | merchant | 商品已上架 | 商品前台不可見 |

### 消費者帳號

| # | 事件 | Actor | 前置條件 | 後置狀態 |
|---|------|-------|---------|---------|
| 9 | 消費者以 Email 註冊了會員 | consumer | Email 未被使用 | 會員待驗證 |
| 10 | 消費者驗證了信箱 | consumer | 已註冊 | 會員生效（初始等級） |
| 11 | 消費者儲存了常用收件地址 | consumer | 會員生效 | 結帳可快選地址 |

### 購物與結帳

| # | 事件 | Actor | 前置條件 | 後置狀態 |
|---|------|-------|---------|---------|
| 12 | 消費者將商品加入了購物車 | consumer | 商品已上架 | 購物車有品項（跨裝置保留） |
| 13 | 消費者調整了購物車數量 | consumer | 購物車有品項 | 數量更新 |
| 14 | 消費者套用了優惠券 | consumer | 券有效＋達最低門檻＋等級符合 | 折扣已計入（一單限一券） |
| 15 | 消費者折抵了點數 | consumer | 點數餘額足夠 | 折抵金額已計入 |
| 16 | 系統計算了訂單金額 | system | 結帳資訊完整 | 含折扣、運費（滿千免運）、5% 稅 |
| 17 | 消費者提交了訂單 | consumer | 金額已確認 | 訂單成立（待付款）、商品快照已存、庫存已扣減 |

### 付款與履約

| # | 事件 | Actor | 前置條件 | 後置狀態 |
|---|------|-------|---------|---------|
| 18 | 消費者完成了付款 | consumer / payment-gateway | 訂單待付款 | 訂單已付款 |
| 19 | 消費者回報了轉帳後五碼 | consumer | 選擇銀行轉帳 | 待商家對帳確認 |
| 20 | 系統開立了發票 | system / einvoice-service | 訂單已付款 | 發票已開立（5% 營業稅） |
| 21 | 商家確認了訂單 | merchant | 訂單已付款 | 訂單已確認 |
| 22 | 商家標記了出貨並填入物流單號 | merchant | 訂單已確認 | 訂單已出貨、可追蹤 |
| 23 | 物流更新了配送狀態 | logistics-provider | 已出貨 | 配送中 → 已送達 |
| 24 | 系統發送了訂單狀態通知 | system / notification-channel | 任一狀態變更 | 消費者收到 LINE/Email |
| 25 | 系統取消了逾時未付款訂單 | system | 待付款逾時（時限未定） | 訂單已取消、庫存釋放 |
| 26 | 消費者取消了訂單 | consumer | 取消條件（未定）成立 | 訂單已取消 |

### 退換貨

| # | 事件 | Actor | 前置條件 | 後置狀態 |
|---|------|-------|---------|---------|
| 27 | 消費者申請了退貨 | consumer | 訂單已送達＋期限內（天數未定） | 退貨申請待審核 |
| 28 | 商家審核了退貨申請 | merchant | 申請待審核 | 核准（安排取件）或拒絕 |
| 29 | 物流取回了退貨商品 | logistics-provider | 退貨已核准 | 商品退回中 |
| 30 | 商家確認了退回商品 | merchant | 商品已退回 | 可執行退款 |
| 31 | 系統執行了退款 | system / payment-gateway | 退回已確認 | 訂單已退款 |

### 會員忠誠

| # | 事件 | Actor | 前置條件 | 後置狀態 |
|---|------|-------|---------|---------|
| 32 | 系統發給了消費點數 | system | 訂單完成（100 元 1 點） | 點數餘額增加 |
| 33 | 系統調整了會員等級 | system | 分級規則（未定）達成 | 等級升/降 |

### 促銷管理

| # | 事件 | Actor | 前置條件 | 後置狀態 |
|---|------|-------|---------|---------|
| 34 | 商家/行銷建立了促銷活動 | merchant / platform-marketer | 店面可營運 | 活動已排程（檔期） |
| 35 | 系統自動上架了到檔期的活動 | system | 檔期開始 | 活動生效 |
| 36 | 系統自動下架了過期的活動 | system | 檔期結束 | 活動失效 |
| 37 | 商家/行銷發行了優惠券 | merchant / platform-marketer | 店面可營運 | 券可被領用（門檻/張數上限/效期/等級限定） |

### 庫存與報表

| # | 事件 | Actor | 前置條件 | 後置狀態 |
|---|------|-------|---------|---------|
| 38 | 系統扣減了庫存 | system | 訂單成立（見 CiC GAP #006） | SKU 庫存減少 |
| 39 | 系統通知了商家補貨 | system | 庫存低於自訂水位 | 商家收到提醒 |
| 40 | 商家查看了銷售報表 | merchant | 有交易資料 | （讀取，無狀態變更） |

## Commands

| Command（現在式） | 觸發的 Event | Actor |
|------------------|------------|-------|
| 註冊商家帳號 | #1 | merchant |
| 開通商家店面 | #2 | platform-admin |
| 建立商品 / 設定 SKU / 上架 / 下架 | #3 #4 #5 #8 | merchant |
| 設定庫存 / 低水位 | #6 #7 | merchant |
| 註冊會員 / 驗證信箱 / 存地址 | #9 #10 #11 | consumer |
| 加入購物車 / 調整數量 | #12 #13 | consumer |
| 套用優惠券 / 折抵點數 | #14 #15 | consumer |
| 提交訂單 | #16 #17 #38 | consumer |
| 付款 / 回報後五碼 | #18 #19 | consumer |
| 確認訂單 / 標記出貨 | #21 #22 | merchant |
| 取消訂單 | #26 | consumer |
| 申請退貨 / 審核退貨 / 確認退回 | #27 #28 #30 | consumer / merchant |
| 建立促銷活動 / 發行優惠券 | #34 #37 | merchant, platform-marketer |

## 初步 Bounded Context 分群（草圖）

### Store & Merchant（商家與店面）
- Events: [#1, #2]
- 可能的 Aggregate: Merchant, Store

### Catalog（商品目錄）
- Events: [#3, #4, #5, #8]
- 可能的 Aggregate: Product, SKU(Variant), Category

### Inventory（庫存）
- Events: [#6, #7, #38, #39]
- 可能的 Aggregate: StockItem

### Shopping（購物車與結帳）
- Events: [#12, #13, #14, #15, #16]
- 可能的 Aggregate: Cart

### Order（訂單）
- Events: [#17, #21, #25, #26]
- 可能的 Aggregate: Order, OrderItem（含商品快照）

### Payment & Invoice（付款與發票）
- Events: [#18, #19, #20, #31]
- 可能的 Aggregate: Payment, Invoice

### Fulfillment（物流履約）
- Events: [#22, #23]
- 可能的 Aggregate: Shipment

### Returns（退換貨）
- Events: [#27, #28, #29, #30]
- 可能的 Aggregate: ReturnRequest

### Membership & Loyalty（會員與忠誠）
- Events: [#9, #10, #11, #32, #33]
- 可能的 Aggregate: Member, PointLedger, MemberTier

### Promotion（促銷）
- Events: [#34, #35, #36, #37, #14]
- 可能的 Aggregate: Campaign, Coupon

### Notification（通知）
- Events: [#24]
- 可能的 Aggregate: NotificationLog

### Reporting（報表）
- Events: [#40]
- 可能的 Aggregate: （讀模型，無聚合）

## CiC 便條

<!-- CiC GAP #006 -->
**類型**：GAP
**位置**：docs/discovery/03-event-timeline.md#38
**描述**：庫存扣減時點未定（PRD 2.3 標高）：「下單當下」或「付款完成」扣減？是否需「預留」概念與釋放時限？同時影響事件 #17 / #25 的後置狀態。
**影響**：Inventory 與 Order context 的核心不變式、超賣防護設計（雙邊最高優先痛點）
**推薦**：clarify 高優先；建議方案「下單即預留＋逾時釋放」供業主決策
<!-- /CiC -->

<!-- CiC GAP #007 -->
**類型**：GAP
**位置**：docs/discovery/03-event-timeline.md#16
**描述**：事件 #16 金額計算的內部順序未定（PRD 6.4 標高）：活動價、優惠券、會員折扣、點數折抵的疊加與計算順序；稅基口徑（PRD 3.5）亦未定。唯一共識：一單一券。
**影響**：Order 金額計算邏輯、Promotion context、發票稅額
**推薦**：clarify 高優先；需逐條白紙黑字定義（林經理訪談）
<!-- /CiC -->

<!-- CiC ASM #008 -->
**類型**：ASM
**位置**：docs/discovery/03-event-timeline.md#21
**描述**：假設「已付款 → 已確認」為商家手動確認動作（PRD 4.2 只列狀態未列觸發者）。轉帳對帳（#19）後的狀態流轉亦為推測。
**影響**：Order 狀態機、商家後台操作流程
**推薦**：clarify 確認訂單狀態機的觸發者與自動/手動邊界
<!-- /CiC -->

## CiC 狀態同步（Phase 3 Clarification，2026-06-13）

- **GAP #006 → RESOLVED**（CLR-260613-01#Q1）：下單即預留＋逾時釋放；付款期限 72h；StockItem 加 reservedQuantity（CON-STK-001/003, CON-ORD-002）。事件 #38 扣減語意改為「下單預留、付款轉扣」。
- **GAP #007 → RESOLVED**（CLR-260613-01#Q2）：事件 #16 金額計算順序＝活動→券→點數→運費→稅；稅基折後不含運（CON-ORD-006/008）。
- **ASM #008 → RESOLVED / CONFIRMED**（CLR-260613-03#ASM#008）：狀態機觸發者邊界確認（CON-ORD-001）。
