# DBML 速查卡 v3.3

> 1 頁 A4 列印；完整規格見 [`annotated_DBML-v3.3.md`](annotated_DBML-v3.3.md)；跨 DSL 整合見 [`CROSS-DSL-GUIDE.md`](CROSS-DSL-GUIDE.md)

## 1. 最小檔案結構（DBML 本體語法見 [dbml.dbdiagram.io](https://dbml.dbdiagram.io)）

```dbml
Table InfoUser {
  userId   nvarchar(60)  [pk, label: '使用者帳號', group: 'basic']
  password nvarchar(150) [not null, sensitive: true, label: '密碼']
  email    nvarchar(50)  [sensitive: true, label: '電子郵件']
  deptId   nvarchar(20)  [label: '部門ID']
  status   nchar(1)      [not null, default: 'Y', ref_code: 'YesNo', label: '狀態']

  Note: 'HT002 使用者主檔'
}

Ref: InfoUser.deptId > Dept.deptId   // 外鍵關聯
```

## 2. v3.3 一級標註（Q9 收編為一級語法）

| 標註 | 型別 | 預設 | 用途 |
|------|------|------|------|
| `label:` | string | 推斷字典 / Capitalize | UI 顯示標籤（取代硬編碼字典）|
| `ref_code:` | string | 無 | CodeMain 動態列舉來源 key（自動生成 select + JOIN）|
| `sensitive:` | boolean | `false` | 敏感欄位（auto mask / password input）|
| `group:` | string | 推斷 / null | 欄位邏輯分組（haPDL groups 可覆寫）|

```dbml
order_number varchar(50) [unique, not null, label: '訂單編號', group: 'basic']
user_type    nchar(1)    [not null, ref_code: 'UserType', label: '使用者類別']
password     varchar(255) [not null, sensitive: true, label: '密碼']
```

> v3.3 起 `haPDL/hapdl_converter/dbml_parser.py` 原生支援；對其他 DBML 工具（dbdiagram.io 等）保持向前相容（未識別屬性會被忽略）。

## 3. DBML 標準屬性

| 屬性 | 範例 | 語義 |
|------|------|------|
| `pk` | `id integer [pk]` | 主鍵 |
| `not null` | `name varchar [not null]` | 非空 |
| `unique` | `email varchar [unique]` | 唯一 |
| `default:` | `status nchar(1) [default: 'Y']` | 預設值 |
| `note:` | `[note: '訂單編號']` | 開發者文件 |
| `ref: >` | `[ref: > Dept.deptId]` | 外鍵指向 |

## 4. Resolution Order（Convention 查找優先序）

| 屬性 | 查找順序（高 → 低）|
|------|------------------|
| **label** | haPDL columns label > DBML `label:` > 推斷字典 > `Capitalize(field_name)` |
| **input type** | haPDL `:type` > DBML enum/type > `infer_input_type()` |
| **sensitive** | DBML `sensitive: true` > 名稱含 password/secret/id_number 推斷 > false |
| **ref_code** | DBML `ref_code:` 唯一來源（無推斷 fallback）|
| **group** | haPDL `groups:` > DBML `group:` > `infer_field_group()` |

## 5. 跨 DSL 引用點

| 從 | 到 | 用途 |
|----|----|------|
| DBML `Table <Name>` | haARM `resource.id`（case-insensitive）| RBAC 對應 |
| DBML `Table <Name>` | haAPI `entity:` | API 對應實體 |
| DBML Column 名稱 | haARM `resource.fields[]` + condition.field | 欄位級權限 |
| DBML `ref: >` | haAPI virtual_relations | 子查詢計數 |
| DBML `ref_code:` | haAPI LEFT JOIN CodeMain、haPDL select options | 動態列舉 |
| DBML `label:` / `group:` / `sensitive:` | haPDL columns / form input 自動推斷 | UI 預設 |

## 6. v3.3 反模式（§9.5）

| 編號 | 反模式 | 修正 |
|------|--------|------|
| AP-01 | 用 `note: 'label:訂單編號\|group:basic'` 嵌入子格式 | 改用一級語法：`[label: '...', group: '...']` |
| AP-02 | 同欄位 `ref_code:` 與 `ref: >` 並存 | 二擇一：值集合用 `ref_code:`、關聯實體用 `ref:` |
| AP-03 | 顯式寫 `sensitive: false` | 省略；預設即 false |
| AP-04 | DBML 與 haPDL 重複寫同名 group | DBML 一次；haPDL 僅在頁面層次重排時寫 |
| AP-05 | 把 UI 偏好（color/icon/display_type）寫進 DBML | 放 haPDL，DBML 只留資料本質屬性 |

## 7. 常用 CLI

```bash
# haPDL 工具鏈解析 DBML（v3.3 支援 4 個一級標註）
hapdl convert <file>.hapdl.yaml --dbml schema.dbml -o output.pdl.yaml

# 跨 DSL 引用驗證（檢查 haARM/haAPI 引用的 Table/Field 都存在）
python benchmarks/validate_cross_dsl.py <anchor>

# 測試 parser 對新標註的支援
cd haPDL && python test_converter.py
```

## 8. 完整範例（含 v3.3 一級標註）

```dbml
Table InfoUser {
  userId    nvarchar(60)  [pk, label: '使用者帳號', group: 'basic']
  password  nvarchar(150) [not null, sensitive: true, label: '密碼', group: 'basic']
  userName  nvarchar(60)  [not null, label: '使用者名稱', group: 'basic']
  userType  nvarchar(1)   [not null, ref_code: 'UserType', label: '使用者類別']
  deptId    nvarchar(20)  [label: '部門ID', group: 'basic']
  email     nvarchar(50)  [sensitive: true, label: '電子郵件', group: 'contact']
  telephone nvarchar(30)  [sensitive: true, label: '聯絡電話', group: 'contact']
  status    nchar(1)      [not null, default: 'Y', ref_code: 'YesNo', label: '帳號狀態']

  Note: 'HT002 使用者主檔'
}

Ref: InfoUser.deptId > Dept.deptId
```

---
**版本**：v3.3.0｜**對齊**：四 DSL v3.3｜**最後更新**：2026-05-14
