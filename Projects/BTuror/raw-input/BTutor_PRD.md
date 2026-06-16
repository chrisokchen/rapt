# 產品需求文件（PRD）

# Bridge Cognitive Tutor — Entry Management Tutor MVP

版本：0.1
日期：2026-05-18
狀態：Draft

---

# 1. 產品概述

## 產品名稱

Bridge Cognitive Tutor

MVP 聚焦：

> Entry Management Tutor（橋引管理教練）

---

# 2. 產品願景

Bridge Cognitive Tutor 是一套：

> AI 驅動、可診斷、可解釋的橋牌認知學習系統。

系統核心不是判定玩家「有沒有打對」，而是理解：

> 玩家是如何思考、在哪個認知環節失敗、以及如何真正形成 transferable bridge cognition。

系統結合：

* Cognitive Ontology（認知本體）
* Situation IR（局面中介表示）
* Evidence-based Diagnosis（基於證據的診斷）
* Probabilistic Student Model（機率式學生模型）
* Adaptive Tutoring（自適應教學）
* Explainable AI Coaching（可解釋 AI 教學）

建立一套 Intelligent Tutoring System（ITS）導向的橋牌認知學習平台。

---

# 3. 問題定義

## 現有橋牌教學系統的問題

### 3.1 靜態教學

現有系統多半：

* 只提供固定教材
* 著重 convention 與答案
* 缺乏認知診斷能力

---

### 3.2 缺乏 Cognitive Diagnosis

大多數系統只能知道：

> 玩家有沒有答對。

但不知道：

> 玩家為什麼會失敗。

例如：

同樣錯失 finesse，可能來自：

* counting failure
* entry mismanagement
* danger hand 誤判
* planning horizon 不足
* probability calibration 錯誤

---

### 3.3 缺乏 Transfer Validation

玩家容易：

* 記住牌例
* 背答案
* 學會 pattern matching

卻沒有真正形成：

> transferable bridge cognition。

---

### 3.4 人類教練成本高

真人教練大量時間花在：

* 找題目
* 分析錯誤
* 追蹤學生進度
* 判定弱點

而非：

* 高層策略
* 心理素質
* bridge thinking
* partnership understanding

---

# 4. 產品目標

## 主要目標

建立一套：

> 可解釋、可診斷、可追蹤 cognition evolution 的 Declarer Play Tutor。

---

## 次要目標

* 建立 bridge cognitive ontology
* 追蹤長期 mastery evolution
* 支援 transfer validation
* 提供教練分析工具
* 建立可重播（replayable）的學習事件系統
* 形成 bridge cognition telemetry dataset

---

# 5. MVP 範圍

## 5.1 MVP Domain

第一版僅支援：

* Declarer Play
* Entry Management

不處理：

* bidding
* defense
* partnership coordination
* multiplayer interaction

---

## 5.2 MVP 核心功能

### 1. Curated Deal Practice

提供人工 curated 的 Entry Management 訓練牌例。

---

### 2. Action Trace 收集

系統記錄：

```yaml
action_trace:
  selected_card
  legal_cards
  think_time_ms
  undo_count
```

用途：

* hesitation analysis
* planning stability
* cognitive load estimation
* diagnosis evidence

---

### 3. Reasoning Tags

玩家可選擇 reasoning tags：

```yaml
reasoning_tags:
  - counting
  - entry preservation
  - planning
  - probability
  - danger hand
```

作為 diagnosis 輔助訊號。

---

### 4. Graduated Hint System

系統採用漸進式提示：

```text
Level 0 — 無提示
Level 1 — Directional cue
Level 2 — Localized cue
Level 3 — Partial reveal
Level 4 — Full explanation
```

Hint escalation 本身也作為 cognition signal。

---

### 5. Evidence-based Diagnosis

系統產生：

* diagnosis hypothesis
* confidence
* supporting evidence
* rule references

範例：

```yaml
diagnosis:
  hypothesis: entry_management_failure
  confidence: 0.72
  evidence:
    - spent_only_entry
    - failed_transfer_variant
```

---

### 6. Mastery Tracking

系統追蹤：

* recognition
* execution
* transfer
* retention

而非單純答對率。

---

### 7. Post-Mortem Coaching

每副牌結束後：

* cognitive diagnosis
* coaching explanation
* misconception analysis
* suggested next training

---

### 8. Coach Dashboard

教練可查看：

* misconception trends
* mastery evolution
* transfer failures
* hint dependency
* cognitive progress

---

# 6. MVP 不包含項目

## Out of Scope

第一版不做：

* bidding tutor
* defense tutor
* multiplayer
* partnership modeling
* free-form AI chat
* autonomous ontology evolution
* eye tracking
* biometric telemetry
* fully automatic deal generation
* deep embeddings-first architecture

---

# 7. 目標使用者

## 7.1 Primary Users

### 中級卡關玩家

特徵：

* 概念知道很多
* 實戰不穩
* planning 弱
* transfer 能力不足
* 容易「上課都懂、打牌不會」

---

## 7.2 Secondary Users

### MiniBridge / Junior Learners

重點：

* planning habit
* counting habit
* declarer cognition foundation
* attention control

---

## 7.3 Human Coaches

用途：

* progress review
* targeted assignment
* misconception diagnosis
* learning analytics

---

# 8. 產品哲學

## 核心理念

```text
AI 不替玩家思考。
AI 幫助理解玩家如何思考。
```

---

## Learning Philosophy

系統測量的是：

> cognitive transfer

而不是：

> pattern memorization。

---

## AI Philosophy

```text
LLM 負責 explain hypothesis。
LLM 不負責決定 diagnosis truth。
```

---

# 9. 系統架構

## High-Level Architecture

```text
Curated Deal
    ↓
Bridge Situation DSL
    ↓
Situation IR
    ↓
Evidence-based Diagnosis
    ↓
Probabilistic Student Model
    ↓
LLM Explanation Layer
```

---

# 10. Cognitive Ontology

## 第一版 Ontology Scope

聚焦於 Entry Management：

* entry recognition
* entry preservation
* sequencing
* unblock awareness
* communication planning
* delayed cashing

---

## Mastery Representation

```yaml
skill:
  recognition:
  execution:
  transfer:
  retention:
```

---

# 11. Bridge Situation DSL

## 定位

Bridge Situation DSL 為：

> 全系統的 cognition intermediate representation。

---

## MVP 功能

### Situation Annotation

描述：

* critical moments
* required skills
* acceptable lines
* common mistakes
* misconception patterns

---

### Diagnosis Rules

定義：

* evidence mapping
* rule conditions
* hint strategies
* mistake taxonomy

---

## 未來擴充

未來將支援：

* constraint-based generation
* adaptive curriculum generation
* situation family generation
* transfer validation generation

---

# 12. Diagnosis System

## Diagnosis Strategy

採用 Hybrid Architecture：

* Rule-based diagnosis
* Probabilistic student model
* LLM explanation layer

---

## Diagnosis Principles

### Explainable

所有 diagnosis 必須包含：

* evidence
* confidence
* supporting rules

---

### Auditable

所有 diagnosis 必須 replayable。

---

### Non-Binary

Bridge mistakes 不只有單一正解。

允許：

* multiple acceptable lines
* practical bridge tradeoffs
* IMP / MP / BAM context differences

---

# 13. Mistake Taxonomy

第一版分類：

* planning failure
* entry mismanagement
* counting failure
* inference failure
* probability miscalibration
* tempo error
* practical overoptimization

---

# 14. Telemetry Strategy

## MVP Signals

```text
action trace
timing
hint escalation
reasoning tags
```

---

## 不收集

第一版不收：

* eye tracking
* biometric data
* mouse path telemetry
* free-form chain-of-thought

---

# 15. Replay System

## 核心原則

所有核心 object versioned：

* ontology
* DSL
* rule sets
* mastery models

並保留：

# Reproducible Replay

---

## Replay 用途

### Debug Replay

重新分析 diagnosis。

---

### Research Replay

比較不同 ontology/rule set。

---

### Mastery Replay

重新計算學生 mastery trajectory。

---

# 16. Ontology Governance

## 治理模式

```text
AI suggests
Human approves
```

---

## Governance Workflow

```text
Telemetry
 → Pattern Mining
   → AI Proposal
     → Human Review
       → Replay Validation
         → Deployment
```

---

# 17. Tutor Explanation Layer

## Explanation Strategy Layer

Diagnosis truth 固定。

Pedagogy 可變。

---

## Dynamic Adaptation

依據：

* 年齡
* mastery
* frustration
* fatigue
* coach preference

動態調整：

* wording
* terminology density
* emotional tone
* Socratic depth

---

# 18. Success Metrics

## Learning Metrics

系統評估：

* transfer success
* hint independence
* planning sophistication
* misconception reduction
* retention stability

---

## Non-Goals

不以：

* solve rate
* streaks
* raw DDS accuracy

作為主要 success metric。

---

# 19. 長期護城河（Moat）

核心資產：

* Cognitive Ontology
* Longitudinal Telemetry
* Diagnosis Evidence Graph
* Mastery Evolution Trajectories

---

# 20. 最終產品定位

Bridge Cognitive Tutor 最終目標不是：

* 題庫
* chatbot
* DDS UI

而是：

# Bridge Cognitive Operating System

---

# 21. MVP 最終架構

```text
Entry Management Tutor
    ↓
Curated Deal Families
    ↓
Bridge Situation DSL
    ↓
Situation IR
    ↓
Evidence-based Diagnosis
    ↓
Probabilistic Student Model
    ↓
Graduated Hint System
    ↓
LLM Explanation Layer
    ↓
Mastery Tracking
    ↓
Coach Dashboard
```

---

# 22. 核心總結

```text
系統不是測記憶。

系統測的是：
Bridge Cognition Transfer。
```

```text
真正的 moat：
不是 prompt engineering。

而是：
longitudinal bridge cognition telemetry。
```
