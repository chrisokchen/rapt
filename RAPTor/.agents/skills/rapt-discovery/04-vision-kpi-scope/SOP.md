# 04 Vision, KPI & Scope SOP

**目的**：確立系統 Vision（遠景）、可量化 KPI（成功指標）、範圍邊界（in-scope / out-of-scope）。

---

## 步驟

### 4.1 DERIVE Vision Statement

從 source 萃取系統遠景：

```
Vision = 1-2 句話，描述系統解決什麼問題、對誰、達到什麼效果
格式：「本系統讓 <目標用戶> 能夠 <核心能力>，從而 <業務價值>」
```

若 source 中無明確 vision：記 CiC `GAP`，暫以最合理的假設 ASM 撰寫並標注。

### 4.2 DERIVE KPIs

從 source 萃取或推導可量化的成功指標：

```
每個 KPI：
  - name: <指標名稱>
  - description: <描述>
  - measurement: <如何量測>
  - baseline: <現況（如知）>
  - target: <目標值>
```

至少需要 2 個 KPI；否則記 CiC `GAP`。

### 4.3 DERIVE Scope Boundary

```
In-scope：本系統負責的功能範圍
Out-of-scope：明確排除的功能（含原因）
Deferred：現在不做，未來可能做的功能
Dependencies：依賴的外部系統或服務
```

### 4.4 ASK（若 scope 不明確）

若 source 中有 scope 衝突或空白：

```
ASK：
  1. <功能 X> 是否在本系統範圍內？（請以 是/否/待議 回答）
  2. 有哪些外部系統需要對接？
  3. 上線時程（影響 deferred 項目判斷）
```

（最多問 3 題，符合 clarify_batch_size 上限）

### 4.5 WRITE `${disc_dir}04-vision-kpi-scope.md`

```markdown
# Vision, KPI & Scope

> 來源：(source 引用)

## Vision

> {vision statement}

## KPI — 成功指標

| # | 指標 | 量測方式 | 基準值 | 目標值 |
|---|------|---------|-------|-------|
| 1 | ...  | ...     | ...   | ...   |

## 範圍邊界

### In-Scope（本系統負責）
- ...

### Out-of-Scope（明確排除）
- ...

### Deferred（未來版本）
- ...

### 外部依賴
- ...
```

---

## Phase 1 閘門自我檢查

執行完本步驟後，對照 `rapt-core::phase-gates.md §Phase 1` 自我驗核：

```
□ 至少一份 discovery 文件已讀取並摘要
□ Stakeholder list 存在（至少 2 個角色）
□ Event timeline 存在
□ Vision statement 存在
□ 至少 2 個 KPI
□ 範圍邊界明確
```

未通過者記 CiC `GAP`。
