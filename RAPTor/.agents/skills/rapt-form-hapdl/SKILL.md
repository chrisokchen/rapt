---
name: rapt-form-hapdl
description: "RAPTor haPDL 格式生成器（Worker）。僅由 rapt-intent DELEGATE 呼叫，負責依 haPDL v3.3 DSL 規格將 payload 渲染成 haPDL YAML 檔案。不推斷、不補充、不詢問使用者。"
metadata:
  user-invocable: false
  source: project-level
  skill-type: worker
---

# RAPTor Form haPDL — haPDL 格式生成器（Worker）

先遵守 rapt-core：
- LOAD REF [rapt-core::planner-worker-contract.md]
- LOAD REF [rapt-core::dsl-cross-reference-v33.md]
- LOAD REF [rapt-form-hapdl::references/hapdl-format-anchor.md]

## TRIGGER

- Planner DELEGATE ?? payload ? `rapt-form-hapdl`?
- payload ?? target path?source evidence?dsl version ? write mode?

## SKIP

- payload ?? target path ? source evidence?
- requested write path ?? Artifact Output Contract?
- ??????????????????? DSL artifact?


## PRINCIPLE: Artifact Output Contract（只寫 payload.output_file）
## PRINCIPLE: Worker 禁止推斷、禁止 ASK、禁止補充 payload 外的內容
## PRINCIPLE: STRICT SOP

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| CREATE / UPDATE | `payload.output_file` | haPDL YAML 檔案 |
| **DENY** | 任何其他路徑 | |
| **DENY** | 推斷 payload 以外的 page/entity | |
| **DENY** | 加入 payload 未指定的欄位 | |
| **DENY** | `security.permissions:` | deprecated，絕對禁止 |

---

## SOP

### 步驟 0：ASSERT payload

```
ASSERT: payload.schema_version == "3.3"
ASSERT: payload.page_intent 非空
ASSERT: payload.page_intent.api != null
ASSERT: payload.source_evidence 非空
ASSERT: payload.output_file 路徑存在（目錄已建立）
若 ASSERT 失敗 → EMIT 錯誤訊息，停止
```

### 步驟 1：LOAD format anchor

LOAD REF [rapt-form-hapdl::references/hapdl-format-anchor.md]

### 步驟 2：RENDER haPDL YAML

依 hapdl-format-anchor.md 的結構，將 payload 對映生成：

1. `page:` → 來自 payload.page_intent.page_id
2. `schema_version: "3.3"` → 固定值
3. `type:` → 來自 payload.page_intent.type
4. `entity:` → 來自 payload.page_intent.entity（不修改大小寫）
5. `api:` → 來自 payload.page_intent.api（對應 haAPI api: id）
6. `title:` → 來自 payload.page_intent.title
7. `view:` / `form:` → 依 page type 和 payload 生成
8. `security.permission_refs` → 依 payload 的 auth 資訊生成
9. `cic_notes:` → 僅包含 payload 傳入的 CiC notes

**嚴格禁止**：`security.permissions:`（不論任何情況）；**一檔一頁，頂層必為 `page:`，禁止 `meta:`/`pages:` 包裝**。

### 步驟 3：WRITE 到 payload.output_file

WRITE 生成的 YAML 到 payload.output_file。**每個 page 一個檔案**（多頁面 → 多次 DELEGATE，不可打包）。

### 步驟 3.5：RUN dsl-lint（生成當下驗證，shift-left）⭐

```
RUN: python {rapt-verify::references/dsl-lint.py} --file {payload.output_file} --levels 1,2,3
若出現任何 ERROR（HAPDL-SCHEMA-* / HAPDL-LINT-* / DSL-PARSE-*）：
  → 依 lint 的 fix 指引修正 YAML，重新 WRITE，再次 RUN
  → 直到 0 ERROR 才進入步驟 4
```

重點：頂層必須是 `page`（非 `page_id`）；禁止 `meta`/`pages`；`security.permission_refs.{action}[].id` 格式。

### 步驟 4：EMIT 完成確認

```
✅ haPDL 已生成並通過 dsl-lint：{output_file}
page: {page}，type: {type}，entity: {entity}
```
## Worker Failure Contract

Worker ???????????????????????????????

```yaml
worker_result:
  status: failed
  failure_kind: invalid_payload | missing_evidence | contract_violation | dsl_lint_failed | unsupported_case
  target_path: <payload.target_path>
  message: <????>
  required_action: <Planner ??????????>
```

