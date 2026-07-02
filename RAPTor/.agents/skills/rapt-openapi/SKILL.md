---
name: rapt-openapi
description: "RAPTor Preview Tool：從 haAPI + haARM + annotated DBML 生成 OpenAPI 3.0.3 YAML，供 Swagger UI / Redocly 預覽 API 規格。Use when: /rapt-openapi、預覽 API、產生 OpenAPI spec。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: preview
---

# RAPTor OpenAPI — API 規格預覽生成器（Preview Tool）

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::preview-audit-schema.md]

## TRIGGER

- 使用者執行 `/rapt-openapi`，或要求產生 OpenAPI spec / API 規格預覽。
- haAPI、DBML、haARM SSoT 已就緒，需要可供 Swagger UI / Redocly 檢視的 OpenAPI 3.0.3 YAML。

## SKIP

- 對應的 SSoT 尚未就緒，或仍有未解的 blocker finding。
- 尚未具備 DBML、haBDD、haARM、haAPI 或 haPDL SSoT。
- `generated.status` 尚未開啟，禁止產生 generated output。


## PRINCIPLE: Artifact Output Contract（只寫 OpenAPI YAML，不修改任何 SSoT）
## PRINCIPLE: CWD 為產出錨點
## PRINCIPLE: STRICT SOP

---

## 功能定位

本 skill 是 **Preview Tool（預覽工具）**，讀取 Phase 2（DBML、haARM）和 Phase 4（haAPI）的 SSoT artifacts，自動生成 OpenAPI 3.0.3 YAML 文件。

產出的 OpenAPI spec 可用以下工具即時預覽：
- `npx swagger-ui-watcher openapi.yaml`
- `npx @redocly/cli preview-docs openapi.yaml`

**本 skill 不修改任何 SSoT artifact。**

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| CREATE / UPDATE | `docs/generate/openapi/openapi.yaml`（預設） | OpenAPI 3.0.3 YAML |
| **DENY** | `docs/02-data-model/*` | 只讀 |
| **DENY** | `docs/03-access-control/*` | 只讀 |
| **DENY** | `docs/05-backend-intent/*` | 只讀 |
| **DENY** | 任何其他 SSoT artifact | |

---

## 輸入路徑（從 arguments.yml 解析）

| 鍵 | 預設路徑 | 說明 |
|----|---------|------|
| `paths.backend_intent_dir` | `docs/05-backend-intent/` | `*.haapi.yaml` 所在目錄 |
| `paths.data_model_dir` | `docs/02-data-model/` | `schema.dbml` 所在目錄 |
| `paths.access_control_dir` | `docs/03-access-control/` | `*.haarm.yaml` 所在目錄 |

---

## SOP

### 步驟 0：READ arguments.yml

```
READ: .raptor/arguments.yml
DERIVE: haapi_dir ← paths.backend_intent_dir（預設 docs/05-backend-intent/）
DERIVE: dbml_path ← 在 paths.data_model_dir 下找 *.dbml
DERIVE: haarm_path ← 在 paths.access_control_dir 下找 *.haarm.yaml
DERIVE: project_name ← project.name
DERIVE: project_desc ← project.description
```

如果 `.raptor/arguments.yml` 不存在，使用預設路徑。

### 步驟 1：ASSERT 輸入存在

```
ASSERT: haapi_dir 存在且包含至少一個 *.haapi.yaml
ASSERT: dbml_path 存在
ASSERT: haarm_path 存在
若 ASSERT 失敗 → EMIT 錯誤訊息，列出缺少的檔案，停止
```

### 步驟 2：EXECUTE 生成 OpenAPI

```
EXECUTE: python rapt-openapi/scripts/haapi2openapi.py \
    --haapi  {haapi_dir} \
    --dbml   {dbml_path} \
    --haarm  {haarm_path} \
    --output docs/generate/openapi/openapi.yaml \
    --title  "{project_name}" \
    --description "{project_desc}"
```

### 步驟 3：EMIT 完成摘要

```
[OK] OpenAPI 3.0.3 spec 已生成：docs/generate/openapi/openapi.yaml

  paths: {N} 個
  operations: {M} 個
  schemas: {K} 個

預覽：
  npx swagger-ui-watcher docs/generate/openapi/openapi.yaml
  npx @redocly/cli preview-docs docs/generate/openapi/openapi.yaml
```

## Preview Audit Gate

ASSERT:
- Preview skill 僅寫入 `docs/generate/**`，不得修改 `docs/ssot/**`。
- 每次 generated artifact 產出後都附上對應的 audit YAML。
- audit findings 標註 `route` 與 `can_fix`，格式依 `rapt-core::preview-audit-schema.md`。

