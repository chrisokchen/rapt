# 01 Story Extraction SOP

**目的**：從 Phase 1 discovery artifacts 萃取使用者故事（User Story），建立有序的故事清單，作為 Gherkin 生成的輸入。

---

## 步驟

### 1.1 READ Phase 1 Artifacts

```
READ: ${disc_dir}01-stakeholders.md
READ: ${disc_dir}02-user-journeys.md
READ: ${disc_dir}03-event-timeline.md
READ: ${disc_dir}04-vision-kpi-scope.md
```

### 1.2 SCAN Cross-Cutting Capabilities

LOAD REF [rapt-behavior::rules/cross-cutting-scenario-checklist.md]

從 discovery 的 scope、KPI、NFR、管理能力列表掃描共通能力：

- 匯入
- 匯出
- 篩選
- 排序
- 分頁
- 批次處理
- 錯誤格式
- 授權不足
- 部分成功 / 部分失敗
- 稽核記錄
- 清理 / 保留政策

對每個 module × capability 建立 matrix entry，承接方式只能是：

- `scenario`
- `common-dsl`
- `deferred`
- `out-of-scope`
- `open-cic`

若 discovery 明列能力但無法決定承接方式，記 CiC `GAP`。

### 1.3 DERIVE User Stories

對每個 User Journey 的每個步驟，DERIVE 一個或多個 User Story：

```
User Story 格式：
  As a <actor.id from stakeholders>
  I want to <業務目標>
  So that <業務價值>

附加：
  - priority: must-have | should-have | nice-to-have | out-of-scope
  - source_evidence: <引用的 journey 步驟>
  - domain_events: [<關聯的事件>]
```

規則：
- 每個 User Story 必須有 `source_evidence`（引用 journey 文件的具體步驟）
- priority 依 Vision/KPI/scope 判斷；無法判斷時記 CiC `ASM`
- out-of-scope 的 story 也要列出，用於後續驗證不遺漏

### 1.4 WRITE `${high_gherkin_dir}/story-index.md`（草稿）

```markdown
# User Story Index

> 最後更新：{date}
> 總計：{N} 個故事（must-have: {X}, should-have: {Y}, nice-to-have: {Z}）

## Must-Have

| 故事 ID | Actor | 目標 | 業務價值 | Feature 連結 |
|--------|-------|------|---------|------------|
| US-001 | ...   | ...  | ...     | (pending)  |

## Should-Have

...

## Out-of-Scope

...

## Cross-Cutting Capability Matrix

| module | capability | handling | feature/scenario | decision_ref | notes |
|---|---|---|---|---|---|
| 使用者管理 | 匯出 | scenario | (pending) |  |  |
```

---

## 邊界規則

- **User Story 只描述業務目標，不描述 UI 操作方式或技術路徑**
- actor 必須引用 `01-stakeholders.md` 中的 actor id
- 若 source 明確說「不做」的功能：歸入 out-of-scope，記錄原因
- scope 明列的共通能力不可消失；必須出現在 Cross-Cutting Capability Matrix
