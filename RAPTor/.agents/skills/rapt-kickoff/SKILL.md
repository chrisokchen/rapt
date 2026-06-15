---
name: rapt-kickoff
description: "RAPTor 專案初始化。建立 `.raptor/KICKOFF_PLAN.md`、`.raptor/arguments.yml`（路徑設定 SSoT）與 `.raptor/session.md`。Use when: 開始新專案需求分析、第一次在某個 repo 執行 RAPTor 流程、/rapt-kickoff、需要建立或重設路徑設定。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: planner
---

# RAPTor Kickoff

必讀：

- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::verb-cheatsheet.md]
- LOAD REF [rapt-kickoff::arguments-schema.md]

## TRIGGER

- 使用者第一次在專案執行 RAPTor。
- 使用者要求 `/rapt-kickoff`。
- `.raptor/arguments.yml` 不存在，且後續 rapt-* skill 需要路徑設定。
- 使用者明確要求重新初始化 RAPTor 路徑與 session。

## SKIP

- `.raptor/arguments.yml` 已存在，且使用者沒有要求重設。
- 使用者只想執行 discovery/modeling/verify 等既有 phase。
- 目前 CWD 不是目標專案根目錄，且使用者尚未確認。

## PRINCIPLE

- CWD 是專案根目錄；所有相對路徑以 CWD 為基準。
- File First：先建立 `.raptor/KICKOFF_PLAN.md`，再建立 `.raptor/arguments.yml`。
- deny-by-default：只寫 Artifact Output Contract 允許的 `.raptor/**`。
- 新專案一律使用 `arguments_schema_version: 2`。

## Artifact Output Contract

| Action | Path | Purpose |
|---|---|---|
| READ | `.raptor/arguments.yml` | 判斷是否已初始化 |
| CREATE / UPDATE | `.raptor/KICKOFF_PLAN.md` | 初始化計畫與路徑預覽 |
| CREATE | `.raptor/arguments.yml` | 路徑設定 SSoT |
| CREATE / UPDATE | `.raptor/session.md` | RAPTor phase 狀態 |
| DENY | `docs/ssot/**` | kickoff 不建立或修改 SSoT artifact |
| DENY | `docs/generate/**` | kickoff 不建立 generated artifact |

## Inputs

ASK 使用者確認：

1. `project.name`
2. `project.description`
3. `project.language`，預設 `zh-hant`
4. `project.mode`，預設 `greenfield`
5. `paths.docs_dir`，預設 `docs/`

## Workflow

### Step 0: Bind CWD

READ:
- CWD
- `.raptor/arguments.yml`

ASSERT:
- CWD 是使用者要初始化的專案根目錄。
- 若 `.raptor/arguments.yml` 已存在，先 EMIT 已初始化狀態並停止，除非使用者明確要求重設。

### Step 1: Derive v2 Paths

DERIVE:

```text
paths.discovery_dir        = {docs_dir}discovery/
paths.reports_dir          = {docs_dir}reports/
paths.ssot_dir             = {docs_dir}ssot/
paths.data_model_dir       = {docs_dir}ssot/dbml/
paths.high_gherkin_dir     = {docs_dir}ssot/habdd/
paths.access_control_dir   = {docs_dir}ssot/haarm/
paths.backend_intent_dir   = {docs_dir}ssot/haapi/
paths.frontend_intent_dir  = {docs_dir}ssot/hapdl/
paths.clarify_dir          = .clarify/
paths.traceability_file    = .raptor/traceability.md
paths.impact_matrix_file   = .raptor/impact-matrix.yml
generated.generated_dir    = {docs_dir}generate/
generated.pdl_dir          = {docs_dir}generate/pdl/
generated.low_gherkin_dir  = {docs_dir}generate/isabdd/
generated.openapi_dir      = {docs_dir}generate/openapi/
generated.lofi_dir         = {docs_dir}generate/lofi/
generated.designbrief_dir  = {docs_dir}generate/designbrief/
```

### Step 2: Create KICKOFF_PLAN

CREATE / UPDATE `.raptor/KICKOFF_PLAN.md`，內容包含：

- 使用者提供的 project 設定。
- 即將寫入的 arguments.yml YAML preview。
- v2 docs layout 預覽。
- `generated.status: deferred` 的意義。
- 下一步建議：`/rapt-discovery`。

### Step 3: Create arguments.yml

CREATE `.raptor/arguments.yml`，格式必須符合 `rapt-kickoff::arguments-schema.md`。

ASSERT:
- `arguments_schema_version: 2`
- `policy.write_mode: deny-by-default`
- `generated.status: deferred`

### Step 4: Create session.md

CREATE / UPDATE `.raptor/session.md`：

```markdown
# RAPTor Session

> arguments.yml: initialized
> arguments_schema_version: 2
> initialized_at: {date}

## Phase Status

| Phase | Status | Next |
|---|---|---|
| 1. Discovery | pending | /rapt-discovery |
| 1.5 Behavior | pending | /rapt-behavior |
| 2. Modeling | pending | /rapt-modeling |
| 3. Clarification | pending | /rapt-clarify |
| 4. Intent | pending | /rapt-intent |
| 5. Verification | pending | /rapt-verify |
| 6. Reconcile | pending | /rapt-reconcile |
| Preview | deferred | /rapt-openapi, /rapt-lofi, /rapt-design-brief |
```

## Exit Report

EMIT:

```text
RAPTor Kickoff 完成。

已建立：
- .raptor/KICKOFF_PLAN.md
- .raptor/arguments.yml
- .raptor/session.md

下一步：執行 /rapt-discovery 匯入原始需求材料。
```
