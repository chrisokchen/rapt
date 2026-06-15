---
name: rapt-lofi
description: "RAPTor Preview Tool：從 haPDL + annotated DBML + haARM 生成自包含的 Lo-Fi wireframe HTML，供開發者預覽頁面意圖。Use when: /rapt-lofi、預覽頁面、Lo-Fi wireframe。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: preview
---

# RAPTor Lo-Fi — 頁面 Wireframe 預覽生成器（Preview Tool）

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::preview-audit-schema.md]

## TRIGGER

- ???????????? preview / generated artifact?
- SSoT ???????? SSoT ????????

## SKIP

- ?? SSoT ?????? blocker finding?
- ??????? DBML?haBDD?haARM?haAPI ? haPDL SSoT?
- `generated.status` ?????? generated output?


## PRINCIPLE: Artifact Output Contract（只寫 HTML wireframe，不修改任何 SSoT）
## PRINCIPLE: CWD 為產出錨點
## PRINCIPLE: STRICT SOP

---

## 功能定位

本 skill 是 **Preview Tool（預覽工具）**，讀取 Phase 4（haPDL）、Phase 2（DBML、haARM）的 SSoT artifacts，自動生成一個 **self-contained HTML 檔案**，以 lo-fi wireframe 呈現所有 haPDL 頁面：

- 列表頁（list）：filter bar + sortable table + pagination
- 表單頁（form）：label-value 表單 + enum dropdown + sensitive field mask
- 明細頁（detail）：key-value 佈局 + action buttons

所有欄位標籤、enum 值、角色權限均直接從 SSoT 讀取，不需手工維護。

**本 skill 不修改任何 SSoT artifact。**

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| CREATE / UPDATE | `docs/generate/lofi/index.html`（預設） | Self-contained wireframe HTML |
| **DENY** | `docs/02-data-model/*` | 只讀 |
| **DENY** | `docs/03-access-control/*` | 只讀 |
| **DENY** | `docs/06-frontend-intent/*` | 只讀 |
| **DENY** | 任何其他 SSoT artifact | |

---

## 輸入路徑（從 arguments.yml 解析）

| 鍵 | 預設路徑 | 說明 |
|----|---------|------|
| `paths.frontend_intent_dir` | `docs/06-frontend-intent/` | `*.hapdl.yaml` 所在目錄 |
| `paths.data_model_dir` | `docs/02-data-model/` | `schema.dbml` 所在目錄 |
| `paths.access_control_dir` | `docs/03-access-control/` | `*.haarm.yaml` 所在目錄 |

---

## SOP

### 步驟 0：READ arguments.yml

```
READ: .raptor/arguments.yml
DERIVE: hapdl_dir ← paths.frontend_intent_dir（預設 docs/06-frontend-intent/）
DERIVE: dbml_path ← 在 paths.data_model_dir 下找 *.dbml
DERIVE: haarm_path ← 在 paths.access_control_dir 下找 *.haarm.yaml
DERIVE: project_name ← project.name
```

如果 `.raptor/arguments.yml` 不存在，使用預設路徑。

### 步驟 1：ASSERT 輸入存在

```
ASSERT: hapdl_dir 存在且包含至少一個 *.hapdl.yaml
ASSERT: dbml_path 存在
ASSERT: haarm_path 存在
若 ASSERT 失敗 → EMIT 錯誤訊息，列出缺少的檔案，停止
```

### 步驟 2：EXECUTE 生成 Lo-Fi HTML

```
EXECUTE: python rapt-lofi/scripts/hapdl2lofi.py \
    --hapdl  {hapdl_dir} \
    --dbml   {dbml_path} \
    --haarm  {haarm_path} \
    --output docs/generate/lofi/index.html \
    --title  "{project_name}"
```

### 步驟 3：EMIT 完成摘要

```
[OK] Lo-Fi wireframe 已生成：docs/generate/lofi/index.html

  pages: {N} 個
  entities: {M} 個
  file size: {K} KB

預覽：
  python -m http.server 8089 --directory docs/generate/lofi
  # 然後開啟 http://localhost:8089
```

## Preview Audit Gate

ASSERT:
- Preview skill ?? `docs/generate/**`???? `docs/ssot/**`?
- ?? generated artifact ?????????? audit YAML?
- audit findings ???? `route` ? `can_fix`????? `rapt-core::preview-audit-schema.md`?
