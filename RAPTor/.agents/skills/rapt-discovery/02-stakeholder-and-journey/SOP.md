# 02 Stakeholder & User Journey SOP

**目的**：從 source inventory 識別所有利害關係人（Stakeholder），並為每個主要角色描繪使用者旅程草圖。

---

## 步驟

### 2.1 DERIVE Stakeholder List

從 `${disc_dir}00-source-inventory.md` 及所有 source 中 DERIVE：

```
對每個 Stakeholder 記錄：
  - id: <lowercase-hyphen>       ← 對應未來 haARM actor.id
  - name: <中文名稱>
  - type: user | service | system | external
  - role_in_system: <一行描述>
  - key_concerns: [<3-5 項>]
  - pain_points: [<可選>]
```

**最少要有 2 個**；若少於 2 個，記 CiC `GAP`。

### 2.2 WRITE `${disc_dir}01-stakeholders.md`

```markdown
# Stakeholders

> 來源：(source 引用)

## 角色列表

| id | 名稱 | 類型 | 系統中的角色 |
|----|------|------|------------|
| ...| ...  | ...  | ...        |

## 各角色詳細描述

### {id} — {name}
- **類型**：{type}
- **系統角色**：{role_in_system}
- **主要關切**：...
- **痛點**：...
```

### 2.3 DERIVE User Journey

對每個**主要 user 類型**（非 service/system）的 Stakeholder，DERIVE：

```
使用者旅程 = 一系列業務事件的有序步驟
每個步驟：
  - 動作 (action)
  - 觸發條件 (trigger)
  - 預期結果 (outcome)
  - 對應系統功能（模糊描述即可，非技術語言）
```

### 2.4 WRITE `${disc_dir}02-user-journeys.md`

```markdown
# User Journeys

> 來源：(source 引用)

## {actor_name} 的主要旅程：{旅程名稱}

1. **{步驟名稱}**
   - 觸發：...
   - 動作：...
   - 預期結果：...
```

---

## 邊界規則

- **只描述業務流程，不涉及技術實作**（不寫 API endpoint / button click / form submit）
- **actor.id 要保持穩定**：後續 haARM 會引用，一旦確定不要輕易改
- 若 source 中角色描述不清楚：記 CiC `ASM`，標明假設的角色定義
