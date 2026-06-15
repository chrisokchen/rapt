# DBML v3.3 Annotation Rules

> **版本**：v3.3.0  
> **完整規格**：`RAPTor/DSLspec/DBML-QUICK-REFERENCE.md`、`RAPTor/DSLspec/annotated_DBML-v3.3.md`  
> DSLspec v3.3 takes precedence over this file's examples.

---

## 四個一級標註（v3.3 收編為正式語法）

| 標註 | 型別 | 預設 | 必要性 |
|------|------|------|-------|
| `label:` | string | 推斷或 Capitalize | 建議每個欄位都寫 |
| `ref_code:` | string | 無 | 有動態列舉下拉才寫 |
| `sensitive:` | boolean | `false` | 只寫 `sensitive: true`，不寫 false |
| `group:` | string | 推斷或 null | 有分組需求時寫 |

---

## 強制規則（MUST）

### R-DBML-01：label 是業務顯示名稱

```dbml
# ✅ 正確
userId nvarchar(60) [pk, label: '使用者帳號', group: 'basic']

# ❌ 錯誤：沒有 label
userId nvarchar(60) [pk]
```

### R-DBML-02：sensitive 只寫 true

```dbml
# ✅ 正確
password nvarchar(150) [not null, sensitive: true, label: '密碼']

# ❌ 錯誤 AP-03：顯式寫 false
phone nvarchar(20) [sensitive: false, label: '電話']
```

### R-DBML-03：ref_code 和 ref 不並存（AP-02）

```dbml
# ✅ 正確（值集合用 ref_code）
status nchar(1) [ref_code: 'OrderStatus', label: '訂單狀態']

# ✅ 正確（關聯實體用 ref）
customerId nvarchar(60) [ref: > Customer.customerId, label: '客戶']

# ❌ 錯誤 AP-02：同時有兩個
status nchar(1) [ref_code: 'Status', ref: > StatusTable.id]
```

### R-DBML-04：不用 note subformat（AP-01）

```dbml
# ✅ 正確：使用一級語法
userId nvarchar(60) [pk, label: '使用者帳號', group: 'basic']

# ❌ 錯誤 AP-01：用 note 嵌入 label/group
userId nvarchar(60) [pk, note: 'label:使用者帳號|group:basic']
```

### R-DBML-05：UI 偏好不放 DBML（AP-05）

```dbml
# ❌ 錯誤 AP-05：color/icon 屬於 UI，放 haPDL
status nchar(1) [label: '狀態', color: 'green', icon: 'check']

# ✅ 正確：DBML 只放資料本質，UI 放 haPDL
status nchar(1) [ref_code: 'Status', label: '狀態']
```

### R-DBML-06：group 只在一處定義（AP-04）

```dbml
# ✅ 正確：DBML 定義 group，haPDL 不重複
email nvarchar(50) [sensitive: true, label: '電子郵件', group: 'contact']
# haPDL 中不要再定義同一個 group

# ❌ 錯誤 AP-04：DBML 和 haPDL 都定義同一個 group
```

### R-DBML-07：ref_code 必須有 seeds.md 值域

```dbml
# ✅ 正確：status 有 ref_code，且 seeds.md 有 AccountStatus section
status nchar(1) [not null, ref_code: 'AccountStatus', label: '帳號狀態']

# ❌ 錯誤：只有 Note 說明值域，沒有 seeds.md 或 OPEN CiC
status nchar(1) [not null, ref_code: 'AccountStatus', label: '帳號狀態']
```

### R-DBML-08：狀態 / 權限 / 刪除限制必須有 constraint 支撐

bitmask、狀態轉換、引用刪除限制、頻率限制等規則必須在 `seeds.md` 或 `constraints.md` 中可追蹤；不能只存在自然語言 Note。

### R-DBML-09：相容性反正規化必須有補償規則

逗號串列、冗餘快照、legacy 欄位保留等設計必須在 compatibility decision 中說明 risk，並在 `constraints.md` 指向服務層補償規則。

### R-DBML-10：legacy 命名必須有 canonical alias

若保留既有 table / column 命名風格，必須在 `glossary.md` 的 Canonical Mapping 中填入 `legacy_aliases`。

---

## Table Note 慣例

```dbml
Table Order {
  ...
  Note: 'HT001 訂單主檔'   // 業務說明，建議格式：<系統代碼> <中文描述>
}
```

---

## 外鍵 Ref 宣告位置

```dbml
// ✅ 推薦：獨立宣告，在 Table 後
Ref: Order.customerId > Customer.customerId

// ✅ 也可以：inline ref
customerId nvarchar(60) [ref: > Customer.customerId, label: '客戶']
```

---

## 最小完整範例

```dbml
Table Order {
  orderId    nvarchar(20)   [pk, label: '訂單編號', group: 'basic']
  customerId nvarchar(60)   [not null, label: '客戶', group: 'basic']
  status     nchar(1)       [not null, default: 'N', ref_code: 'OrderStatus', label: '訂單狀態']
  totalAmount decimal(18,2) [not null, label: '訂單金額', group: 'payment']
  createdAt  datetime2(0)   [not null, label: '建立時間', group: 'system']
  
  Note: 'ORD001 訂單主檔'
}

Ref: Order.customerId > Customer.customerId
```
