# smallBiz UI Design Brief

> **Purpose**: This document is a structured design brief auto-generated from
> `haPDL` (page intent specs) + `schema.dbml` (data model) + `haARM` (access control).
> Feed this entire document to **Claude Design** or any AI design tool to generate
> Hi-Fi mockups, HTML, or React component code.
>
> **System**: 月租制、開箱即用的 B2C 電商平台，讓台灣中小零售商家自有線上商店、自管商品訂單與會員資料。
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

  [audit-log]
    ☰ 稽核紀錄
  [brand]
    ✏ 品牌編輯
  [campaign]
    ✏ 促銷活動編輯
    ☰ 促銷活動列表
  [cart]
    📄 購物車
  [category]
    ✏ 商品分類編輯
    ☰ 商品分類管理
  [coupon]
    ✏ 優惠券編輯
    ☰ 優惠券列表
  [member-address]
    ✏ 收件地址編輯
    ☰ 常用收件地址
  [member]
    ✏ 會員註冊與資料
  [merchant]
    ✏ 商家註冊開店
    ☰ 商家管理列表
  [merchant-operator]
    ✏ 操作者帳號編輯
    ☰ 操作者帳號管理
  [merchant-report]
    · 商家銷售報表
  [notification-log]
    ☰ 通知紀錄
  [order]
    📄 訂單明細
    ✏ 結帳
    ☰ 訂單列表
  [platform-user]
    ✏ 平台人員編輯
    ☰ 平台人員管理
  [point-ledger]
    ☰ 點數明細
  [product]
    ✏ 商品編輯
    ☰ 商品列表
  [product-variant]
    ✏ 規格 SKU 編輯
  [return-request]
    ✏ 申請退貨
    ☰ 退貨申請列表
  [shipment]
    ✏ 標記出貨
  [stock-item]
    ✏ 庫存設定
    ☰ 庫存列表
  [store]
    ✏ 店面資料
  [wishlist]
    ☰ 願望清單
```

### Page Flow

```
稽核紀錄 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

促銷活動列表 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

商品分類管理 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

優惠券列表 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

常用收件地址 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

商家管理列表 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

操作者帳號管理 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

通知紀錄 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

訂單列表 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

平台人員管理 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

點數明細 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

商品列表 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

退貨申請列表 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

庫存列表 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

願望清單 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

品牌編輯 (form)
  └── [送出/核准] → back to list

促銷活動編輯 (form)
  └── [送出/核准] → back to list

商品分類編輯 (form)
  └── [送出/核准] → back to list

優惠券編輯 (form)
  └── [送出/核准] → back to list

收件地址編輯 (form)
  └── [送出/核准] → back to list

會員註冊與資料 (form)
  └── [送出/核准] → back to list

商家註冊開店 (form)
  └── [送出/核准] → back to list

操作者帳號編輯 (form)
  └── [送出/核准] → back to list

結帳 (form)
  └── [送出/核准] → back to list

平台人員編輯 (form)
  └── [送出/核准] → back to list

商品編輯 (form)
  └── [送出/核准] → back to list

規格 SKU 編輯 (form)
  └── [送出/核准] → back to list

申請退貨 (form)
  └── [送出/核准] → back to list

標記出貨 (form)
  └── [送出/核准] → back to list

庫存設定 (form)
  └── [送出/核准] → back to list

店面資料 (form)
  └── [送出/核准] → back to list

購物車 (detail)

訂單明細 (detail)

```

## Page Specifications

### Page 1: 稽核紀錄

| Property | Value |
|:---|:---|
| Page ID | `audit-log-list` |
| Type | **LIST** |
| Entity | `AuditLog` |
| Primary Actor |  |
| Allowed Roles | 商家, 平台管理員 |
| Source | `audit-log-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `actorType` | 操作者類型 | Text input | Free text |
| `action` | 操作類型 | Text input | Free text |
| `createdAt` | 操作時間 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `auditId` | 稽核編號 | text | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `actorType` | 操作者類型 | badge | - | `操作者類型-1`, `操作者類型-2`, `操作者類型-3` |
| 3 | `action` | 操作類型 | badge | - | `操作類型-1`, `操作類型-2`, `操作類型-3` |
| 4 | `targetEntity` | 目標實體 | text | - | `目標實體-1`, `目標實體-2`, `目標實體-3` |
| 5 | `targetId` | 目標編號 | text | - | `目標編號-1`, `目標編號-2`, `目標編號-3` |
| 6 | `createdAt` | 操作時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

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
    "auditId": "ID-0001",
    "actorType": "操作者類型-1",
    "action": "操作類型-1",
    "targetEntity": "目標實體-1",
    "targetId": "目標編號-1",
    "createdAt": "2026-06-01 09:00"
  },
  {
    "auditId": "ID-0002",
    "actorType": "操作者類型-2",
    "action": "操作類型-2",
    "targetEntity": "目標實體-2",
    "targetId": "目標編號-2",
    "createdAt": "2026-06-02 09:00"
  },
  {
    "auditId": "ID-0003",
    "actorType": "操作者類型-3",
    "action": "操作類型-3",
    "targetEntity": "目標實體-3",
    "targetId": "目標編號-3",
    "createdAt": "2026-06-03 09:00"
  }
]
```


---

### Page 2: 品牌編輯

| Property | Value |
|:---|:---|
| Page ID | `brand-form` |
| Type | **FORM** |
| Entity | `Brand` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `brand-form.hapdl.yaml` |

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

### Page 3: 促銷活動編輯

| Property | Value |
|:---|:---|
| Page ID | `campaign-form` |
| Type | **FORM** |
| Entity | `Campaign` |
| Primary Actor |  |
| Allowed Roles | 商家, 平台行銷人員 |
| Source | `campaign-form.hapdl.yaml` |

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

### Page 4: 促銷活動列表

| Property | Value |
|:---|:---|
| Page ID | `campaign-list` |
| Type | **LIST** |
| Entity | `Campaign` |
| Primary Actor |  |
| Allowed Roles | 商家, 平台行銷人員 |
| Source | `campaign-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `campaignType` | 活動類型 | Text input | Free text |
| `status` | 活動狀態 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `campaignId` | 活動編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `name` | 活動名稱 | text | - | `活動名稱-1`, `活動名稱-2`, `活動名稱-3` |
| 3 | `campaignType` | 活動類型 | badge | - | `活動類型-1`, `活動類型-2`, `活動類型-3` |
| 4 | `status` | 活動狀態 | badge | - | `活動狀態-1`, `活動狀態-2`, `活動狀態-3` |
| 5 | `startAt` | 檔期開始 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |
| 6 | `endAt` | 檔期結束 | text | - | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

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
    "campaignId": "ID-0001",
    "name": "活動名稱-1",
    "campaignType": "活動類型-1",
    "status": "活動狀態-1",
    "startAt": "2026-06-01 09:00",
    "endAt": "2026-06-01 09:00"
  },
  {
    "campaignId": "ID-0002",
    "name": "活動名稱-2",
    "campaignType": "活動類型-2",
    "status": "活動狀態-2",
    "startAt": "2026-06-02 09:00",
    "endAt": "2026-06-02 09:00"
  },
  {
    "campaignId": "ID-0003",
    "name": "活動名稱-3",
    "campaignType": "活動類型-3",
    "status": "活動狀態-3",
    "startAt": "2026-06-03 09:00",
    "endAt": "2026-06-03 09:00"
  }
]
```


---

### Page 5: 購物車

| Property | Value |
|:---|:---|
| Page ID | `cart-detail` |
| Type | **DETAIL** |
| Entity | `Cart` |
| Primary Actor |  |
| Allowed Roles | 消費者 |
| Source | `cart-detail.hapdl.yaml` |

#### Detail Fields

| # | Field | Label | Display | Sample Value |
|:---|:---|:---|:---|:---|
| 1 | `cartId` | 購物車編號 | Monospace, bold | `ID-0001` |
| 2 | `updatedAt` | 更新時間 | Plain text | `2026-06-01 09:00` |

#### Detail Layout

- **Layout**: 2-column key-value grid (label left-aligned, value right)
- **Section dividers**: Group related fields with subtle horizontal rules
- **Related data**: Show related tables below (e.g., attachments list, audit history)


---

### Page 6: 商品分類編輯

| Property | Value |
|:---|:---|
| Page ID | `category-form` |
| Type | **FORM** |
| Entity | `Category` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `category-form.hapdl.yaml` |

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

### Page 7: 商品分類管理

| Property | Value |
|:---|:---|
| Page ID | `category-list` |
| Type | **LIST** |
| Entity | `Category` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `category-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `parentCategoryId` | 上層分類 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `categoryId` | 分類編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `name` | 分類名稱 | text | - | `分類名稱-1`, `分類名稱-2`, `分類名稱-3` |
| 3 | `parentCategoryId` | 上層分類 | text | - | `上層分類-1`, `上層分類-2`, `上層分類-3` |
| 4 | `sortOrder` | 排序 | text | Yes | `排序-1`, `排序-2`, `排序-3` |

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "categoryId": "ID-0001",
    "name": "分類名稱-1",
    "parentCategoryId": "上層分類-1",
    "sortOrder": "排序-1"
  },
  {
    "categoryId": "ID-0002",
    "name": "分類名稱-2",
    "parentCategoryId": "上層分類-2",
    "sortOrder": "排序-2"
  },
  {
    "categoryId": "ID-0003",
    "name": "分類名稱-3",
    "parentCategoryId": "上層分類-3",
    "sortOrder": "排序-3"
  }
]
```


---

### Page 8: 優惠券編輯

| Property | Value |
|:---|:---|
| Page ID | `coupon-form` |
| Type | **FORM** |
| Entity | `Coupon` |
| Primary Actor |  |
| Allowed Roles | 商家, 平台行銷人員 |
| Source | `coupon-form.hapdl.yaml` |

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

### Page 9: 優惠券列表

| Property | Value |
|:---|:---|
| Page ID | `coupon-list` |
| Type | **LIST** |
| Entity | `Coupon` |
| Primary Actor |  |
| Allowed Roles | 商家, 平台行銷人員 |
| Source | `coupon-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `code` | 券代碼 | Text input | Free text |
| `discountType` | 折扣方式 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `couponId` | 優惠券編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `code` | 券代碼 | text | - | `券代碼-1`, `券代碼-2`, `券代碼-3` |
| 3 | `name` | 券名稱 | text | - | `券名稱-1`, `券名稱-2`, `券名稱-3` |
| 4 | `minSpend` | 最低消費門檻 | text | - | `最低消費門檻-1`, `最低消費門檻-2`, `最低消費門檻-3` |
| 5 | `usedCount` | 已使用張數 | text | - | `已使用張數-1`, `已使用張數-2`, `已使用張數-3` |
| 6 | `usageCap` | 總使用張數上限 | text | - | `總使用張數上限-1`, `總使用張數上限-2`, `總使用張數上限-3` |
| 7 | `validTo` | 有效期間迄 | text | Yes | `有效期間迄-1`, `有效期間迄-2`, `有效期間迄-3` |

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "couponId": "ID-0001",
    "code": "券代碼-1",
    "name": "券名稱-1",
    "minSpend": "最低消費門檻-1",
    "usedCount": "已使用張數-1",
    "usageCap": "總使用張數上限-1",
    "validTo": "有效期間迄-1"
  },
  {
    "couponId": "ID-0002",
    "code": "券代碼-2",
    "name": "券名稱-2",
    "minSpend": "最低消費門檻-2",
    "usedCount": "已使用張數-2",
    "usageCap": "總使用張數上限-2",
    "validTo": "有效期間迄-2"
  },
  {
    "couponId": "ID-0003",
    "code": "券代碼-3",
    "name": "券名稱-3",
    "minSpend": "最低消費門檻-3",
    "usedCount": "已使用張數-3",
    "usageCap": "總使用張數上限-3",
    "validTo": "有效期間迄-3"
  }
]
```


---

### Page 10: 收件地址編輯

| Property | Value |
|:---|:---|
| Page ID | `member-address-form` |
| Type | **FORM** |
| Entity | `MemberAddress` |
| Primary Actor |  |
| Allowed Roles | 消費者 |
| Source | `member-address-form.hapdl.yaml` |

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

### Page 11: 常用收件地址

| Property | Value |
|:---|:---|
| Page ID | `member-address-list` |
| Type | **LIST** |
| Entity | `MemberAddress` |
| Primary Actor |  |
| Allowed Roles | 消費者 |
| Source | `member-address-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `recipientName` | 收件人姓名 | text | - | `收件人姓名-1`, `收件人姓名-2`, `收件人姓名-3` |
| 2 | `phone` | 收件人電話 | text | - | `********`, `********`, `********` |
| 3 | `address` | 收件地址 | text | - | `收件地址-1`, `收件地址-2`, `收件地址-3` |
| 4 | `isDefault` | 預設地址 | text | - | `預設地址-1`, `預設地址-2`, `預設地址-3` |

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "recipientName": "收件人姓名-1",
    "phone": "********",
    "address": "收件地址-1",
    "isDefault": "預設地址-1"
  },
  {
    "recipientName": "收件人姓名-2",
    "phone": "********",
    "address": "收件地址-2",
    "isDefault": "預設地址-2"
  },
  {
    "recipientName": "收件人姓名-3",
    "phone": "********",
    "address": "收件地址-3",
    "isDefault": "預設地址-3"
  }
]
```


---

### Page 12: 會員註冊與資料

| Property | Value |
|:---|:---|
| Page ID | `member-form` |
| Type | **FORM** |
| Entity | `Member` |
| Primary Actor |  |
| Allowed Roles | 公開訪客, 消費者 |
| Source | `member-form.hapdl.yaml` |

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

### Page 13: 商家註冊開店

| Property | Value |
|:---|:---|
| Page ID | `merchant-form` |
| Type | **FORM** |
| Entity | `Merchant` |
| Primary Actor |  |
| Allowed Roles | 公開訪客 |
| Source | `merchant-form.hapdl.yaml` |

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

### Page 14: 商家管理列表

| Property | Value |
|:---|:---|
| Page ID | `merchant-list` |
| Type | **LIST** |
| Entity | `Merchant` |
| Primary Actor |  |
| Allowed Roles | 平台管理員 |
| Source | `merchant-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `status` | 帳號狀態 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `merchantId` | 商家編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `name` | 商家名稱 | text | - | `商家名稱-1`, `商家名稱-2`, `商家名稱-3` |
| 3 | `status` | 帳號狀態 | badge | - | `帳號狀態-1`, `帳號狀態-2`, `帳號狀態-3` |
| 4 | `createdAt` | 註冊時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

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
    "merchantId": "ID-0001",
    "name": "商家名稱-1",
    "status": "帳號狀態-1",
    "createdAt": "2026-06-01 09:00"
  },
  {
    "merchantId": "ID-0002",
    "name": "商家名稱-2",
    "status": "帳號狀態-2",
    "createdAt": "2026-06-02 09:00"
  },
  {
    "merchantId": "ID-0003",
    "name": "商家名稱-3",
    "status": "帳號狀態-3",
    "createdAt": "2026-06-03 09:00"
  }
]
```


---

### Page 15: 操作者帳號編輯

| Property | Value |
|:---|:---|
| Page ID | `merchant-operator-form` |
| Type | **FORM** |
| Entity | `MerchantOperator` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `merchant-operator-form.hapdl.yaml` |

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

### Page 16: 操作者帳號管理

| Property | Value |
|:---|:---|
| Page ID | `merchant-operator-list` |
| Type | **LIST** |
| Entity | `MerchantOperator` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `merchant-operator-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `status` | 帳號狀態 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `operatorId` | 操作者編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `name` | 操作者姓名 | text | - | `操作者姓名-1`, `操作者姓名-2`, `操作者姓名-3` |
| 3 | `isOwner` | 是否店主 | text | - | `是否店主-1`, `是否店主-2`, `是否店主-3` |
| 4 | `status` | 帳號狀態 | badge | - | `帳號狀態-1`, `帳號狀態-2`, `帳號狀態-3` |

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
    "operatorId": "ID-0001",
    "name": "操作者姓名-1",
    "isOwner": "是否店主-1",
    "status": "帳號狀態-1"
  },
  {
    "operatorId": "ID-0002",
    "name": "操作者姓名-2",
    "isOwner": "是否店主-2",
    "status": "帳號狀態-2"
  },
  {
    "operatorId": "ID-0003",
    "name": "操作者姓名-3",
    "isOwner": "是否店主-3",
    "status": "帳號狀態-3"
  }
]
```


---

### Page 17: 商家銷售報表

| Property | Value |
|:---|:---|
| Page ID | `merchant-report-dashboard` |
| Type | **DASHBOARD** |
| Entity | `Order` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `merchant-report-dashboard.hapdl.yaml` |


---

### Page 18: 通知紀錄

| Property | Value |
|:---|:---|
| Page ID | `notification-log-list` |
| Type | **LIST** |
| Entity | `NotificationLog` |
| Primary Actor |  |
| Allowed Roles | 消費者 |
| Source | `notification-log-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `channel` | 通知通道 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `title` | 通知標題 | text | - | `通知標題-1`, `通知標題-2`, `通知標題-3` |
| 2 | `channel` | 通知通道 | badge | - | `通知通道-1`, `通知通道-2`, `通知通道-3` |
| 3 | `content` | 通知內容 | text | - | `通知內容-1`, `通知內容-2`, `通知內容-3` |
| 4 | `sentAt` | 發送時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

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
    "title": "通知標題-1",
    "channel": "通知通道-1",
    "content": "通知內容-1",
    "sentAt": "2026-06-01 09:00"
  },
  {
    "title": "通知標題-2",
    "channel": "通知通道-2",
    "content": "通知內容-2",
    "sentAt": "2026-06-02 09:00"
  },
  {
    "title": "通知標題-3",
    "channel": "通知通道-3",
    "content": "通知內容-3",
    "sentAt": "2026-06-03 09:00"
  }
]
```


---

### Page 19: 訂單明細

| Property | Value |
|:---|:---|
| Page ID | `order-detail` |
| Type | **DETAIL** |
| Entity | `Order` |
| Primary Actor |  |
| Allowed Roles | 消費者, 商家 |
| Source | `order-detail.hapdl.yaml` |

#### Detail Fields

| # | Field | Label | Display | Sample Value |
|:---|:---|:---|:---|:---|
| 1 | `orderId` | 訂單編號 | Monospace, bold | `ID-0001` |
| 2 | `status` | 訂單狀態 | Plain text | `訂單狀態-1` |
| 3 | `subtotal` | 商品小計 | Plain text | `商品小計-1` |
| 4 | `campaignDiscount` | 活動折扣金額 | Plain text | `活動折扣金額-1` |
| 5 | `couponDiscount` | 優惠券折抵金額 | Plain text | `優惠券折抵金額-1` |
| 6 | `pointsDiscount` | 點數折抵金額 | Plain text | `點數折抵金額-1` |
| 7 | `shippingFee` | 運費 | Plain text | `運費-1` |
| 8 | `taxAmount` | 營業稅額 | Plain text | `營業稅額-1` |
| 9 | `totalAmount` | 訂單總額 | Plain text | `訂單總額-1` |
| 10 | `recipientName` | 收件人姓名 | Plain text | `收件人姓名-1` |
| 11 | `shippingAddress` | 收件地址 | Plain text | `收件地址-1` |

#### Detail Layout

- **Layout**: 2-column key-value grid (label left-aligned, value right)
- **Section dividers**: Group related fields with subtle horizontal rules
- **Related data**: Show related tables below (e.g., attachments list, audit history)


---

### Page 20: 結帳

| Property | Value |
|:---|:---|
| Page ID | `order-form` |
| Type | **FORM** |
| Entity | `Order` |
| Primary Actor |  |
| Allowed Roles | 消費者 |
| Source | `order-form.hapdl.yaml` |

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

### Page 21: 訂單列表

| Property | Value |
|:---|:---|
| Page ID | `order-list` |
| Type | **LIST** |
| Entity | `Order` |
| Primary Actor |  |
| Allowed Roles | 消費者, 商家 |
| Source | `order-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `status` | 訂單狀態 | Text input | Free text |
| `createdAt` | 成立時間 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `orderId` | 訂單編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `status` | 訂單狀態 | badge | - | `訂單狀態-1`, `訂單狀態-2`, `訂單狀態-3` |
| 3 | `totalAmount` | 訂單總額 | text | - | `訂單總額-1`, `訂單總額-2`, `訂單總額-3` |
| 4 | `createdAt` | 成立時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

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
    "status": "訂單狀態-1",
    "totalAmount": "訂單總額-1",
    "createdAt": "2026-06-01 09:00"
  },
  {
    "orderId": "ID-0002",
    "status": "訂單狀態-2",
    "totalAmount": "訂單總額-2",
    "createdAt": "2026-06-02 09:00"
  },
  {
    "orderId": "ID-0003",
    "status": "訂單狀態-3",
    "totalAmount": "訂單總額-3",
    "createdAt": "2026-06-03 09:00"
  }
]
```


---

### Page 22: 平台人員編輯

| Property | Value |
|:---|:---|
| Page ID | `platform-user-form` |
| Type | **FORM** |
| Entity | `PlatformUser` |
| Primary Actor |  |
| Allowed Roles | 平台管理員 |
| Source | `platform-user-form.hapdl.yaml` |

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

### Page 23: 平台人員管理

| Property | Value |
|:---|:---|
| Page ID | `platform-user-list` |
| Type | **LIST** |
| Entity | `PlatformUser` |
| Primary Actor |  |
| Allowed Roles | 平台管理員 |
| Source | `platform-user-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `roleCode` | 平台角色 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `platformUserId` | 平台人員編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `name` | 姓名 | text | - | `姓名-1`, `姓名-2`, `姓名-3` |
| 3 | `roleCode` | 平台角色 | badge | - | `平台角色-1`, `平台角色-2`, `平台角色-3` |
| 4 | `isActive` | 是否啟用 | text | - | `是否啟用-1`, `是否啟用-2`, `是否啟用-3` |

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
    "platformUserId": "ID-0001",
    "name": "姓名-1",
    "roleCode": "平台角色-1",
    "isActive": "是否啟用-1"
  },
  {
    "platformUserId": "ID-0002",
    "name": "姓名-2",
    "roleCode": "平台角色-2",
    "isActive": "是否啟用-2"
  },
  {
    "platformUserId": "ID-0003",
    "name": "姓名-3",
    "roleCode": "平台角色-3",
    "isActive": "是否啟用-3"
  }
]
```


---

### Page 24: 點數明細

| Property | Value |
|:---|:---|
| Page ID | `point-ledger-list` |
| Type | **LIST** |
| Entity | `PointLedger` |
| Primary Actor |  |
| Allowed Roles | 消費者 |
| Source | `point-ledger-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `changeType` | 異動類型 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `ledgerId` | 異動編號 | text | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `changeType` | 異動類型 | badge | - | `異動類型-1`, `異動類型-2`, `異動類型-3` |
| 3 | `points` | 異動點數（正負） | text | - | `異動點數（正負）-1`, `異動點數（正負）-2`, `異動點數（正負）-3` |
| 4 | `balanceAfter` | 異動後餘額 | text | - | `異動後餘額-1`, `異動後餘額-2`, `異動後餘額-3` |
| 5 | `expireAt` | 點數效期（獲得型適用） | text | - | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |
| 6 | `createdAt` | 異動時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

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
    "ledgerId": "ID-0001",
    "changeType": "異動類型-1",
    "points": "異動點數（正負）-1",
    "balanceAfter": "異動後餘額-1",
    "expireAt": "2026-06-01 09:00",
    "createdAt": "2026-06-01 09:00"
  },
  {
    "ledgerId": "ID-0002",
    "changeType": "異動類型-2",
    "points": "異動點數（正負）-2",
    "balanceAfter": "異動後餘額-2",
    "expireAt": "2026-06-02 09:00",
    "createdAt": "2026-06-02 09:00"
  },
  {
    "ledgerId": "ID-0003",
    "changeType": "異動類型-3",
    "points": "異動點數（正負）-3",
    "balanceAfter": "異動後餘額-3",
    "expireAt": "2026-06-03 09:00",
    "createdAt": "2026-06-03 09:00"
  }
]
```


---

### Page 25: 商品編輯

| Property | Value |
|:---|:---|
| Page ID | `product-form` |
| Type | **FORM** |
| Entity | `Product` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `product-form.hapdl.yaml` |

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

### Page 26: 商品列表

| Property | Value |
|:---|:---|
| Page ID | `product-list` |
| Type | **LIST** |
| Entity | `Product` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `product-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `categoryId` | 商品分類 | Text input | Free text |
| `brandId` | 品牌 | Text input | Free text |
| `status` | 商品狀態 | Text input | Free text |
| `name` | 商品名稱 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `productId` | 商品編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `name` | 商品名稱 | text | - | `商品名稱-1`, `商品名稱-2`, `商品名稱-3` |
| 3 | `status` | 商品狀態 | badge | - | `商品狀態-1`, `商品狀態-2`, `商品狀態-3` |
| 4 | `publishedAt` | 上架時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

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
    "name": "商品名稱-1",
    "status": "商品狀態-1",
    "publishedAt": "2026-06-01 09:00"
  },
  {
    "productId": "ID-0002",
    "name": "商品名稱-2",
    "status": "商品狀態-2",
    "publishedAt": "2026-06-02 09:00"
  },
  {
    "productId": "ID-0003",
    "name": "商品名稱-3",
    "status": "商品狀態-3",
    "publishedAt": "2026-06-03 09:00"
  }
]
```


---

### Page 27: 規格 SKU 編輯

| Property | Value |
|:---|:---|
| Page ID | `product-variant-form` |
| Type | **FORM** |
| Entity | `ProductVariant` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `product-variant-form.hapdl.yaml` |

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

### Page 28: 申請退貨

| Property | Value |
|:---|:---|
| Page ID | `return-request-form` |
| Type | **FORM** |
| Entity | `ReturnRequest` |
| Primary Actor |  |
| Allowed Roles | 消費者 |
| Source | `return-request-form.hapdl.yaml` |

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

### Page 29: 退貨申請列表

| Property | Value |
|:---|:---|
| Page ID | `return-request-list` |
| Type | **LIST** |
| Entity | `ReturnRequest` |
| Primary Actor |  |
| Allowed Roles | 消費者, 商家 |
| Source | `return-request-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `status` | 退貨狀態 | Text input | Free text |
| `orderId` | 所屬訂單 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `returnRequestId` | 退貨申請編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `orderId` | 所屬訂單 | text | - | `所屬訂單-1`, `所屬訂單-2`, `所屬訂單-3` |
| 3 | `status` | 退貨狀態 | badge | - | `退貨狀態-1`, `退貨狀態-2`, `退貨狀態-3` |
| 4 | `appliedAt` | 申請時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

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
    "orderId": "所屬訂單-1",
    "status": "退貨狀態-1",
    "appliedAt": "2026-06-01 09:00"
  },
  {
    "returnRequestId": "ID-0002",
    "orderId": "所屬訂單-2",
    "status": "退貨狀態-2",
    "appliedAt": "2026-06-02 09:00"
  },
  {
    "returnRequestId": "ID-0003",
    "orderId": "所屬訂單-3",
    "status": "退貨狀態-3",
    "appliedAt": "2026-06-03 09:00"
  }
]
```


---

### Page 30: 標記出貨

| Property | Value |
|:---|:---|
| Page ID | `shipment-form` |
| Type | **FORM** |
| Entity | `Shipment` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `shipment-form.hapdl.yaml` |

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

### Page 31: 庫存設定

| Property | Value |
|:---|:---|
| Page ID | `stock-item-form` |
| Type | **FORM** |
| Entity | `StockItem` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `stock-item-form.hapdl.yaml` |

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

### Page 32: 庫存列表

| Property | Value |
|:---|:---|
| Page ID | `stock-item-list` |
| Type | **LIST** |
| Entity | `StockItem` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `stock-item-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `variantId` | 對應 SKU | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `variantId` | 對應 SKU | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `quantity` | 實際庫存量 | text | - | `實際庫存量-1`, `實際庫存量-2`, `實際庫存量-3` |
| 3 | `reservedQuantity` | 預留量 | text | - | `預留量-1`, `預留量-2`, `預留量-3` |
| 4 | `restockThreshold` | 補貨水位 | text | - | `補貨水位-1`, `補貨水位-2`, `補貨水位-3` |
| 5 | `updatedAt` | 異動時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "variantId": "ID-0001",
    "quantity": "實際庫存量-1",
    "reservedQuantity": "預留量-1",
    "restockThreshold": "補貨水位-1",
    "updatedAt": "2026-06-01 09:00"
  },
  {
    "variantId": "ID-0002",
    "quantity": "實際庫存量-2",
    "reservedQuantity": "預留量-2",
    "restockThreshold": "補貨水位-2",
    "updatedAt": "2026-06-02 09:00"
  },
  {
    "variantId": "ID-0003",
    "quantity": "實際庫存量-3",
    "reservedQuantity": "預留量-3",
    "restockThreshold": "補貨水位-3",
    "updatedAt": "2026-06-03 09:00"
  }
]
```


---

### Page 33: 店面資料

| Property | Value |
|:---|:---|
| Page ID | `store-form` |
| Type | **FORM** |
| Entity | `Store` |
| Primary Actor |  |
| Allowed Roles | 商家 |
| Source | `store-form.hapdl.yaml` |

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

### Page 34: 願望清單

| Property | Value |
|:---|:---|
| Page ID | `wishlist-list` |
| Type | **LIST** |
| Entity | `Wishlist` |
| Primary Actor |  |
| Allowed Roles | 消費者 |
| Source | `wishlist-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `wishlistId` | 願望清單編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `productId` | 收藏商品 | text | - | `收藏商品-1`, `收藏商品-2`, `收藏商品-3` |
| 3 | `createdAt` | 加入時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "wishlistId": "ID-0001",
    "productId": "收藏商品-1",
    "createdAt": "2026-06-01 09:00"
  },
  {
    "wishlistId": "ID-0002",
    "productId": "收藏商品-2",
    "createdAt": "2026-06-02 09:00"
  },
  {
    "wishlistId": "ID-0003",
    "productId": "收藏商品-3",
    "createdAt": "2026-06-03 09:00"
  }
]
```


---


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
