# SmallBiz 電商管理 UI Design Brief

> **Purpose**: This document is a structured design brief auto-generated from
> `haPDL` (page intent specs) + `schema.dbml` (data model) + `haARM` (access control).
> Feed this entire document to **Claude Design** or any AI design tool to generate
> Hi-Fi mockups, HTML, or React component code.
>
> **System**: SmallBiz B2C 電商管理系統，支援商品、庫存、購物車、結帳、訂單、會員、促銷、退貨退款與商家報表。
> **Language**: Traditional Chinese (zh-TW)
> **Target framework**: React + Ant Design (or shadcn/ui)

---


## Design System

> Use this as the global design language for all pages.

### Color Palette

| Token | Value | Usage |
|:---|:---|:---|
| `--primary` | `#2563eb` (Blue 600) | Primary buttons, links, active states |
| `--primary-hover` | `#1d4ed8` (Blue 700) | Hover state |
| `--success` | `#16a34a` (Green 600) | Approve actions, success states |
| `--danger` | `#dc2626` (Red 600) | Delete, reject actions |
| `--warning` | `#d97706` (Amber 600) | Warnings, adjust actions |
| `--bg-page` | `#f8fafc` (Slate 50) | Page background |
| `--bg-card` | `#ffffff` | Card/panel backgrounds |
| `--bg-header` | `#1e293b` (Slate 800) | Top navigation / sidebar |
| `--border` | `#e2e8f0` (Slate 200) | Borders, dividers |
| `--text-primary` | `#0f172a` (Slate 900) | Headings, labels |
| `--text-secondary` | `#64748b` (Slate 500) | Descriptions, hints |
| `--badge-blue` | `#dbeafe` bg / `#1e40af` text | Status badges (info) |
| `--badge-green` | `#dcfce7` bg / `#166534` text | Status badges (success) |
| `--badge-amber` | `#fef3c7` bg / `#92400e` text | Status badges (warning) |
| `--badge-red` | `#fee2e2` bg / `#991b1b` text | Status badges (danger) |
| `--badge-gray` | `#f1f5f9` bg / `#475569` text | Status badges (neutral) |

### Typography

| Element | Font | Size | Weight |
|:---|:---|:---|:---|
| Page title | Noto Sans TC | 20px | 700 |
| Section heading | Noto Sans TC | 16px | 600 |
| Table header | Noto Sans TC | 13px | 600 |
| Body text | Noto Sans TC | 14px | 400 |
| Label | Noto Sans TC | 13px | 600 |
| Badge | JetBrains Mono | 12px | 500 |
| Button | Noto Sans TC | 14px | 500 |
| Hint/caption | Noto Sans TC | 12px | 400 |

### Spacing

| Token | Value |
|:---|:---|
| Page padding | 24px |
| Card padding | 20px |
| Form field gap | 16px |
| Table cell padding | 12px 16px |
| Button padding | 8px 20px |
| Border radius (card) | 8px |
| Border radius (button) | 6px |
| Border radius (input) | 6px |
| Border radius (badge) | 4px |

### Component Library (reference)

Use **Ant Design** or **shadcn/ui** component patterns:
- Table: sortable headers, row hover, row actions menu
- Form: label-left layout (label 120px, input flex-1), validation messages
- Select: searchable dropdown with Chinese labels
- DatePicker: range selector for date fields
- Badge: colored status badge with icon
- Button: primary / secondary / ghost / danger variants
- Modal: confirmation dialogs for destructive actions
- Breadcrumb: for navigation context
- Sidebar: collapsible left navigation

### Layout Structure

```
+------------------------------------------+
| Top Nav (dark bg, logo, user menu)       |
+--------+---------------------------------+
| Side   | Breadcrumb                      |
| Nav    +---+-----------------------------+
|        |   | Page Title        [Actions]  |
|        |   +-+---------------------------+
|        |   | | Filter Bar                 |
|        |   | +---------------------------+
|        |   | | Content (Table/Form/Detail)|
|        |   | +---------------------------+
|        |   | | Pagination / Footer        |
+--------+---+-----------------------------+
```

## Page Navigation Map

```
Sidebar Navigation:

  [cart-checkout]
    · 購物車結帳
  [sales-order]
    ☰ 我的訂單
    ☰ 商家訂單管理
  [inventory]
    · 庫存控管
  [member-account]
    ✏ 會員註冊
  [product-catalog]
    ☰ 商家商品管理
    ☰ 商品瀏覽
  [merchant-report]
    · 商家營運報表
  [platform-admin]
    · 平台權限邊界
  [promotion-coupon]
    ☰ 促銷與優惠券管理
  [return-refund]
    ☰ 退貨退款處理
```

### Page Flow

```
我的訂單 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

商家訂單管理 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

商家商品管理 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

促銷與優惠券管理 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

商品瀏覽 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

退貨退款處理 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

會員註冊 (form)
  └── [送出/核准] → back to list

```

## Page Specifications

### Page 1: 購物車結帳

| Property | Value |
|:---|:---|
| Page ID | `consumer-cart-checkout` |
| Type | **WIZARD** |
| Entity | `Cart` |
| Primary Actor |  |
| Allowed Roles |  |
| Source | `consumer-cart-checkout.hapdl.yaml` |


---

### Page 2: 我的訂單

| Property | Value |
|:---|:---|
| Page ID | `consumer-order-history` |
| Type | **LIST** |
| Entity | `SalesOrder` |
| Primary Actor |  |
| Allowed Roles |  |
| Source | `consumer-order-history.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `consumerId` | 消費者 | Text input | Free text |
| `orderStatus` | 訂單狀態 | Text input | Free text |
| `placedAt` | 下單時間 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `orderId` | 訂單編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `orderStatus` | 訂單狀態 | badge | - | `訂單狀態-1`, `訂單狀態-2`, `訂單狀態-3` |
| 3 | `totalAmount` | 應付總額 | text | - | `應付總額-1`, `應付總額-2`, `應付總額-3` |
| 4 | `paidAt` | 付款時間 | text | - | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |
| 5 | `placedAt` | 下單時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

#### Status Badge Color Mapping

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "orderId": "ID-0001",
    "orderStatus": "訂單狀態-1",
    "totalAmount": "應付總額-1",
    "paidAt": "2026-06-01 09:00",
    "placedAt": "2026-06-01 09:00"
  },
  {
    "orderId": "ID-0002",
    "orderStatus": "訂單狀態-2",
    "totalAmount": "應付總額-2",
    "paidAt": "2026-06-02 09:00",
    "placedAt": "2026-06-02 09:00"
  },
  {
    "orderId": "ID-0003",
    "orderStatus": "訂單狀態-3",
    "totalAmount": "應付總額-3",
    "paidAt": "2026-06-03 09:00",
    "placedAt": "2026-06-03 09:00"
  }
]
```


---

### Page 3: 庫存控管

| Property | Value |
|:---|:---|
| Page ID | `inventory-dashboard` |
| Type | **DASHBOARD** |
| Entity | `InventoryItem` |
| Primary Actor |  |
| Allowed Roles |  |
| Source | `inventory-dashboard.hapdl.yaml` |


---

### Page 4: 會員註冊

| Property | Value |
|:---|:---|
| Page ID | `member-registration` |
| Type | **FORM** |
| Entity | `ConsumerProfile` |
| Primary Actor |  |
| Allowed Roles |  |
| Source | `member-registration.hapdl.yaml` |

#### Form Fields

| # | Field | Label | Widget | Required | Sensitive | Options / Constraints | Sample Value |
|:---|:---|:---|:---|:---|:---|:---|:---|

#### Form Layout

- **Layout**: Label-left, 2-column for short fields (text, select, date), full-width for textarea
- **Grouping**: Group by DBML `group` attribute if available
- **Validation**: Show inline error messages below each field
- **Sensitive fields**: Show a lock icon and mask input by default, with a toggle to reveal

#### Footer Actions


#### Interaction Notes



---

### Page 5: 商家訂單管理

| Property | Value |
|:---|:---|
| Page ID | `merchant-order-list` |
| Type | **LIST** |
| Entity | `SalesOrder` |
| Primary Actor |  |
| Allowed Roles |  |
| Source | `merchant-order-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `merchantId` | 商家 | Text input | Free text |
| `orderStatus` | 訂單狀態 | Text input | Free text |
| `placedAt` | 下單時間 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `orderId` | 訂單編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `consumerId` | 消費者 | text | - | `消費者-1`, `消費者-2`, `消費者-3` |
| 3 | `orderStatus` | 訂單狀態 | badge | - | `訂單狀態-1`, `訂單狀態-2`, `訂單狀態-3` |
| 4 | `totalAmount` | 應付總額 | text | - | `應付總額-1`, `應付總額-2`, `應付總額-3` |
| 5 | `placedAt` | 下單時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

#### Status Badge Color Mapping

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "orderId": "ID-0001",
    "consumerId": "消費者-1",
    "orderStatus": "訂單狀態-1",
    "totalAmount": "應付總額-1",
    "placedAt": "2026-06-01 09:00"
  },
  {
    "orderId": "ID-0002",
    "consumerId": "消費者-2",
    "orderStatus": "訂單狀態-2",
    "totalAmount": "應付總額-2",
    "placedAt": "2026-06-02 09:00"
  },
  {
    "orderId": "ID-0003",
    "consumerId": "消費者-3",
    "orderStatus": "訂單狀態-3",
    "totalAmount": "應付總額-3",
    "placedAt": "2026-06-03 09:00"
  }
]
```


---

### Page 6: 商家商品管理

| Property | Value |
|:---|:---|
| Page ID | `merchant-product-management` |
| Type | **LIST** |
| Entity | `Product` |
| Primary Actor |  |
| Allowed Roles |  |
| Source | `merchant-product-management.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `merchantId` | 商家 | Text input | Free text |
| `categoryId` | 分類 | Text input | Free text |
| `productStatus` | 商品狀態 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `productId` | 商品編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `productName` | 商品名稱 | text | - | `商品名稱-1`, `商品名稱-2`, `商品名稱-3` |
| 3 | `categoryId` | 分類 | text | - | `分類-1`, `分類-2`, `分類-3` |
| 4 | `productStatus` | 商品狀態 | badge | - | `商品狀態-1`, `商品狀態-2`, `商品狀態-3` |
| 5 | `updatedAt` | 更新時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

#### Status Badge Color Mapping

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "productId": "ID-0001",
    "productName": "商品名稱-1",
    "categoryId": "分類-1",
    "productStatus": "商品狀態-1",
    "updatedAt": "2026-06-01 09:00"
  },
  {
    "productId": "ID-0002",
    "productName": "商品名稱-2",
    "categoryId": "分類-2",
    "productStatus": "商品狀態-2",
    "updatedAt": "2026-06-02 09:00"
  },
  {
    "productId": "ID-0003",
    "productName": "商品名稱-3",
    "categoryId": "分類-3",
    "productStatus": "商品狀態-3",
    "updatedAt": "2026-06-03 09:00"
  }
]
```


---

### Page 7: 商家營運報表

| Property | Value |
|:---|:---|
| Page ID | `merchant-report-dashboard` |
| Type | **DASHBOARD** |
| Entity | `SalesOrder` |
| Primary Actor |  |
| Allowed Roles |  |
| Source | `merchant-report-dashboard.hapdl.yaml` |


---

### Page 8: 平台權限邊界

| Property | Value |
|:---|:---|
| Page ID | `platform-admin-access` |
| Type | **DASHBOARD** |
| Entity | `Account` |
| Primary Actor |  |
| Allowed Roles |  |
| Source | `platform-admin-access.hapdl.yaml` |


---

### Page 9: 促銷與優惠券管理

| Property | Value |
|:---|:---|
| Page ID | `promotion-coupon-management` |
| Type | **LIST** |
| Entity | `Promotion` |
| Primary Actor |  |
| Allowed Roles |  |
| Source | `promotion-coupon-management.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `merchantId` | 商家 | Text input | Free text |
| `promotionStatus` | 活動狀態 | Text input | Free text |
| `startsAt` | 開始時間 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `promotionId` | 促銷活動編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `promotionName` | 活動名稱 | text | - | `活動名稱-1`, `活動名稱-2`, `活動名稱-3` |
| 3 | `promotionType` | 活動類型 | text | - | `活動類型-1`, `活動類型-2`, `活動類型-3` |
| 4 | `promotionStatus` | 活動狀態 | badge | - | `活動狀態-1`, `活動狀態-2`, `活動狀態-3` |
| 5 | `startsAt` | 開始時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |
| 6 | `endsAt` | 結束時間 | text | - | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

#### Status Badge Color Mapping

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "promotionId": "ID-0001",
    "promotionName": "活動名稱-1",
    "promotionType": "活動類型-1",
    "promotionStatus": "活動狀態-1",
    "startsAt": "2026-06-01 09:00",
    "endsAt": "2026-06-01 09:00"
  },
  {
    "promotionId": "ID-0002",
    "promotionName": "活動名稱-2",
    "promotionType": "活動類型-2",
    "promotionStatus": "活動狀態-2",
    "startsAt": "2026-06-02 09:00",
    "endsAt": "2026-06-02 09:00"
  },
  {
    "promotionId": "ID-0003",
    "promotionName": "活動名稱-3",
    "promotionType": "活動類型-3",
    "promotionStatus": "活動狀態-3",
    "startsAt": "2026-06-03 09:00",
    "endsAt": "2026-06-03 09:00"
  }
]
```


---

### Page 10: 商品瀏覽

| Property | Value |
|:---|:---|
| Page ID | `public-product-list` |
| Type | **LIST** |
| Entity | `Product` |
| Primary Actor |  |
| Allowed Roles |  |
| Source | `public-product-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `categoryId` | 分類 | Text input | Free text |
| `productName` | 商品名稱 | Text input | Free text |
| `productStatus` | 商品狀態 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `productId` | 商品編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `productName` | 商品名稱 | text | - | `商品名稱-1`, `商品名稱-2`, `商品名稱-3` |
| 3 | `brand` | 品牌 | text | - | `品牌-1`, `品牌-2`, `品牌-3` |
| 4 | `productStatus` | 商品狀態 | badge | - | `商品狀態-1`, `商品狀態-2`, `商品狀態-3` |
| 5 | `updatedAt` | 更新時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

#### Status Badge Color Mapping

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "productId": "ID-0001",
    "productName": "商品名稱-1",
    "brand": "品牌-1",
    "productStatus": "商品狀態-1",
    "updatedAt": "2026-06-01 09:00"
  },
  {
    "productId": "ID-0002",
    "productName": "商品名稱-2",
    "brand": "品牌-2",
    "productStatus": "商品狀態-2",
    "updatedAt": "2026-06-02 09:00"
  },
  {
    "productId": "ID-0003",
    "productName": "商品名稱-3",
    "brand": "品牌-3",
    "productStatus": "商品狀態-3",
    "updatedAt": "2026-06-03 09:00"
  }
]
```


---

### Page 11: 退貨退款處理

| Property | Value |
|:---|:---|
| Page ID | `return-refund-workbench` |
| Type | **LIST** |
| Entity | `ReturnRequest` |
| Primary Actor |  |
| Allowed Roles |  |
| Source | `return-refund-workbench.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `returnStatus` | 退貨狀態 | Text input | Free text |
| `requestedAt` | 申請時間 | Text input | Free text |
| `consumerId` | 消費者 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `returnRequestId` | 退貨申請編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `orderId` | 訂單 | text | - | `訂單-1`, `訂單-2`, `訂單-3` |
| 3 | `consumerId` | 消費者 | text | - | `消費者-1`, `消費者-2`, `消費者-3` |
| 4 | `returnStatus` | 退貨狀態 | badge | - | `退貨狀態-1`, `退貨狀態-2`, `退貨狀態-3` |
| 5 | `requestedAt` | 申請時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |
| 6 | `reviewedAt` | 審核時間 | text | - | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

#### Status Badge Color Mapping

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "returnRequestId": "ID-0001",
    "orderId": "訂單-1",
    "consumerId": "消費者-1",
    "returnStatus": "退貨狀態-1",
    "requestedAt": "2026-06-01 09:00",
    "reviewedAt": "2026-06-01 09:00"
  },
  {
    "returnRequestId": "ID-0002",
    "orderId": "訂單-2",
    "consumerId": "消費者-2",
    "returnStatus": "退貨狀態-2",
    "requestedAt": "2026-06-02 09:00",
    "reviewedAt": "2026-06-02 09:00"
  },
  {
    "returnRequestId": "ID-0003",
    "orderId": "訂單-3",
    "consumerId": "消費者-3",
    "returnStatus": "退貨狀態-3",
    "requestedAt": "2026-06-03 09:00",
    "reviewedAt": "2026-06-03 09:00"
  }
]
```


---


## Coverage Supplements

The generator baseline covers list pages well. The following supplement fills page types that require explicit design guidance: wizard, dashboard, and form fields declared under `form.fields`.

### Wizard Page: ????? (`consumer-cart-checkout`)

Design as a four-step checkout wizard with a horizontal stepper, a persistent order summary panel, and footer actions.

| Step | Label | Design Notes |
|:---|:---|:---|
| 1 | 確認購物車 | Show completed state, current state, and validation hint before advancing. |
| 2 | 確認金額 | Show completed state, current state, and validation hint before advancing. |
| 3 | 選擇付款 | Show completed state, current state, and validation hint before advancing. |
| 4 | 建立訂單 | Show completed state, current state, and validation hint before advancing. |

Actions: -

Recommended layout: left content area for cart items/payment form, right sticky summary for subtotal, discount, tax, shipping, and total. Use primary CTA for `create_order`, secondary CTA for `calculate_checkout`.

### Form Page: ???? (`member-registration`)

| Field | Label | Type / Format | Required |
|:---|:---|:---|:---|
| `accountId` | 帳戶 | text | Yes |
| `displayName` | 顯示名稱 | text | - |
| `phone` | 聯絡電話 | text | - |

Actions: `register_with_email`, `public-product-list`

Design as a compact public registration form. Mark required fields, show inline validation, and provide a secondary cancel/back action to product browsing.

### Dashboard Pages

#### 庫存控管 (`inventory-dashboard`)

Filters:
| Field | Label | Type / Format | Required |
|:---|:---|:---|:---|
| `skuId` | SKU | eq | - |
| `availableQty` | 可售庫存 | range | - |

Table / drill-down columns:
| Field | Label | Type / Format | Required |
|:---|:---|:---|:---|
| `inventoryItemId` | 庫存項目 | - | - |
| `skuId` | SKU | - | - |
| `onHandQty` | 帳面庫存 | number | - |
| `availableQty` | 可售庫存 | number | - |
| `lowStockThreshold` | 低庫存門檻 | number | - |
| `updatedAt` | 更新時間 | date | - |

Actions: -

Design guidance: use KPI cards for summary values, a filter bar at the top, and a drill-down table or activity panel below. Keep the layout dense and operational rather than marketing-style.

#### 商家營運報表 (`merchant-report-dashboard`)

Filters:
| Field | Label | Type / Format | Required |
|:---|:---|:---|:---|
| `merchantId` | 商家 | eq | - |
| `placedAt` | 報表期間 | range | - |
| `orderStatus` | 訂單狀態 | eq | - |

Metrics / KPI cards:
| Field | Label | Type / Format | Required |
|:---|:---|:---|:---|
| `totalAmount` | 銷售額 | currency | - |
| `orderId` | 訂單數 | number | - |
| `consumerId` | 消費者數 | number | - |

Actions: -

Design guidance: use KPI cards for summary values, a filter bar at the top, and a drill-down table or activity panel below. Keep the layout dense and operational rather than marketing-style.

#### 平台權限邊界 (`platform-admin-access`)

Filters:
| Field | Label | Type / Format | Required |
|:---|:---|:---|:---|
| `accountType` | 帳戶類型 | eq | - |
| `accountStatus` | 帳戶狀態 | eq | - |

Table / drill-down columns:
| Field | Label | Type / Format | Required |
|:---|:---|:---|:---|
| `accountId` | 帳戶編號 | - | - |
| `email` | Email | - | - |
| `accountType` | 類型 | badge | - |
| `accountStatus` | 狀態 | badge | - |
| `updatedAt` | 更新時間 | date | - |

Actions: -

Design guidance: use KPI cards for summary values, a filter bar at the top, and a drill-down table or activity panel below. Keep the layout dense and operational rather than marketing-style.


## Generation Instructions

When generating UI from this brief:

1. **Use the Design System** above for all colors, typography, and spacing
2. **Render all text in Traditional Chinese (zh-TW)** as specified in each page
3. **Include the sidebar navigation** as shown in the Navigation Map
4. **Use the sample data** provided for each page to populate the preview
5. **Apply badge colors** as specified in the Status Badge Color Mapping
6. **Include responsive layout** that works on 1280px+ screens
7. **For forms**: show validation states, required field markers (*), and sensitive field masks
8. **For tables**: include sortable column headers, hover states, and row action buttons
9. **For detail pages**: use a clean key-value layout with grouped sections
10. Generate as **React + TypeScript** with **Ant Design** components, or as standalone **HTML + CSS**
