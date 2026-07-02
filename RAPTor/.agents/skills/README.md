# RAPTor Skills README

本目錄收錄 RAPTor 的 `rapt-*` skill family。最新版以 `.raptor/arguments.yml` v2 作為路徑 SSoT，主要產物分為：

- SSoT：`docs/ssot/**`
- Generated / Preview：`docs/generate/**`
- Discovery：`docs/discovery/**`
- Reports：`docs/reports/**`
- Session / trace / impact：`.raptor/**`

## Skill 總覽

| 類型 | Skill | 用途 |
|---|---|---|
| Utility | `rapt-core` | 共用 reference、schema、script、template hub |
| Planner | `rapt-kickoff` | 初始化 `.raptor/KICKOFF_PLAN.md`、`.raptor/arguments.yml`、`.raptor/session.md` |
| Planner | `rapt-discovery` | Phase 1，整理來源需求、stakeholder、journey、event、vision/KPI/scope |
| Planner | `rapt-behavior` | Phase 1.5，產生高階 haBDD / Gherkin 行為規格 |
| Planner | `rapt-modeling` | Phase 2，產生 DBML 與 haARM |
| Planner | `rapt-clarify` | Phase 3，整理不確定性、產生問題包、套用已確認決策 |
| Planner | `rapt-intent` | Phase 4，產生 haAPI 與 haPDL intent |
| Verifier | `rapt-verify` | Phase 5，輸出 verify report 與 machine-readable findings |
| Planner | `rapt-reconcile` | 根據 findings 修復可修項、建立 session/archive、轉交需澄清項 |
| Worker | `rapt-form-dbml` | DBML DSL renderer |
| Worker | `rapt-form-gherkin` | haBDD / Gherkin renderer，含 haBDD lint gate |
| Worker | `rapt-form-haarm` | haARM DSL renderer |
| Worker | `rapt-form-haapi` | haAPI DSL renderer |
| Worker | `rapt-form-hapdl` | haPDL DSL renderer |
| Utility | `rapt-clarify-loop` | 問題批次與使用者澄清互動 |
| Utility | `rapt-RAscore` | advisory-only 品質評分、scorecard、findings、action map |
| Utility | `rapt-human-sync` | 偵測人工直接修改的 SSoT，產生 HSYNC 變更紀錄並登錄 `manual_change` 到 impact matrix |
| Utility | `rapt-impact` | 變更事前影響分析（advisory-only），唯讀遍歷 SSoT 與 traceability，產出受影響 artifact、風險與建議 |
| Preview | `rapt-openapi` | 從 haAPI/DBML/haARM 產生 OpenAPI preview |
| Preview | `rapt-lofi` | 從 haPDL/DBML/haARM 產生 Lo-Fi HTML preview |
| Preview | `rapt-design-brief` | 從 haPDL/DBML/haARM 產生 Design Brief |

## 核心原則

- CWD 是目標專案根目錄；相對路徑都以 CWD 解析。
- 所有路徑來自 `.raptor/arguments.yml`，不得複製另一份設定。
- 每個 skill 都有 `TRIGGER`、`SKIP`、`Artifact Output Contract`。
- Worker 只接受 Planner payload，不自行 ASK、不擴張寫入範圍。
- Worker 失敗必須回傳 `failure_kind`，例如 `invalid_payload`、`missing_evidence`、`contract_violation`、`dsl_lint_failed`、`unsupported_case`。
- Preview skill 只寫 `docs/generate/**`，不改 `docs/ssot/**`。
- Verify 只報告，不修復；修復交給 `rapt-reconcile` 或 owner skill。

## arguments.yml v2

新專案由 `rapt-kickoff` 建立：

```yaml
arguments_schema_version: 2

project:
  name: <string>
  description: <string>
  language: zh-hant
  mode: greenfield

paths:
  docs_dir: docs/
  discovery_dir: docs/discovery/
  reports_dir: docs/reports/
  clarify_dir: .clarify/
  traceability_file: .raptor/traceability.md
  impact_matrix_file: .raptor/impact-matrix.yml

  ssot_dir: docs/ssot/
  data_model_dir: docs/ssot/dbml/
  high_gherkin_dir: docs/ssot/habdd/
  access_control_dir: docs/ssot/haarm/
  backend_intent_dir: docs/ssot/haapi/
  frontend_intent_dir: docs/ssot/hapdl/

generated:
  status: deferred
  generated_dir: docs/generate/
  pdl_dir: docs/generate/pdl/
  low_gherkin_dir: docs/generate/isabdd/
  openapi_dir: docs/generate/openapi/
  lofi_dir: docs/generate/lofi/
  designbrief_dir: docs/generate/designbrief/
```

既有 v1 專案可參考 `rapt-core/scripts/migrate_docs_layout.py` 產生 dry-run 遷移計畫。

## 目錄結構

```text
my-project/
├── .raptor/
│   ├── KICKOFF_PLAN.md
│   ├── arguments.yml
│   ├── session.md
│   ├── traceability.md
│   ├── impact-matrix.yml
│   └── reconcile/
│       ├── sessions/
│       └── archive/
├── .clarify/
└── docs/
    ├── discovery/
    ├── reports/
    ├── ssot/
    │   ├── dbml/
    │   ├── habdd/
    │   ├── haarm/
    │   ├── haapi/
    │   └── hapdl/
    └── generate/
        ├── pdl/
        ├── isabdd/
        ├── openapi/
        ├── lofi/
        └── designbrief/
```

## SSoT 與 Generated 邊界

| 層級 | Artifact | 路徑 |
|---|---|---|
| First-class SSoT | Annotated DBML | `docs/ssot/dbml/*.dbml` |
| First-class SSoT | haBDD | `docs/ssot/habdd/*.ha.feature` |
| First-class SSoT | haARM | `docs/ssot/haarm/*.haarm.yaml` |
| First-class SSoT | haAPI | `docs/ssot/haapi/*.haapi.yaml` |
| First-class SSoT | haPDL | `docs/ssot/hapdl/*.hapdl.yaml` |
| Supporting SSoT | Discovery | `docs/discovery/*.md` |
| Supporting SSoT | Reports | `docs/reports/*` |
| Supporting SSoT | Traceability | `.raptor/traceability.md` |
| Supporting SSoT | Impact Matrix | `.raptor/impact-matrix.yml` |
| Generated | OpenAPI | `docs/generate/openapi/openapi.yaml` |
| Generated | Lo-Fi | `docs/generate/lofi/index.html` |
| Generated | Design Brief | `docs/generate/designbrief/design-brief.md` |
| Generated | PDL | `docs/generate/pdl/` |
| Generated | isaBDD | `docs/generate/isabdd/` |

## 標準流程

```text
1. /rapt-kickoff
   → .raptor/KICKOFF_PLAN.md
   → .raptor/arguments.yml
   → .raptor/session.md

2. /rapt-discovery
   → docs/discovery/*.md

3. /rapt-behavior
   → docs/ssot/habdd/*.ha.feature

4. /rapt-modeling
   → docs/ssot/dbml/*.dbml
   → docs/ssot/haarm/*.haarm.yaml

5. /rapt-clarify
   → .clarify/*
   → 已確認決策可套用回 SSoT

6. /rapt-intent
   → docs/ssot/haapi/*.haapi.yaml
   → docs/ssot/hapdl/*.hapdl.yaml

7. /rapt-verify
   → docs/reports/verify-report.md
   → docs/reports/verify-report.yml

8. 若 PARTIAL / FAIL：
   /rapt-reconcile
   → .raptor/reconcile/sessions/*.yml
   → .raptor/reconcile/archive/**
   → .raptor/impact-matrix.yml
   → 修復後再跑 /rapt-verify

9. 人工直接修改 docs/ssot/** 後：
   /rapt-human-sync
   → .raptor/human-sync/HSYNC-*.yml
   → .raptor/impact-matrix.yml（manual_change entries）
   → 接續執行 /rapt-verify

10. 新功能 / 需求變更的事前評估（可選，advisory-only）：
   /rapt-impact
   → docs/reports/impact/IA-YYYYMMDD-NNN.md
   → docs/reports/impact/IA-YYYYMMDD-NNN.yml

11. Preview：
   /rapt-openapi
   → docs/generate/openapi/openapi.yaml
   → docs/generate/openapi/openapi-audit.yml

   /rapt-lofi
   → docs/generate/lofi/index.html
   → docs/generate/lofi/scope-audit.yml

   /rapt-design-brief
   → docs/generate/designbrief/design-brief.md
   → docs/generate/designbrief/style-profile.yml
```

## haBDD 規則

haBDD 是 business behavior SSoT，建議使用 `*.ha.feature`。

必要 header：

```gherkin
# source: docs/discovery/02-story-index.md#US-001
# feature-id: F-001
Feature: 案件覆核
```

禁止在 haBDD 放入：

- CSS selector，例如 `#submit`、`.button-primary`
- `data-testid`
- URL 或 API path，例如 `/api/cases`
- HTTP method，例如 `GET`、`POST`
- response status / JSON body / database setup

`rapt-verify/references/dsl-lint.py` 已支援 `--habdd` 與單檔 `.ha.feature` lint。

## Verify / Reconcile

`rapt-verify` 同時輸出：

- `docs/reports/verify-report.md`
- `docs/reports/verify-report.yml`

每筆 finding 必須包含：

- `route`: `NEED_TO_FIX`、`NEED_TO_CLARIFY`、`NOTE_ONLY`
- `can_fix`
- `owner_skill`
- `artifact`
- `location`
- `evidence`
- `suggested_action`

`rapt-reconcile` 優先讀取 `verify-report.yml`，修改任何 SSoT 前必須建立 archive snapshot，並輸出 `.raptor/reconcile/sessions/*.yml`。

## Human Sync / Impact

`rapt-human-sync` 處理「人工直接修改 SSoT」的治理缺口：

- 以 git baseline 掃描 `docs/ssot/**` 的人工變更，產生 `.raptor/human-sync/HSYNC-*.yml`（含 who/when/why、hunk 摘要、risk）。
- 透過 `manage_impact_matrix.py upsert` 登錄 `source_type: manual_change` entries；以 fingerprint 保證重跑冪等。
- 只登錄、不修復；完成後建議接續 `/rapt-verify`。

`rapt-impact` 是變更「事前」的影響分析（advisory-only）：

- 輸入 what-if 提案（`whatif/` 或行內描述），唯讀遍歷 DBML、haBDD、haARM、haAPI、haPDL 與 traceability。
- 產出成對的 `IA-*.md` / `IA-*.yml` 報告與 impact graph，給出 accept / defer / reject / needs_clarification 建議。
- 不修改任何 SSoT 或 `.raptor/impact-matrix.yml`；只輸出 `proposed_impact_entries` 供後續決策。

## Core Scripts

| Script | 用途 |
|---|---|
| `rapt-core/scripts/resolve_args.py` | 解析 `.raptor/arguments.yml`，輸出 `KEY=value` |
| `rapt-core/scripts/manage_impact_matrix.py` | validate/query/upsert `.raptor/impact-matrix.yml` |
| `rapt-core/scripts/migrate_docs_layout.py` | v1 到 v2 docs layout dry-run / apply |
| `rapt-core/scripts/analyze_skill_family.py` | 檢查 skill family 一致性 |

## Preview Audit

Preview tool 只產生 generated artifact，同時輸出 audit YAML：

| Skill | Output | Audit |
|---|---|---|
| `rapt-openapi` | `docs/generate/openapi/openapi.yaml` | `docs/generate/openapi/openapi-audit.yml` |
| `rapt-lofi` | `docs/generate/lofi/index.html` | `docs/generate/lofi/scope-audit.yml` |
| `rapt-design-brief` | `docs/generate/designbrief/design-brief.md` | `docs/generate/designbrief/style-profile.yml` |

Audit finding 也必須具備 `route` 與 `can_fix`，但 preview skill 不直接修改 SSoT。
