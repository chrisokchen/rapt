# 可追溯性矩陣模板

> **階段**: Phase 5 - 驗證確認
> **目的**: 建立需求與規格之間的雙向追溯關係,確保完整涵蓋與一致性
> **產出**: 可追溯性矩陣、缺口分析報告

---

## 專案資訊

| 項目 | 內容 |
|------|------|
| **專案名稱** | [專案名稱] |
| **建立日期** | YYYY-MM-DD |
| **維護者** | [姓名] |
| **最後更新** | YYYY-MM-DD |

---

## 可追溯性矩陣說明

### 追溯方向

1. **前向追溯 (Forward Traceability)**: 需求 → 設計 → 實作 → 測試
   - 確保每個需求都有對應的實作與測試

2. **後向追溯 (Backward Traceability)**: 測試 → 實作 → 設計 → 需求
   - 確保所有實作都源自明確的需求

### 符號說明

- ✅ **完整**: 已完成且經過驗證
- ⚠️ **部分完成**: 僅部分實作或測試
- ❌ **缺失**: 尚未實作或測試
- 🔄 **進行中**: 正在開發或測試
- 🔗 **相關**: 有間接關聯

---

## 矩陣 1: 需求 → BDD Scenario

| 需求 ID | 需求描述 | BDD Feature | BDD Scenario | 涵蓋狀態 | 備註 |
|---------|---------|-------------|--------------|---------|------|
| REQ-001 | 使用者登入功能 | user-login.feature | 使用有效憑證成功登入<br>使用無效密碼登入失敗<br>帳號被鎖定時無法登入 | ✅ 完整 | 涵蓋正常流程與異常處理 |
| REQ-002 | 商品瀏覽功能 | product-browsing.feature | 瀏覽商品列表<br>搜尋商品<br>依分類篩選商品 | ✅ 完整 | - |
| REQ-003 | 購物車管理 | shopping-cart.feature | 加入商品到購物車<br>更新購物車數量<br>移除購物車品項 | ⚠️ 部分完成 | 缺少購物車持久化場景 |
| REQ-004 | 訂單結帳 | order-checkout.feature | 基本結帳流程<br>使用優惠券<br>使用忠誠點數 | 🔄 進行中 | 測試中 |
| REQ-005 | 庫存管理 | inventory-management.feature | 查看庫存狀態<br>調整庫存數量 | ❌ 缺失 | 尚未撰寫 BDD 場景 |

### 缺口分析

**完全缺失的 BDD 場景**:
- [ ] REQ-005: 庫存管理 - 需補充完整的 BDD 場景

**部分涵蓋的需求**:
- [ ] REQ-003: 購物車管理 - 需補充購物車持久化場景

---

## 矩陣 2: BDD Scenario → API 規格

| BDD Feature | BDD Scenario | API 端點 | HTTP 方法 | 狀態 | 備註 |
|-------------|--------------|----------|-----------|------|------|
| user-login.feature | 使用有效憑證成功登入 | POST /auth/login | POST | ✅ 完整 | - |
| user-login.feature | 使用無效密碼登入失敗 | POST /auth/login | POST | ✅ 完整 | 包含錯誤回應 |
| product-browsing.feature | 瀏覽商品列表 | GET /products | GET | ✅ 完整 | 支援分頁與篩選 |
| product-browsing.feature | 搜尋商品 | GET /products?search={keyword} | GET | ✅ 完整 | - |
| shopping-cart.feature | 加入商品到購物車 | POST /cart/items | POST | ✅ 完整 | - |
| shopping-cart.feature | 更新購物車數量 | PATCH /cart/items/{id} | PATCH | ✅ 完整 | - |
| shopping-cart.feature | 移除購物車品項 | DELETE /cart/items/{id} | DELETE | ✅ 完整 | - |
| order-checkout.feature | 基本結帳流程 | POST /orders | POST | 🔄 進行中 | API 規格已定義,待實作 |
| order-checkout.feature | 使用優惠券 | POST /coupons/apply | POST | ⚠️ 部分完成 | 缺少驗證邏輯 |
| inventory-management.feature | 查看庫存狀態 | GET /inventory | GET | ❌ 缺失 | 尚未定義 API |

### 缺口分析

**缺失的 API 端點**:
- [ ] GET /inventory - 查看庫存狀態
- [ ] PATCH /inventory/{id} - 調整庫存數量

**需要改進的 API**:
- [ ] POST /coupons/apply - 補充完整的驗證邏輯規格

---

## 矩陣 3: haARM Permission → API 端點 → BDD Scenario

| haARM Permission | API 端點 | BDD Positive | BDD Negative | 涵蓋狀態 | 備註 |
|-----------------|---------|-------------|-------------|---------|------|
| user_read | GET /api/users | 管理員可查看使用者列表 | 客戶不能查看使用者列表 | ✅ 完整 | — |
| order_view_own | GET /api/orders?owner=me | 客戶查看自己的訂單 | — | ⚠️ 缺少 Negative | 需補充非擁有者存取被拒的場景 |

### 缺口分析

**缺少 BDD 場景的權限**:
- [ ] [permission_id]: [說明]

**缺少 Negative 測試的權限**:
- [ ] [permission_id]: 有 Positive 場景但缺少 403 被拒的場景

---

## 矩陣 4: API 規格 → UI 頁面

| API 端點 | API 用途 | UI 頁面 | 頁面規格檔案 | 狀態 | 備註 |
|----------|---------|---------|-------------|------|------|
| POST /auth/login | 使用者登入 | 登入頁 | login.rui.yaml | ✅ 完整 | - |
| GET /products | 列出商品 | 商品列表頁 | product-list.rui.yaml | ✅ 完整 | 包含搜尋與篩選 |
| GET /products/{id} | 商品詳情 | 商品詳情頁 | product-detail.rui.yaml | ⚠️ 部分完成 | 缺少評價區塊 |
| GET /cart | 取得購物車 | 購物車頁 | shopping-cart.rui.yaml | ✅ 完整 | - |
| POST /cart/items | 加入購物車 | 商品列表頁<br>商品詳情頁 | product-list.rui.yaml<br>product-detail.rui.yaml | ✅ 完整 | - |
| POST /orders | 建立訂單 | 結帳頁 | checkout.rui.yaml | 🔄 進行中 | 規格已定義,待實作 |
| GET /orders | 列出訂單 | 訂單列表頁 | order-list.rui.yaml | ❌ 缺失 | 尚未定義頁面規格 |
| GET /orders/{id} | 訂單詳情 | 訂單詳情頁 | order-detail.rui.yaml | ❌ 缺失 | 尚未定義頁面規格 |

### 缺口分析

**缺失的 UI 頁面規格**:
- [ ] order-list.rui.yaml - 訂單列表頁
- [ ] order-detail.rui.yaml - 訂單詳情頁
- [ ] inventory-management.rui.yaml - 庫存管理頁 (後台)

**需要補充的 UI 功能**:
- [ ] product-detail.rui.yaml - 補充商品評價區塊

---

## 矩陣 5: UI 頁面 → 使用者故事

| UI 頁面 | 頁面功能 | 使用者故事 | User Journey 階段 | 狀態 | 備註 |
|---------|---------|-----------|------------------|------|------|
| login.rui.yaml | 使用者登入 | US-001: 作為註冊使用者,我想要登入系統 | 認證 | ✅ 完整 | - |
| product-list.rui.yaml | 瀏覽商品 | US-002: 作為消費者,我想要瀏覽商品 | 發現商品 | ✅ 完整 | - |
| product-list.rui.yaml | 搜尋商品 | US-003: 作為消費者,我想要搜尋商品 | 發現商品 | ✅ 完整 | - |
| product-detail.rui.yaml | 查看商品詳情 | US-004: 作為消費者,我想要查看商品詳情 | 評估商品 | ⚠️ 部分完成 | 缺少評價功能 |
| shopping-cart.rui.yaml | 管理購物車 | US-005: 作為消費者,我想要管理購物車 | 決策購買 | ✅ 完整 | - |
| checkout.rui.yaml | 結帳付款 | US-006: 作為消費者,我想要完成結帳 | 結帳流程 | 🔄 進行中 | - |
| - | 追蹤訂單 | US-007: 作為消費者,我想要追蹤訂單狀態 | 訂單追蹤 | ❌ 缺失 | 缺少對應頁面 |

### 缺口分析

**未實現的使用者故事**:
- [ ] US-007: 追蹤訂單狀態 - 需建立訂單追蹤頁面

---

## 矩陣 5: BDD Scenario → 測試實作

| BDD Feature | BDD Scenario | 測試類型 | 測試檔案 | 測試狀態 | 涵蓋率 |
|-------------|--------------|---------|---------|---------|--------|
| user-login.feature | 使用有效憑證成功登入 | E2E | e2e/auth/login.spec.ts | ✅ 通過 | 100% |
| user-login.feature | 使用無效密碼登入失敗 | E2E | e2e/auth/login.spec.ts | ✅ 通過 | 100% |
| user-login.feature | 帳號被鎖定時無法登入 | E2E | e2e/auth/login.spec.ts | ✅ 通過 | 100% |
| product-browsing.feature | 瀏覽商品列表 | E2E | e2e/product/list.spec.ts | ✅ 通過 | 100% |
| shopping-cart.feature | 加入商品到購物車 | E2E | e2e/cart/add-item.spec.ts | ✅ 通過 | 100% |
| shopping-cart.feature | 更新購物車數量 | E2E | e2e/cart/update-item.spec.ts | ⚠️ 失敗 | 80% |
| shopping-cart.feature | 超過庫存數量 | E2E | e2e/cart/update-item.spec.ts | ❌ 未實作 | 0% |
| order-checkout.feature | 基本結帳流程 | E2E | e2e/order/checkout.spec.ts | 🔄 進行中 | 60% |

### 缺口分析

**失敗的測試**:
- [ ] e2e/cart/update-item.spec.ts::更新購物車數量 - 修復邊界條件測試

**未實作的測試**:
- [ ] e2e/cart/update-item.spec.ts::超過庫存數量 - 需補充測試案例

---

## 矩陣 6: API 規格 → 資料模型

| API 端點 | 使用的資料模型 | DBML 定義 | 欄位完整性 | 狀態 | 備註 |
|----------|--------------|----------|-----------|------|------|
| POST /auth/login | User | users 表 | ✅ 完整 | ✅ 一致 | - |
| GET /products | Product, Category | products 表, categories 表 | ✅ 完整 | ✅ 一致 | - |
| GET /products/{id} | Product, ProductVariant, Inventory | products 表, product_variants 表, inventory 表 | ✅ 完整 | ✅ 一致 | - |
| POST /orders | Order, OrderItem, Payment | orders 表, order_items 表, payments 表 | ⚠️ 部分完成 | ⚠️ 不一致 | payments 表缺少 transaction_id 欄位 |
| POST /coupons/apply | Coupon, CouponUsage | coupons 表, coupon_usage 表 | ✅ 完整 | ✅ 一致 | - |

### 缺口分析

**資料模型不一致**:
- [ ] payments 表 - 需補充 transaction_id 欄位以支援第三方支付追蹤

---

## 矩陣 7: 業務規則 → 實作驗證

| 規則 ID | 業務規則 | BDD Scenario | 單元測試 | 整合測試 | 狀態 | 備註 |
|---------|---------|-------------|---------|---------|------|------|
| BR-ORD-001 | 訂單金額計算 | order-checkout.feature::訂單金額計算 | test_order_amount_calculation() | ✅ | ✅ 完整 | - |
| BR-ORD-002 | 運費計算 | order-checkout.feature::運費計算 | test_shipping_fee_calculation() | ✅ | ✅ 完整 | - |
| BR-ORD-003 | 訂單取消 | order-management.feature::訂單取消 | test_order_cancellation() | 🔄 | ⚠️ 部分完成 | 缺少退款流程測試 |
| BR-INV-001 | 可售庫存計算 | inventory-management.feature::庫存計算 | test_available_inventory() | ✅ | ✅ 完整 | - |
| BR-INV-002 | 庫存預留 | inventory-management.feature::庫存預留 | test_inventory_reservation() | ❌ | ❌ 缺失 | 尚未撰寫測試 |
| BR-PRM-001 | 優惠券折扣 | promotion-management.feature::優惠券 | test_coupon_discount() | ✅ | ⚠️ 部分完成 | 缺少疊加規則測試 |

### 缺口分析

**缺失的測試**:
- [ ] BR-INV-002: 庫存預留規則 - 需補充單元測試與整合測試

**需要補充的測試**:
- [ ] BR-ORD-003: 訂單取消規則 - 補充退款流程整合測試
- [ ] BR-PRM-001: 優惠券折扣規則 - 補充折扣疊加規則測試

---

## 總體涵蓋率統計

### 需求涵蓋率

| 分類 | 總數 | 已完成 | 進行中 | 未開始 | 涵蓋率 |
|------|------|--------|--------|--------|--------|
| 使用者故事 | 10 | 6 | 2 | 2 | 60% |
| BDD Scenario | 25 | 18 | 4 | 3 | 72% |
| API 端點 | 20 | 15 | 3 | 2 | 75% |
| UI 頁面 | 12 | 7 | 2 | 3 | 58% |
| 業務規則 | 15 | 10 | 2 | 3 | 67% |
| 測試案例 | 30 | 22 | 5 | 3 | 73% |

### 涵蓋率趨勢圖

```
涵蓋率 (%)
100 |
 90 |
 80 |                     ●
 70 |         ● ●   ●       ●
 60 |     ●               ●
 50 |
    +--------------------------------
      US  BDD API  UI  BR  Test
```

---

## 缺口總覽與行動計畫

### 優先級 P0 (必須完成)

1. **REQ-005: 庫存管理**
   - [ ] 撰寫 BDD Feature 與 Scenarios
   - [ ] 定義 API 規格
   - [ ] 建立 UI 頁面規格
   - [ ] 實作測試案例
   - **負責人**: [姓名]
   - **預計完成**: YYYY-MM-DD

2. **BR-INV-002: 庫存預留規則**
   - [ ] 實作單元測試
   - [ ] 實作整合測試
   - [ ] 驗證併發場景
   - **負責人**: [姓名]
   - **預計完成**: YYYY-MM-DD

### 優先級 P1 (短期完成)

1. **訂單管理頁面**
   - [ ] 建立 order-list.rui.yaml
   - [ ] 建立 order-detail.rui.yaml
   - [ ] 實作對應 API
   - **負責人**: [姓名]
   - **預計完成**: YYYY-MM-DD

2. **補充測試涵蓋率**
   - [ ] 購物車持久化測試
   - [ ] 訂單取消退款流程測試
   - [ ] 優惠券疊加規則測試
   - **負責人**: [姓名]
   - **預計完成**: YYYY-MM-DD

### 優先級 P2 (中期規劃)

1. **商品評價功能**
   - [ ] 補充使用者故事
   - [ ] 撰寫 BDD Scenarios
   - [ ] 擴展 product-detail.rui.yaml
   - **負責人**: [姓名]
   - **預計完成**: YYYY-MM-DD

---

## 檢查清單

### 追溯完整性
- [ ] 所有需求都有對應的 BDD Scenario
- [ ] 所有 BDD Scenario 都有對應的 API 規格
- [ ] 所有 API 都有對應的 UI 頁面或系統流程
- [ ] 所有業務規則都有對應的測試驗證

### 雙向追溯
- [ ] 所有測試都可追溯到需求
- [ ] 所有實作都可追溯到需求
- [ ] 沒有「孤兒」需求 (無實作)
- [ ] 沒有「孤兒」實作 (無需求)

### 一致性檢查
- [ ] API 規格與資料模型一致
- [ ] UI 頁面與 API 端點一致
- [ ] BDD Scenario 與 API 行為一致
- [ ] 測試案例與業務規則一致

---

**維護指南**:

1. **定期更新**: 每個 Sprint 結束後更新矩陣
2. **自動化檢查**: 使用腳本自動檢測缺口
3. **團隊協作**: 由 QA、開發、產品經理共同維護
4. **版本控制**: 矩陣檔案納入 Git 版本控制
5. **持續改進**: 基於發現的缺口調整開發優先級

**最佳實踐**:
- 使用工具輔助追溯 (如: Jira, Azure DevOps)
- 建立自動化檢查腳本驗證一致性
- 在 Code Review 時檢查追溯性
- 定期召開追溯性審查會議
