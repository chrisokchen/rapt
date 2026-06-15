---
name: rapt-discovery
description: "RAPTor Phase 1 業務探索。讀取現有需求文件、會議記錄、RFP 等 source，產出 discovery 摘要（stakeholders、journey、events、vision/KPI/scope）。Use when: 開始一個新需求分析、/rapt-discovery、需要整理業務背景資料。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: planner
---

# RAPTor Discovery — Phase 1 業務探索

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::ssot-definition.md]
- LOAD REF [rapt-core::cic-note-policy.md]
- LOAD REF [rapt-core::phase-gates.md]

## TRIGGER

- ??????? `rapt-discovery` ??? RAPTor phase?
- ???? artifact ?????? phase ???????????????

## SKIP

- `.raptor/arguments.yml` ???????? `/rapt-kickoff`?
- ?????? worker ? DSL ????????? `rapt-form-*` skill?
- ??????? skill ? Artifact Output Contract?


## PRINCIPLE: CWD 為產出錨點
## PRINCIPLE: Artifact Output Contract（只寫 `${paths.business_discovery_dir}/**`）
## PRINCIPLE: STRICT SOP
## PRINCIPLE: 長流程待辦（Tier 0 / Tier 1）

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| CREATE / UPDATE | `${paths.business_discovery_dir}/**` | 所有 discovery 產出 |
| UPDATE | `.raptor/session.md` | 更新 Phase 1 進度 |
| **DENY** | DBML / haARM / Gherkin / haAPI / haPDL | 絕不觸碰規格 artifact |
| **DENY** | `generated/` | 不建立 generated artifacts |

---

## SOP

### 步驟 0：READ arguments.yml

```
READ: .raptor/arguments.yml
ASSERT: 存在，否則 EMIT 錯誤「請先執行 /rapt-kickoff」並停止
LOAD: paths.business_discovery_dir → 以下稱 ${disc_dir}
```

### 步驟 1：EXECUTE `01-source-intake/SOP.md`

讀取所有輸入 source 並建立 intake 摘要。

### 步驟 2：EXECUTE `02-stakeholder-and-journey/SOP.md`

識別角色並繪製使用者旅程草圖。

### 步驟 3：EXECUTE `03-event-storming-digest/SOP.md`

萃取業務事件並建立 event timeline。

### 步驟 4：EXECUTE `04-vision-kpi-scope/SOP.md`

確立 Vision、KPI、範圍邊界。

### 步驟 5：VALIDATE Phase 1 閘門

LOAD REF [rapt-core::phase-gates.md §Phase 1]

逐一檢查閘門條件，EMIT 通過/不通過摘要。  
未通過的項目：記 CiC `GAP`，並提示使用者補充資訊。

### 步驟 6：EMIT 完成通知

```
✅ Phase 1 Business Discovery 完成！

產出：
- ${disc_dir}00-source-inventory.md
- ${disc_dir}01-stakeholders.md
- ${disc_dir}02-user-journeys.md
- ${disc_dir}03-event-timeline.md
- ${disc_dir}04-vision-kpi-scope.md

品質閘門：PASS / PARTIAL（如有 GAP 請先處理）

建議下一步：執行 /rapt-behavior 產生高階 Gherkin
```
