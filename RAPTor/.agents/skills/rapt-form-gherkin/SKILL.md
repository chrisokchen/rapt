---
name: rapt-form-gherkin
description: "RAPTor Gherkin Worker。僅由 rapt-behavior DELEGATE 呼叫，依 payload 渲染高階 Gherkin .feature 檔案。不推斷、不填補 payload 以外內容。"
metadata:
  user-invocable: false
  source: project-level
  skill-type: worker
---

# RAPTor Form Gherkin — Gherkin Renderer Worker

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::planner-worker-contract.md]
- LOAD REF [rapt-form-gherkin::references/gherkin-format-anchor.md]
- LOAD REF [rapt-form-gherkin::references/habdd-patterns.md]

## TRIGGER

- Planner 透過 DELEGATE 傳入 payload 呼叫 `rapt-form-gherkin`。
- payload 含 target path、source evidence、dsl version 與 write mode。

## SKIP

- payload 缺少 target path 或 source evidence。
- requested write path 超出 Artifact Output Contract。
- 需要推斷或補充 payload 以外內容才能完成的 DSL artifact。


## PRINCIPLE: CWD 為產出錨點
## PRINCIPLE: Artifact Output Contract（只寫 payload.target_path）
## PRINCIPLE: STRICT SOP

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| CREATE / UPDATE | `payload.target_path` | 由 caller 指定，唯一可寫路徑 |
| **DENY** | payload.target_path 以外任何路徑 | 嚴格限制 |
| **DENY** | ASK 使用者 | Worker 不問問題 |

---

## SOP

### 步驟 0：ASSERT payload 完整性

```
ASSERT: payload.target_path 存在
ASSERT: payload.content.feature_name 存在
ASSERT: payload.content.scenarios 存在且非空
ASSERT: payload.source_evidence 存在
ASSERT: payload.dsl_version == "3.3.0"
若 ASSERT 失敗 → EMIT 錯誤給 caller，停止
```

### 步驟 1：LOAD format rules

LOAD REF [rapt-form-gherkin::references/gherkin-format-anchor.md]

### 步驟 2：RENDER feature file

依 payload.content 按 Gherkin 格式渲染：

```gherkin
# source: {source_evidence[0].ref}
Feature: {feature_name}
  In order to {in_order_to}
  As a {as_a}
  I want to {i_want_to}

  {Background if present}

  {Scenarios...}
```

### 步驟 3：VALIDATE 輸出

對照 `rapt-behavior::rules/high-level-gherkin-rules.md` 反模式清單，確認輸出無違規。  
若有違規：EMIT 錯誤給 caller（不自行修正），停止。

### 步驟 4：WRITE `payload.target_path`

使用 `payload.write_mode`（預設 create）寫入。

### 步驟 5：EMIT 完成

```
✅ rapt-form-gherkin: 已寫入 {target_path}
```

## haBDD Lint Gate

ASSERT:
- haBDD 檔名使用 `*.ha.feature`，不得使用 legacy `*.feature`。
- haBDD 不得出現 selector、`data-testid`、HTTP method、URL、`/api/` 或 implementation literal。
- 渲染後執行 `rapt-verify/references/dsl-lint.py --file payload.target_path --levels 3`。
- lint 失敗時回傳 `failure_kind: dsl_lint_failed`，並且不得寫出任何 artifact。

## Worker Failure Contract

Worker 遇到下列任一情況時，不得產生任何檔案，必須立即回傳結構化的失敗結果。

```yaml
worker_result:
  status: failed
  failure_kind: invalid_payload | missing_evidence | contract_violation | dsl_lint_failed | unsupported_case
  target_path: <payload.target_path>
  message: <失敗原因>
  required_action: <Planner 需執行的後續修正動作>
```

