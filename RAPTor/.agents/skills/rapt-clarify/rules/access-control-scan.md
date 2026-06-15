# 存取控制掃描規則（C1-C3）

本文件定義 `rapt-clarify/01-gap-scan` 對 haARM 存取控制執行的結構性掃描規則。

---

## C1：haARM resource 必須對應 DBML Table

```
規則：haARM 中每個 resource.id 必須能 case-insensitive 對應一個 DBML Table Name
嚴重度：ERROR
處理：
  - 若 resource.id 有對應 Table（大小寫不同）→ CREATE CiC ASM，建議統一命名
  - 若 resource.id 無對應任何 Table → CREATE CiC GAP，可能是遺漏的 Table 或錯誤命名
```

**掃描方法**：
1. READ schema.dbml → COLLECT all Table Names（lowercase set）
2. READ *.haarm.yaml → COLLECT all resource.id（lowercase）
3. 找出 haARM resource 中無對應 DBML Table 的項目

---

## C2：end-user role 不應有 scope: all（AP-04）

```
規則：識別為 end-user 的 role，其關聯的 permission 不得有 scope: all
嚴重度：ERROR
處理：CREATE CiC BDY，需要 rapt-clarify（語意決策）解決
```

**end-user 識別方式**：
- actor type = `user`（不是 service / system / external）
- role 沒有 `admin` / `sysadm` / `system` 等管理詞彙
- role 在 Discovery stakeholders 中被描述為一般使用者

---

## C3：haARM role 應覆蓋所有 Stakeholder actor

```
規則：Discovery 中識別的每個 user type actor，haARM 應有對應的 role
嚴重度：WARNING
處理：CREATE CiC ASM，標明可能遺漏的 role
```

**掃描方法**：
1. READ `${disc_dir}01-stakeholders.md` → COLLECT user type actors
2. READ *.haarm.yaml → COLLECT role.id
3. 找出 Stakeholder actor 中沒有對應 role 的

---

## C4（額外）：haARM permission.id 命名一致性

```
規則：permission.id 應遵循 {resource_id}_{action} 命名慣例
嚴重度：WARNING（建議，非強制）
處理：CREATE CiC ASM，建議規範化命名
```

---

## 掃描輸出格式

```markdown
## 結構掃描發現（存取控制 C1-C3）

| 規則 | 位置 | 問題 | 嚴重度 | 建議 |
|------|------|------|-------|------|
| C1 | shop.haarm.yaml#resource:cartItem | 無對應 DBML Table 'cartItem' | ERROR | 確認是 CartItem 還是 OrderItem |
| C2 | shop.haarm.yaml#permission:order_read_all | customer role 使用 scope:all | ERROR | 改為 scope:own + conditions |
| C3 | 01-stakeholders.md | Stakeholder 'supplier' 在 haARM 無對應 role | WARNING | 需添加 supplier role |
```
