---
name: rapt-design-brief
description: "RAPTor Preview Tool：從 haPDL + annotated DBML + haARM 生成結構化 Design Brief markdown，供 Claude Design 或 AI 設計工具直接生成 Hi-Fi UI。Use when: /rapt-design-brief、設計稿、Design Brief、Claude Design。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: preview
---

# RAPTor Design Brief — UI 設計稿摘要生成器（Preview Tool）

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::preview-audit-schema.md]

## TRIGGER

- 使用者執行 `/rapt-design-brief`，或要求產生給 Claude Design / AI 設計工具的 Design Brief。
- haPDL、DBML、haARM SSoT 已就緒，需要結構化設計稿摘要以生成 Hi-Fi mockup。

## SKIP

- 對應的 SSoT 尚未就緒，或仍有未解的 blocker finding。
- 尚未具備 DBML、haBDD、haARM、haAPI 或 haPDL SSoT。
- `generated.status` 尚未開啟，禁止產生 generated output。


## PRINCIPLE: Artifact Output Contract（只寫 Design Brief markdown，不修改任何 SSoT）
## PRINCIPLE: CWD 為產出錨點
## PRINCIPLE: STRICT SOP

---

## 功能定位

本 skill 是 **Preview Tool（預覽工具）**，讀取 Phase 4（haPDL）、Phase 2（DBML、haARM）的 SSoT artifacts，自動生成一份 **結構化的 Design Brief markdown**，包含：

1. **Design System** — 色彩、字型、間距、元件庫規範
2. **Navigation Map** — 側邊欄結構與頁面流程圖
3. **Per-page Specifications** — 每頁的欄位定義、widget 類型、enum 值、badge 色碼、action 按鈕
4. **Sample Data** — 每頁 JSON 範例資料
5. **Generation Instructions** — 給 AI 設計工具的生成指令

產出的 markdown 可直接複製貼上到 **Claude Design** 或其他 AI 設計工具，生成 Hi-Fi mockup 或 React/HTML 程式碼。

**本 skill 不修改任何 SSoT artifact。**

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| CREATE / UPDATE | `docs/generate/designbrief/design-brief.md`（預設） | Design Brief markdown |
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
DERIVE: project_desc ← project.description
DERIVE: project_lang ← project.language
```

如果 `.raptor/arguments.yml` 不存在，使用預設路徑。

### 步驟 1：ASSERT 輸入存在

```
ASSERT: hapdl_dir 存在且包含至少一個 *.hapdl.yaml
ASSERT: dbml_path 存在
ASSERT: haarm_path 存在
若 ASSERT 失敗 → EMIT 錯誤訊息，列出缺少的檔案，停止
```

### 步驟 2：EXECUTE 生成 Design Brief

```
EXECUTE: python rapt-design-brief/scripts/hapdl2brief.py \
    --hapdl  {hapdl_dir} \
    --dbml   {dbml_path} \
    --haarm  {haarm_path} \
    --output docs/generate/designbrief/design-brief.md \
    --title  "{project_name}" \
    --description "{project_desc}" \
    --language "{project_lang}"
```

### 步驟 3：EMIT 完成摘要

```
[OK] Design Brief 已生成：docs/generate/designbrief/design-brief.md

  pages: {N} 個
  entities: {M} 個
  file size: {K} KB

使用方式：
  將 design-brief.md 的完整內容複製貼上到 Claude Design，
  即可生成 Hi-Fi mockup 或 React/HTML 程式碼。
```

## Preview Audit Gate

ASSERT:
- Preview skill 僅寫入 `docs/generate/**`，不得修改 `docs/ssot/**`。
- 每次 generated artifact 產出後都附上對應的 audit YAML。
- audit findings 標註 `route` 與 `can_fix`，格式依 `rapt-core::preview-audit-schema.md`。

