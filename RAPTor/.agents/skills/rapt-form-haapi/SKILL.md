---
name: rapt-form-haapi
description: "RAPTor haAPI 格式生成器（Worker）。僅由 rapt-intent DELEGATE 呼叫，負責依 haAPI v3.3 DSL 規格將 payload 渲染成 haAPI YAML 檔案。不推斷、不補充、不詢問使用者。"
metadata:
  user-invocable: false
  source: project-level
  skill-type: worker
---

# RAPTor Form haAPI — haAPI 格式生成器（Worker）

先遵守 rapt-core：
- LOAD REF [rapt-core::planner-worker-contract.md]
- LOAD REF [rapt-core::dsl-cross-reference-v33.md]
- LOAD REF [rapt-form-haapi::references/haapi-format-anchor.md]

## TRIGGER

- Planner 透過 DELEGATE 傳入 payload 呼叫 `rapt-form-haapi`。
- payload 含 target path、source evidence、dsl version 與 write mode。

## SKIP

- payload 缺少 target path 或 source evidence。
- requested write path 超出 Artifact Output Contract。
- 需要推斷或補充 payload 以外內容才能完成的 DSL artifact。


## PRINCIPLE: Artifact Output Contract（只寫 payload.output_file）
## PRINCIPLE: Worker 禁止推斷、禁止 ASK、禁止補充 payload 外的內容
## PRINCIPLE: STRICT SOP

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| CREATE / UPDATE | `payload.output_file` | haAPI YAML 檔案 |
| **DENY** | 任何其他路徑 | |
| **DENY** | 推斷 payload 以外的 entity/resource | |
| **DENY** | 加入 payload 未指定的欄位 | |
| **DENY** | `access.permissions:` | deprecated，絕對禁止 |

---

## SOP

### 步驟 0：ASSERT payload

```
ASSERT: payload.schema_version == "3.3"
ASSERT: payload.api_intent 非空
ASSERT: payload.source_evidence 非空
ASSERT: payload.output_file 路徑存在（目錄已建立）
若 ASSERT 失敗 → EMIT 錯誤訊息，停止
```

### 步驟 1：LOAD format anchor

LOAD REF [rapt-form-haapi::references/haapi-format-anchor.md]

### 步驟 2：RENDER haAPI YAML

依 haapi-format-anchor.md 的結構，將 payload 對映生成：

1. `api:` → 來自 payload.api_intent.api_id
2. `schema_version: "3.3"` → 固定值
3. `entity:` → 來自 payload.api_intent.entity（不修改大小寫）
4. `title:` → 來自 payload.api_intent.title
5. `access.endpoints` → 依 standard + operations 生成
6. `access.operations` → 每個 operation 附 required_roles / required_permissions
7. `list:` → 依 payload.api_intent.list 生成
8. `cic_notes:` → 僅包含 payload 傳入的 CiC notes

**嚴格禁止**：`access.permissions:`（不論任何情況）

### 步驟 3：WRITE 到 payload.output_file

WRITE 生成的 YAML 到 payload.output_file。

### 步驟 3.5：RUN dsl-lint（生成當下驗證，shift-left）⭐

```
RUN: python {rapt-verify::references/dsl-lint.py} --file {payload.output_file} --levels 1,2,3
若出現任何 ERROR（HAAPI-SCHEMA-* / HAAPI-LINT-* / DSL-PARSE-*）：
  → 依 lint 的 fix 指引修正 YAML，重新 WRITE，再次 RUN
  → 直到 0 ERROR 才進入步驟 4（禁止帶著漂移輸出）
```

重點：`access.endpoints` / `access.operations` 必為 **dict（key=操作名）**；path/method 只在 `exposes`；禁止頂層 `endpoints:`、禁止 `access.permissions:`。

### 步驟 4：EMIT 完成確認

```
✅ haAPI 已生成並通過 dsl-lint：{output_file}
entity: {entity}，operations: {N} 個
```
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

