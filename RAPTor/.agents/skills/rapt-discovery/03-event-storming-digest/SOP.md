# 03 Event Storming Digest SOP

**目的**：從 source 萃取業務事件（Domain Events），建立 event timeline，識別 commands、aggregates 的初步輪廓。

---

## 步驟

### 3.1 DERIVE Domain Events

從所有 source 文件萃取：

```
Domain Event = 業務上發生過的重要事實（過去式動詞）
格式：<Actor> <動詞-過去式> <業務物件>
範例：「客戶提交了訂單」、「管理員審核了退款申請」
```

規則：
- 每個事件用**正體中文過去式**描述（英文亦可，但要保持一致）
- 每個事件標注觸發的 actor（引用 `01-stakeholders.md` 的 id）
- 盡量窮舉，不要篩選（先廣後收）

### 3.2 DERIVE Commands

對每個 Domain Event，反推觸發它的 Command（使用者意圖）：

```
Command = 觸發 Domain Event 的使用者指令（現在式）
範例：「提交訂單」觸發「訂單已提交」
```

### 3.3 CLUSTER events 為 Bounded Context 候選

對所有 events DERIVE 初步分群（不強制——粗分即可）：

```
群組名稱 → [event1, event2, ...]
```

**注意**：這是初步分群，不是最終 Bounded Context 定義（Phase 2 才確立）。

### 3.4 WRITE `${disc_dir}03-event-timeline.md`

```markdown
# Event Timeline

> 來源：(source 引用)
> 方法：Event Storming 輕量版

## Domain Events（時序排列）

| # | 事件 | Actor | 前置條件 | 後置狀態 |
|---|------|-------|---------|---------|
| 1 | ...  | ...   | ...     | ...     |

## Commands

| Command | 觸發的 Event |
|---------|------------|
| ...     | ...        |

## 初步 Bounded Context 分群（草圖）

### {群組名稱}
- Events: [...]
- 可能的 Aggregate: [...]
```

---

## 邊界規則

- **只做業務層分析**：不寫資料庫 Table / API / UI
- 若事件清單少於 5 個：記 CiC `GAP`（source 可能不足，需更多資料）
- 若有事件的 actor 無法對應到 Stakeholder：記 CiC `ASM`，標明假設
