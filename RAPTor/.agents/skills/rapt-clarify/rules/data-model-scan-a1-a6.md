# 資料模型掃描規則（A1-A6）

本文件定義 `rapt-clarify/01-gap-scan` 對 DBML 資料模型執行的結構性掃描規則。

---

## A1：每個 Table 必須有 PK

```
規則：DBML Table 至少有一個 [pk] 欄位
嚴重度：ERROR
處理：CREATE CiC GAP，提醒設計者定義主鍵
```

**掃描方法**：SEARCH 所有 Table，若無任何 `[pk` 屬性，記 CiC GAP。

---

## A2：每個 Column 建議有 label

```
規則：所有欄位（除系統欄位如 createdAt, updatedAt）應有 label:
嚴重度：WARNING
處理：CREATE CiC ASM，標明推斷的 label 值，請使用者確認
```

**掃描方法**：SEARCH 所有欄位的屬性，若無 `label:`，記 CiC ASM 並附推斷值。

---

## A3：狀態碼類欄位應有 ref_code

```
規則：欄位名稱含 status / type / kind / category / level，型別為 nchar(1) 或 nvarchar(1-5)，應有 ref_code:
嚴重度：WARNING
處理：CREATE CiC ASM，提醒可能需要動態列舉
```

**排除**：明確是 boolean（bit 型別）或 PK 的欄位不在此規則範圍。

---

## A4：外鍵應有 Ref 宣告

```
規則：欄位名稱以 Id / Code 結尾，且型別與引用 Table PK 一致，應有 Ref: 宣告
嚴重度：WARNING
處理：CREATE CiC ASM，標明推斷的 Ref 引用
```

**例外**：若 Code 欄位是 ref_code（引用 CodeMain），則不需要 Ref。

---

## A5：密碼/敏感欄位應標注 sensitive: true

```
規則：欄位名稱含 password / secret / token / id_number / passport / credit，應有 sensitive: true
嚴重度：ERROR
處理：直接建議修正（可自動套用 rapt-reconcile）
```

**注意**：email 和 phone 也建議 sensitive: true，但嚴重度為 WARNING。

---

## A6：group 不應在 DBML 和 haPDL 重複定義（AP-04）

```
規則：若 DBML 某欄位有 group:，對應的 haPDL 欄位不應再定義同名 group
嚴重度：WARNING（僅在 haPDL 存在後才可掃描）
處理：CREATE CiC ASM，確認哪個版本為準
```

---

## 掃描輸出格式

```markdown
## 結構掃描發現（資料模型 A1-A6）

| 規則 | 位置 | 問題 | 嚴重度 | 建議 |
|------|------|------|-------|------|
| A1 | schema.dbml#Payment | Table Payment 無 PK | ERROR | 定義 paymentId 為 PK |
| A2 | schema.dbml#Order.remark | Order.remark 缺 label | WARNING | label: '備註' |
| A5 | schema.dbml#User.password | password 欄位缺 sensitive: true | ERROR | 添加 sensitive: true |
```
