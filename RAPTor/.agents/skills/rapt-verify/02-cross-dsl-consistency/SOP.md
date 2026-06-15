# 02 Cross-DSL Consistency Check SOP

**目的**：依 `rapt-core::dsl-cross-reference-v33.md` 的規則，驗證跨 DSL 引用的一致性。

---

## 步驟 2.0：執行程式化 lint（取代人工目視）⭐

跨 DSL 一致性已由 `dsl-lint.py` 的 L4 機械化（規則來源同為 `dsl-cross-reference-v33.md`）。**優先呼叫 lint 取得客觀結果**，再據以填寫 report：

```
RUN: python {skill_dir}/references/dsl-lint.py \
       --haapi {paths.backend_intent_dir} \
       --hapdl {paths.frontend_intent_dir} \
       --dbml  {paths.dbml_file} \
       --haarm {paths.haarm_file} \
       --levels all --format json
```

- lint exit code != 0 或 JSON 內含 `severity: ERROR` → 本步驟 FAIL。
- 將 lint 的 `XREF-*`（跨 DSL）、`HAAPI-SCHEMA-*` / `HAPDL-SCHEMA-*`（結構）、`*-LINT-*`（語意）findings 全數收錄到 `consistency_result.errors / warnings`，**保留 `fix` 欄位**作為修正指引。
- rapt-verify 維持唯讀；修正交由 `rapt-reconcile`。

> 下列 2.1–2.5 為 lint 規則的人類可讀對照（lint 不可用時的 fallback 檢查清單），平時以 2.0 的程式化結果為準。

---

## 步驟（對照清單 / fallback）

### 2.1 entity: case-sensitive 一致性

對每個 haAPI / haPDL 中的 `entity:` 值：
- READ DBML Table Names（uppercase first）
- ASSERT `entity:` 值能 exact-match DBML Table Name

### 2.2 haAPI → haARM 引用

對每個 `required_roles` / `required_permissions`：
- ASSERT role.id 存在於 haARM
- ASSERT permission.id 存在於 haARM

### 2.3 haPDL → haAPI 引用

對每個 haPDL 的 `api:` 值：
- ASSERT 對應的 `{api_id}.haapi.yaml` 存在

### 2.4 haPDL → haARM permission_refs

對每個 `security.permission_refs.{action}[].id`：
- ASSERT permission.id 存在於 haARM

### 2.5 FORBIDDEN 欄位掃描

掃描所有 haAPI 中的 `access.permissions:`（deprecated）→ FAIL  
掃描所有 haPDL 中的 `security.permissions:`（deprecated）→ FAIL

### 2.6 OUTPUT consistency_result

```yaml
cross_dsl:
  status: PASS | PARTIAL | FAIL
  errors: []      # R-API-* / R-PDL-* 違規
  warnings: []
```
