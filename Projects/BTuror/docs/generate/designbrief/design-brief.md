# Bridge Cognitive Tutor UI Design Brief

> **Purpose**: This document is a structured design brief auto-generated from
> `haPDL` (page intent specs) + `schema.dbml` (data model) + `haARM` (access control).
> Feed this entire document to **Claude Design** or any AI design tool to generate
> Hi-Fi mockups, HTML, or React component code.
>
> **System**: AI 驅動、可診斷、可解釋的橋牌認知學習系統；MVP 聚焦 Entry Management Tutor（橋引管理教練）。
> **Language**: Traditional Chinese (zh-TW)
> **Target framework**: React + Ant Design (or shadcn/ui)

---


## Design System

> Use this as the global design language for all pages.

### Color Palette

| Token | Value | Usage |
|:---|:---|:---|
| `--primary` | `#2563eb` (Blue 600) | Primary buttons, links, active states |
| `--primary-hover` | `#1d4ed8` (Blue 700) | Hover state |
| `--success` | `#16a34a` (Green 600) | Approve actions, success states |
| `--danger` | `#dc2626` (Red 600) | Delete, reject actions |
| `--warning` | `#d97706` (Amber 600) | Warnings, adjust actions |
| `--bg-page` | `#f8fafc` (Slate 50) | Page background |
| `--bg-card` | `#ffffff` | Card/panel backgrounds |
| `--bg-header` | `#1e293b` (Slate 800) | Top navigation / sidebar |
| `--border` | `#e2e8f0` (Slate 200) | Borders, dividers |
| `--text-primary` | `#0f172a` (Slate 900) | Headings, labels |
| `--text-secondary` | `#64748b` (Slate 500) | Descriptions, hints |
| `--badge-blue` | `#dbeafe` bg / `#1e40af` text | Status badges (info) |
| `--badge-green` | `#dcfce7` bg / `#166534` text | Status badges (success) |
| `--badge-amber` | `#fef3c7` bg / `#92400e` text | Status badges (warning) |
| `--badge-red` | `#fee2e2` bg / `#991b1b` text | Status badges (danger) |
| `--badge-gray` | `#f1f5f9` bg / `#475569` text | Status badges (neutral) |

### Typography

| Element | Font | Size | Weight |
|:---|:---|:---|:---|
| Page title | Noto Sans TC | 20px | 700 |
| Section heading | Noto Sans TC | 16px | 600 |
| Table header | Noto Sans TC | 13px | 600 |
| Body text | Noto Sans TC | 14px | 400 |
| Label | Noto Sans TC | 13px | 600 |
| Badge | JetBrains Mono | 12px | 500 |
| Button | Noto Sans TC | 14px | 500 |
| Hint/caption | Noto Sans TC | 12px | 400 |

### Spacing

| Token | Value |
|:---|:---|
| Page padding | 24px |
| Card padding | 20px |
| Form field gap | 16px |
| Table cell padding | 12px 16px |
| Button padding | 8px 20px |
| Border radius (card) | 8px |
| Border radius (button) | 6px |
| Border radius (input) | 6px |
| Border radius (badge) | 4px |

### Component Library (reference)

Use **Ant Design** or **shadcn/ui** component patterns:
- Table: sortable headers, row hover, row actions menu
- Form: label-left layout (label 120px, input flex-1), validation messages
- Select: searchable dropdown with Chinese labels
- DatePicker: range selector for date fields
- Badge: colored status badge with icon
- Button: primary / secondary / ghost / danger variants
- Modal: confirmation dialogs for destructive actions
- Breadcrumb: for navigation context
- Sidebar: collapsible left navigation

### Layout Structure

```
+------------------------------------------+
| Top Nav (dark bg, logo, user menu)       |
+--------+---------------------------------+
| Side   | Breadcrumb                      |
| Nav    +---+-----------------------------+
|        |   | Page Title        [Actions]  |
|        |   +-+---------------------------+
|        |   | | Filter Bar                 |
|        |   | +---------------------------+
|        |   | | Content (Table/Form/Detail)|
|        |   | +---------------------------+
|        |   | | Pagination / Footer        |
+--------+---+-----------------------------+
```

## Page Navigation Map

```
Sidebar Navigation:

  [assignment]
    ✏ 派發訓練
    ☰ 訓練指派清單
  [student-skill-state]
    · 教練認知儀表板
    · 孩子認知進展
    📄 我的認知精熟度
  [cognitive-skill]
    ☰ 認知技能清單
  [curated-deal]
    ✏ 建立 / 編輯牌例
    ☰ 牌例清單
  [diagnosis]
    📄 賽後認知診斷
  [ontology-proposal]
    ☰ 本體演化提案
  [play-session]
    📄 橋引管理練習
  [replay-run]
    ☰ 重播紀錄
  [situation-annotation]
    ✏ 局面標注
```

### Page Flow

```
訓練指派清單 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

認知技能清單 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

牌例清單 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

本體演化提案 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

重播紀錄 (list)
  ├── [+ 新增] → (form)
  ├── [檢視]   → (detail)
  └── [編輯]   → (form, edit mode)

派發訓練 (form)
  └── [送出/核准] → back to list

建立 / 編輯牌例 (form)
  └── [送出/核准] → back to list

局面標注 (form)
  └── [送出/核准] → back to list

賽後認知診斷 (detail)

橋引管理練習 (detail)
  ├── [request_hint] → action
  ├── [tag_reasoning] → action

我的認知精熟度 (detail)

```

## Page Specifications

### Page 1: 派發訓練

| Property | Value |
|:---|:---|
| Page ID | `assignment-form` |
| Type | **FORM** |
| Entity | `Assignment` |
| Primary Actor |  |
| Allowed Roles | 教練 |
| Source | `assignment-form.hapdl.yaml` |

#### Form Fields

| # | Field | Label | Widget | Required | Sensitive | Options / Constraints | Sample Value |
|:---|:---|:---|:---|:---|:---|:---|:---|

#### Form Layout

- **Layout**: Label-left, 2-column for short fields (text, select, date), full-width for textarea
- **Grouping**: Group by DBML `group` attribute if available
- **Validation**: Show inline error messages below each field
- **Sensitive fields**: Show a lock icon and mask input by default, with a toggle to reveal

#### Footer Actions


#### Interaction Notes



---

### Page 2: 訓練指派清單

| Property | Value |
|:---|:---|
| Page ID | `assignment-list` |
| Type | **LIST** |
| Entity | `Assignment` |
| Primary Actor |  |
| Allowed Roles | 教練 |
| Source | `assignment-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `studentId` | 學生 | Text input | Free text |
| `targetSkillId` | 目標認知缺口技能 | Text input | Free text |
| `status` | 指派狀態 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `assignmentId` | 指派編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `studentId` | 學生 | text | - | `學生-1`, `學生-2`, `學生-3` |
| 3 | `dealId` | 指派牌例 | text | - | `指派牌例-1`, `指派牌例-2`, `指派牌例-3` |
| 4 | `targetSkillId` | 目標認知缺口技能 | text | - | `目標認知缺口技能-1`, `目標認知缺口技能-2`, `目標認知缺口技能-3` |
| 5 | `status` | 指派狀態 | badge | - | `指派狀態-1`, `指派狀態-2`, `指派狀態-3` |
| 6 | `assignedAt` | 指派時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

#### Status Badge Color Mapping

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "assignmentId": "ID-0001",
    "studentId": "學生-1",
    "dealId": "指派牌例-1",
    "targetSkillId": "目標認知缺口技能-1",
    "status": "指派狀態-1",
    "assignedAt": "2026-06-01 09:00"
  },
  {
    "assignmentId": "ID-0002",
    "studentId": "學生-2",
    "dealId": "指派牌例-2",
    "targetSkillId": "目標認知缺口技能-2",
    "status": "指派狀態-2",
    "assignedAt": "2026-06-02 09:00"
  },
  {
    "assignmentId": "ID-0003",
    "studentId": "學生-3",
    "dealId": "指派牌例-3",
    "targetSkillId": "目標認知缺口技能-3",
    "status": "指派狀態-3",
    "assignedAt": "2026-06-03 09:00"
  }
]
```


---

### Page 3: 教練認知儀表板

| Property | Value |
|:---|:---|
| Page ID | `coach-dashboard` |
| Type | **DASHBOARD** |
| Entity | `StudentSkillState` |
| Primary Actor |  |
| Allowed Roles | 教練 |
| Source | `coach-dashboard.hapdl.yaml` |


---

### Page 4: 認知技能清單

| Property | Value |
|:---|:---|
| Page ID | `cognitive-skill-list` |
| Type | **LIST** |
| Entity | `CognitiveSkill` |
| Primary Actor |  |
| Allowed Roles | 標注者 |
| Source | `cognitive-skill-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `ontologyVersion` | 所屬本體版本 | Text input | Free text |
| `cognitiveLevel` | 認知層級 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `skillCode` | 技能代碼 | link | Yes | `技能代碼-1`, `技能代碼-2`, `技能代碼-3` |
| 2 | `skillName` | 技能名稱 | text | - | `技能名稱-1`, `技能名稱-2`, `技能名稱-3` |
| 3 | `cognitiveLevel` | 認知層級 | badge | - | `認知層級-1`, `認知層級-2`, `認知層級-3` |
| 4 | `ontologyVersion` | 所屬本體版本 | text | - | `所屬本體版本-1`, `所屬本體版本-2`, `所屬本體版本-3` |

#### Status Badge Color Mapping

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "skillCode": "技能代碼-1",
    "skillName": "技能名稱-1",
    "cognitiveLevel": "認知層級-1",
    "ontologyVersion": "所屬本體版本-1"
  },
  {
    "skillCode": "技能代碼-2",
    "skillName": "技能名稱-2",
    "cognitiveLevel": "認知層級-2",
    "ontologyVersion": "所屬本體版本-2"
  },
  {
    "skillCode": "技能代碼-3",
    "skillName": "技能名稱-3",
    "cognitiveLevel": "認知層級-3",
    "ontologyVersion": "所屬本體版本-3"
  }
]
```


---

### Page 5: 建立 / 編輯牌例

| Property | Value |
|:---|:---|
| Page ID | `curated-deal-form` |
| Type | **FORM** |
| Entity | `CuratedDeal` |
| Primary Actor |  |
| Allowed Roles | 標注者 |
| Source | `curated-deal-form.hapdl.yaml` |

#### Form Fields

| # | Field | Label | Widget | Required | Sensitive | Options / Constraints | Sample Value |
|:---|:---|:---|:---|:---|:---|:---|:---|

#### Form Layout

- **Layout**: Label-left, 2-column for short fields (text, select, date), full-width for textarea
- **Grouping**: Group by DBML `group` attribute if available
- **Validation**: Show inline error messages below each field
- **Sensitive fields**: Show a lock icon and mask input by default, with a toggle to reveal

#### Footer Actions


#### Interaction Notes



---

### Page 6: 牌例清單

| Property | Value |
|:---|:---|
| Page ID | `curated-deal-list` |
| Type | **LIST** |
| Entity | `CuratedDeal` |
| Primary Actor |  |
| Allowed Roles | 標注者 |
| Source | `curated-deal-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `situationType` | situationType | Text input | Free text |
| `declarer` | 莊家方位 | Text input | Free text |
| `scoringContext` | 計分制 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `dealId` | 牌例編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `title` | 牌例標題 | text | - | `牌例標題-1`, `牌例標題-2`, `牌例標題-3` |
| 3 | `declarer` | 莊家方位 | badge | - | `莊家方位-1`, `莊家方位-2`, `莊家方位-3` |
| 4 | `scoringContext` | 計分制 | text | - | `計分制-1`, `計分制-2`, `計分制-3` |
| 5 | `createdAt` | 建立時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

#### Status Badge Color Mapping

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "dealId": "ID-0001",
    "title": "牌例標題-1",
    "declarer": "莊家方位-1",
    "scoringContext": "計分制-1",
    "createdAt": "2026-06-01 09:00"
  },
  {
    "dealId": "ID-0002",
    "title": "牌例標題-2",
    "declarer": "莊家方位-2",
    "scoringContext": "計分制-2",
    "createdAt": "2026-06-02 09:00"
  },
  {
    "dealId": "ID-0003",
    "title": "牌例標題-3",
    "declarer": "莊家方位-3",
    "scoringContext": "計分制-3",
    "createdAt": "2026-06-03 09:00"
  }
]
```


---

### Page 7: 賽後認知診斷

| Property | Value |
|:---|:---|
| Page ID | `diagnosis-detail` |
| Type | **DETAIL** |
| Entity | `Diagnosis` |
| Primary Actor |  |
| Allowed Roles | 學生 |
| Source | `diagnosis-detail.hapdl.yaml` |

#### Detail Fields

| # | Field | Label | Display | Sample Value |
|:---|:---|:---|:---|:---|
| 1 | `hypothesis` | 診斷假設 | Plain text | `診斷假設-1` |
| 2 | `confidence` | 信心值 | Plain text | `信心值-1` |
| 3 | `mistakeCategory` | 錯誤分類 | Plain text | `錯誤分類-1` |
| 4 | `cognitiveOrigin` | 認知成因 | Plain text | `認知成因-1` |
| 5 | `severity` | 嚴重度 | Plain text | `嚴重度-1` |
| 6 | `isStylistic` | 是否為風格差異 | Plain text | `是否為風格差異-1` |
| 7 | `diagnosedAt` | 診斷時間 | Plain text | `2026-06-01 09:00` |

#### Detail Layout

- **Layout**: 2-column key-value grid (label left-aligned, value right)
- **Section dividers**: Group related fields with subtle horizontal rules
- **Related data**: Show related tables below (e.g., attachments list, audit history)


---

### Page 8: 本體演化提案

| Property | Value |
|:---|:---|
| Page ID | `ontology-proposal-list` |
| Type | **LIST** |
| Entity | `OntologyProposal` |
| Primary Actor |  |
| Allowed Roles | 治理者 |
| Source | `ontology-proposal-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `baseVersion` | 基準本體版本 | Text input | Free text |
| `status` | 提案狀態 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `proposalId` | 提案編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `baseVersion` | 基準本體版本 | text | - | `基準本體版本-1`, `基準本體版本-2`, `基準本體版本-3` |
| 3 | `status` | 提案狀態 | badge | - | `提案狀態-1`, `提案狀態-2`, `提案狀態-3` |
| 4 | `proposedAt` | 提出時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

#### Status Badge Color Mapping

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "proposalId": "ID-0001",
    "baseVersion": "基準本體版本-1",
    "status": "提案狀態-1",
    "proposedAt": "2026-06-01 09:00"
  },
  {
    "proposalId": "ID-0002",
    "baseVersion": "基準本體版本-2",
    "status": "提案狀態-2",
    "proposedAt": "2026-06-02 09:00"
  },
  {
    "proposalId": "ID-0003",
    "baseVersion": "基準本體版本-3",
    "status": "提案狀態-3",
    "proposedAt": "2026-06-03 09:00"
  }
]
```


---

### Page 9: 孩子認知進展

| Property | Value |
|:---|:---|
| Page ID | `parent-progress` |
| Type | **DASHBOARD** |
| Entity | `StudentSkillState` |
| Primary Actor |  |
| Allowed Roles | 家長 / 學校 |
| Source | `parent-progress.hapdl.yaml` |


---

### Page 10: 橋引管理練習

| Property | Value |
|:---|:---|
| Page ID | `play-session-play` |
| Type | **DETAIL** |
| Entity | `PlaySession` |
| Primary Actor |  |
| Allowed Roles | 學生 |
| Source | `play-session-play.hapdl.yaml` |

#### Detail Fields

| # | Field | Label | Display | Sample Value |
|:---|:---|:---|:---|:---|
| 1 | `dealId` | 牌例 | Plain text | `牌例-1` |
| 2 | `status` | 練習狀態 | Plain text | `練習狀態-1` |
| 3 | `startedAt` | 開始時間 | Plain text | `2026-06-01 09:00` |

#### Detail Layout

- **Layout**: 2-column key-value grid (label left-aligned, value right)
- **Section dividers**: Group related fields with subtle horizontal rules
- **Related data**: Show related tables below (e.g., attachments list, audit history)

#### Header Actions

- `request_hint`: **request_hint** (Button style: `primary`)
- `tag_reasoning`: **tag_reasoning** (Button style: `primary`)


---

### Page 11: 重播紀錄

| Property | Value |
|:---|:---|
| Page ID | `replay-run-list` |
| Type | **LIST** |
| Entity | `ReplayRun` |
| Primary Actor |  |
| Allowed Roles | 標注者 |
| Source | `replay-run-list.hapdl.yaml` |

#### Filter Bar

| Field | Label | Widget | Options |
|:---|:---|:---|:---|
| `scope` | 重播範圍 | Text input | Free text |
| `replayType` | 重播用途 | Text input | Free text |

#### Table Columns

| # | Field | Label | Display | Sortable | Sample Values |
|:---|:---|:---|:---|:---|:---|
| 1 | `replayId` | 重播編號 | link | - | `ID-0001`, `ID-0002`, `ID-0003` |
| 2 | `scope` | 重播範圍 | text | - | `重播範圍-1`, `重播範圍-2`, `重播範圍-3` |
| 3 | `replayType` | 重播用途 | badge | - | `重播用途-1`, `重播用途-2`, `重播用途-3` |
| 4 | `ontologyVersion` | 套用本體版本 | text | - | `套用本體版本-1`, `套用本體版本-2`, `套用本體版本-3` |
| 5 | `ruleSetVersion` | 套用規則集版本 | text | - | `套用規則集版本-1`, `套用規則集版本-2`, `套用規則集版本-3` |
| 6 | `ranAt` | 執行時間 | text | Yes | `2026-06-01 09:00`, `2026-06-02 09:00`, `2026-06-03 09:00` |

#### Status Badge Color Mapping

#### Actions

#### Pagination

- Style: `offset` (page numbers + prev/next)
- Default page size: 20
- Show: `1-20 / 128 筆` format

#### Sample Data (JSON)

```json
[
  {
    "replayId": "ID-0001",
    "scope": "重播範圍-1",
    "replayType": "重播用途-1",
    "ontologyVersion": "套用本體版本-1",
    "ruleSetVersion": "套用規則集版本-1",
    "ranAt": "2026-06-01 09:00"
  },
  {
    "replayId": "ID-0002",
    "scope": "重播範圍-2",
    "replayType": "重播用途-2",
    "ontologyVersion": "套用本體版本-2",
    "ruleSetVersion": "套用規則集版本-2",
    "ranAt": "2026-06-02 09:00"
  },
  {
    "replayId": "ID-0003",
    "scope": "重播範圍-3",
    "replayType": "重播用途-3",
    "ontologyVersion": "套用本體版本-3",
    "ruleSetVersion": "套用規則集版本-3",
    "ranAt": "2026-06-03 09:00"
  }
]
```


---

### Page 12: 局面標注

| Property | Value |
|:---|:---|
| Page ID | `situation-annotation-form` |
| Type | **FORM** |
| Entity | `SituationAnnotation` |
| Primary Actor |  |
| Allowed Roles | 標注者 |
| Source | `situation-annotation-form.hapdl.yaml` |

#### Form Fields

| # | Field | Label | Widget | Required | Sensitive | Options / Constraints | Sample Value |
|:---|:---|:---|:---|:---|:---|:---|:---|

#### Form Layout

- **Layout**: Label-left, 2-column for short fields (text, select, date), full-width for textarea
- **Grouping**: Group by DBML `group` attribute if available
- **Validation**: Show inline error messages below each field
- **Sensitive fields**: Show a lock icon and mask input by default, with a toggle to reveal

#### Footer Actions


#### Interaction Notes



---

### Page 13: 我的認知精熟度

| Property | Value |
|:---|:---|
| Page ID | `student-mastery-detail` |
| Type | **DETAIL** |
| Entity | `StudentSkillState` |
| Primary Actor |  |
| Allowed Roles | 學生 |
| Source | `student-mastery-detail.hapdl.yaml` |

#### Detail Fields

| # | Field | Label | Display | Sample Value |
|:---|:---|:---|:---|:---|
| 1 | `skillId` | 技能 | Plain text | `技能-1` |
| 2 | `recognitionMastery` | 辨識精熟度 | Plain text | `辨識精熟度-1` |
| 3 | `executionMastery` | 執行精熟度 | Plain text | `執行精熟度-1` |
| 4 | `transferMastery` | 遷移精熟度 | Plain text | `遷移精熟度-1` |
| 5 | `retentionMastery` | 保留精熟度 | Plain text | `保留精熟度-1` |
| 6 | `confidence` | 估計信心 | Plain text | `估計信心-1` |
| 7 | `trend` | 趨勢 | Plain text | `趨勢-1` |

#### Detail Layout

- **Layout**: 2-column key-value grid (label left-aligned, value right)
- **Section dividers**: Group related fields with subtle horizontal rules
- **Related data**: Show related tables below (e.g., attachments list, audit history)


---


## Generation Instructions

When generating UI from this brief:

1. **Use the Design System** above for all colors, typography, and spacing
2. **Render all text in Traditional Chinese (zh-TW)** as specified in each page
3. **Include the sidebar navigation** as shown in the Navigation Map
4. **Use the sample data** provided for each page to populate the preview
5. **Apply badge colors** as specified in the Status Badge Color Mapping
6. **Include responsive layout** that works on 1280px+ screens
7. **For forms**: show validation states, required field markers (*), and sensitive field masks
8. **For tables**: include sortable column headers, hover states, and row action buttons
9. **For detail pages**: use a clean key-value layout with grouped sections
10. Generate as **React + TypeScript** with **Ant Design** components, or as standalone **HTML + CSS**
