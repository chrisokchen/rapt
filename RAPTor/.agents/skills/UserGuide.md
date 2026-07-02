# RAPTor Skills 使用手冊

本手冊以目前最新版 `rapt-*` skills 為準，說明如何在一個專案中使用 RAPTor 完成需求探索、行為規格、資料與權限模型、API/UI intent、驗證、修復與 preview。

## 1. 開始前

請先確認目前工作目錄是你要產生 RAPTor artifacts 的專案根目錄。

建議初始結構：

```text
my-project/
├── raw-input/
│   ├── prd.md
│   └── stakeholder-notes.md
├── docs/
├── .raptor/
└── .clarify/
```

`raw-input/` 或 `docs/00-source/` 都可以放原始需求。RAPTor 不強制來源文件位置，但後續產物路徑一律由 `.raptor/arguments.yml` 控制。

## 2. Kickoff

第一次使用請執行：

```text
/rapt-kickoff
```

它會詢問：

1. `project.name`
2. `project.description`
3. `project.language`，預設 `zh-hant`
4. `project.mode`，預設 `greenfield`
5. `paths.docs_dir`，預設 `docs/`

輸出：

```text
.raptor/
├── KICKOFF_PLAN.md
├── arguments.yml
└── session.md
```

新版 arguments schema 為 v2：

```yaml
arguments_schema_version: 2

paths:
  discovery_dir: docs/discovery/
  reports_dir: docs/reports/
  data_model_dir: docs/ssot/dbml/
  high_gherkin_dir: docs/ssot/habdd/
  access_control_dir: docs/ssot/haarm/
  backend_intent_dir: docs/ssot/haapi/
  frontend_intent_dir: docs/ssot/hapdl/
  traceability_file: .raptor/traceability.md
  impact_matrix_file: .raptor/impact-matrix.yml

generated:
  status: deferred
  openapi_dir: docs/generate/openapi/
  lofi_dir: docs/generate/lofi/
  designbrief_dir: docs/generate/designbrief/
```

`rapt-kickoff` 不會一次建立所有 phase 產物；它先建立路徑與 session SSoT。

## 3. Phase 1：Discovery

執行：

```text
/rapt-discovery
```

輸入：

- `raw-input/*`
- `docs/00-source/*`
- 其他你指定的需求文件

輸出：

```text
docs/discovery/
├── 01-stakeholders.md
├── 02-story-index.md
├── 03-ubiquitous-language.md
└── 04-vision-kpi.md
```

目標是整理 stakeholder、user story、domain language、event/journey、vision/KPI/scope。

## 4. Phase 1.5：Behavior / haBDD

當 `docs/discovery/02-story-index.md` 成形後執行：

```text
/rapt-behavior
```

輸出：

```text
docs/ssot/habdd/
└── *.ha.feature
```

haBDD 是高階業務行為 SSoT。它描述 business behavior，不描述 UI selector、API endpoint、HTTP method、JSON response、database setup。

建議格式：

```gherkin
# source: docs/discovery/02-story-index.md#US-001
# feature-id: F-001
Feature: 案件覆核
  Scenario: 主管核准待覆核案件
    Given 待覆核案件已由承辦人送出
    When 審核主管核准案件
    Then 案件狀態應變更為已核准
```

## 5. Phase 2：Modeling

執行：

```text
/rapt-modeling
```

輸入：

- `docs/discovery/*.md`
- `docs/ssot/habdd/*.ha.feature`

輸出：

```text
docs/ssot/dbml/
└── *.dbml

docs/ssot/haarm/
└── *.haarm.yaml
```

DBML 是 entity/field 的唯一 SSoT。haARM 是 role/permission/resource/policy 的唯一 SSoT。

## 6. Phase 3：Clarify

當 Discovery、haBDD、DBML、haARM 中存在缺口、矛盾或需業務決策時執行：

```text
/rapt-clarify
```

輸出：

```text
.clarify/
├── backlog.md
└── <batch>.md
```

新版 clarify payload 應包含來源 skill、artifact、location、問題、why、options、impact。涉及下游同步時，應更新 `.raptor/impact-matrix.yml`。

只有已確認的 decision 才能套用回 SSoT。

## 7. Phase 4：Intent

當 DBML、haARM、haBDD 已相對穩定後執行：

```text
/rapt-intent
```

輸出：

```text
docs/ssot/haapi/
└── *.haapi.yaml

docs/ssot/hapdl/
└── *.hapdl.yaml
```

注意：

- haAPI / haPDL 不自行發明 role/permission，必須引用 haARM。
- haAPI / haPDL 不自行發明 entity/field，必須引用 DBML。
- `access.permissions` 與 `security.permissions` 這類 legacy 欄位不可再使用，應改用 v3.3 規則。

## 8. Phase 5：Verify

當五類 SSoT 都已產出後執行：

```text
/rapt-verify
```

輸出：

```text
docs/reports/
├── verify-report.md
└── verify-report.yml
```

`verify-report.yml` 是 machine-readable report。每筆 finding 都會分流：

| Route | 意義 |
|---|---|
| `NEED_TO_FIX` | evidence 足夠，可由 reconcile 或 owner skill 修復 |
| `NEED_TO_CLARIFY` | 需要使用者或 domain owner 決策 |
| `NOTE_ONLY` | 不阻擋流程，但保留紀錄 |

`rapt-verify` 只報告，不修改 SSoT。

## 9. Reconcile

如果 verify 結果是 `PARTIAL` 或 `FAIL`，執行：

```text
/rapt-reconcile
```

它會優先讀取：

```text
docs/reports/verify-report.yml
```

輸出或更新：

```text
.raptor/reconcile/sessions/*.yml
.raptor/reconcile/archive/**
.raptor/impact-matrix.yml
.raptor/session.md
```

規則：

- 修改任何 SSoT 前必須建立 archive snapshot。
- 可修項走 `NEED_TO_FIX`。
- 需決策項轉成 clarify payload。
- 修復後應再執行 `/rapt-verify`。

## 10. RAscore

執行：

```text
/rapt-RAscore
```

輸出：

```text
docs/reports/
├── rascore-precheck.json
├── rascore-scorecard.draft.json
├── rascore-scorecard.yml
├── rascore-report.md
├── rascore-findings.md
└── rascore-findings.json
```

RAscore 是 advisory-only，不阻擋 phase gate。findings 會透過 `rascore-action-map.md` 對應到：

- `NEED_TO_FIX`
- `NEED_TO_CLARIFY`
- `NOTE_ONLY`

## 11. Human Sync（人工修改 SSoT 後）

當你（或團隊成員）**不經 skill、直接手動修改** `docs/ssot/**` 之後，在下一次 verify 前執行：

```text
/rapt-human-sync
```

它會：

1. 解析 git baseline（可用 `--baseline <commit>` 明確指定）。
2. 掃描 SSoT 的人工變更，記錄 who/when/why 與 hunk 摘要。
3. 產生 HSYNC 變更紀錄，並把 `manual_change` entries 登錄進 impact matrix。

輸出：

```text
.raptor/human-sync/
└── HSYNC-YYYYMMDD-NNN.yml

.raptor/impact-matrix.yml   （manual_change entries，status=open）
.raptor/traceability.md     （追加 Decision Traceability 摘要）
```

規則：

- 只登錄、不修復；修復仍走 `/rapt-verify` → `/rapt-reconcile`。
- SSoT 沒有任何變更時，不建立空 HSYNC。
- 重跑具冪等性（以 fingerprint 去重），不會產生重複 entries。
- 無法解析 baseline 時會停止，請以 `--baseline <commit>` 指定。

建議下一步：執行 `/rapt-verify`。

## 12. Impact（變更事前影響分析）

在 brownfield 專案要加新功能、改需求，或 clarify 選項可能改變 scope 時，**先**執行：

```text
/rapt-impact
```

輸入（三擇一）：

- `whatif/` 目錄下的提案文件
- 你本次行內的自然語言描述
- 指定某個既有 SSoT 檔案，分析其改動的傳播

輸出：

```text
docs/reports/impact/
├── IA-YYYYMMDD-NNN.md      （人類可讀報告）
├── IA-YYYYMMDD-NNN.yml     （機器可讀報告）
└── impact-graph-YYYYMMDD.json
```

規則：

- **Advisory-only**：只給 accept / defer / reject / needs_clarification 建議，不修改任何 SSoT、不寫 `.raptor/impact-matrix.yml`（僅輸出 `proposed_impact_entries`）。
- 每個影響項目都附 evidence 與 confidence；traceability L2/L3 不完整時會降級分析並明示 limitations。
- greenfield 且尚無 DBML / haBDD 時不適用，請先跑 `/rapt-discovery`。

## 13. Preview Tools

Preview tools 只能寫 `docs/generate/**`，不可修改 `docs/ssot/**`。每個 preview 都會同步輸出 audit YAML。

### OpenAPI

```text
/rapt-openapi
```

輸入：

- `docs/ssot/haapi/*.haapi.yaml`
- `docs/ssot/dbml/*.dbml`
- `docs/ssot/haarm/*.haarm.yaml`

輸出：

```text
docs/generate/openapi/
├── openapi.yaml
└── openapi-audit.yml
```

### Lo-Fi

```text
/rapt-lofi
```

輸入：

- `docs/ssot/hapdl/*.hapdl.yaml`
- `docs/ssot/dbml/*.dbml`
- `docs/ssot/haarm/*.haarm.yaml`

輸出：

```text
docs/generate/lofi/
├── index.html
└── scope-audit.yml
```

本機預覽：

```powershell
python -m http.server 8089 --directory docs/generate/lofi
```

### Design Brief

```text
/rapt-design-brief
```

輸入：

- `docs/ssot/hapdl/*.hapdl.yaml`
- `docs/ssot/dbml/*.dbml`
- `docs/ssot/haarm/*.haarm.yaml`

輸出：

```text
docs/generate/designbrief/
├── design-brief.md
└── style-profile.yml
```

## 14. 常用工具

### 解析 arguments.yml

```powershell
python RAPTor/.agents/skills/rapt-core/scripts/resolve_args.py --key paths.data_model_dir
```

### 檢查 skill family

```powershell
python RAPTor/.agents/skills/rapt-core/scripts/analyze_skill_family.py
```

### haBDD lint

```powershell
python RAPTor/.agents/skills/rapt-verify/references/dsl-lint.py --habdd docs/ssot/habdd --levels 3
```

### Impact matrix

```powershell
python RAPTor/.agents/skills/rapt-core/scripts/manage_impact_matrix.py validate
python RAPTor/.agents/skills/rapt-core/scripts/manage_impact_matrix.py query --artifact docs/ssot/haapi
```

### v1 layout 遷移 dry-run

```powershell
python RAPTor/.agents/skills/rapt-core/scripts/migrate_docs_layout.py --root .
```

### 人工 SSoT 變更偵測（唯讀，不寫任何檔案）

```powershell
python RAPTor/.agents/skills/rapt-human-sync/scripts/detect_unsynced.py --root .
```

### 影響圖譜萃取（rapt-impact 使用）

```powershell
python RAPTor/.agents/skills/rapt-impact/scripts/extract_impact_graph.py --ssot-dir docs/ssot --trace .raptor/traceability.md --format json
```

## 15. 一頁流程表

| 階段 | 指令 | 主要輸入 | 主要輸出 |
|---|---|---|---|
| Kickoff | `/rapt-kickoff` | 使用者回答 | `.raptor/KICKOFF_PLAN.md`、`.raptor/arguments.yml`、`.raptor/session.md` |
| Discovery | `/rapt-discovery` | `raw-input/*`、`docs/00-source/*` | `docs/discovery/*.md` |
| Behavior | `/rapt-behavior` | `docs/discovery/02-story-index.md` | `docs/ssot/habdd/*.ha.feature` |
| Modeling | `/rapt-modeling` | Discovery + haBDD | `docs/ssot/dbml/*.dbml`、`docs/ssot/haarm/*.haarm.yaml` |
| Clarify | `/rapt-clarify` | 缺口與矛盾 | `.clarify/*`、已確認決策回寫 SSoT |
| Intent | `/rapt-intent` | DBML + haARM + haBDD | `docs/ssot/haapi/*.haapi.yaml`、`docs/ssot/hapdl/*.hapdl.yaml` |
| Verify | `/rapt-verify` | 所有 SSoT | `docs/reports/verify-report.md`、`docs/reports/verify-report.yml` |
| Reconcile | `/rapt-reconcile` | `verify-report.yml` | session、archive、impact matrix、修復後 SSoT |
| RAscore | `/rapt-RAscore` | Discovery + SSoT + verify | `docs/reports/rascore-*` |
| Human Sync | `/rapt-human-sync` | 人工修改後的 `docs/ssot/**`（git diff） | `.raptor/human-sync/HSYNC-*.yml`、`.raptor/impact-matrix.yml`（manual_change） |
| Impact | `/rapt-impact` | what-if 提案 / 行內需求 / 指定 SSoT | `docs/reports/impact/IA-*.md`、`IA-*.yml` |
| OpenAPI | `/rapt-openapi` | haAPI + DBML + haARM | `docs/generate/openapi/*` |
| Lo-Fi | `/rapt-lofi` | haPDL + DBML + haARM | `docs/generate/lofi/*` |
| Design Brief | `/rapt-design-brief` | haPDL + DBML + haARM | `docs/generate/designbrief/*` |

## 16. FAQ

### Kickoff 後沒有 `docs/discovery/`，是不是失敗？

不是。Kickoff 只建立 `.raptor/**` 設定與 session。各 phase 目錄會在對應 skill 寫入 artifact 時建立。

### 可以使用舊版 `docs/01-discovery` 嗎？

既有專案可由 legacy fallback 讀取，但新專案預設使用 v2 layout。建議用 `migrate_docs_layout.py` 先產生 dry-run 遷移計畫。

### Worker 可以直接呼叫嗎？

不建議。`rapt-form-*` 是 worker，應由 planner DELEGATE payload。缺 payload 或 source evidence 時，worker 必須回傳 failure contract。

### Preview output 可以拿來改 SSoT 嗎？

不可以。Preview 是 generated artifact。若 preview audit 發現 SSoT 問題，應交給 verify/reconcile/clarify，而不是反向修改 SSoT。
