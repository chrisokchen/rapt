# 04 Decision Apply SOP

**目的**：將 session 中的決策套用回 SSoT artifact（DBML / haARM / Gherkin / discovery CiC 狀態 / seeds / constraints / traceability）。這是 `rapt-clarify` 中**唯一可以回寫 SSoT** 的步驟。

---

## ⚠ 重要限制

```
只有本步驟（04-decision-apply）可以回寫 SSoT。
步驟 01、02、03 嚴禁回寫任何 SSoT。
```

---

## 步驟

### 4.1 READ ANSWERED batches

```
READ: ${clarify_dir}decisions/batch-*.md（ANSWERED 狀態）
DERIVE: 每個決策的 action plan（要修改什麼、改成什麼）
```

### 4.2 PLAN artifact updates

對每個 ANSWERED decision，DERIVE：

```yaml
update_plan:
  - decision_id: CiC-001
    decision: "B（訂單明細折扣率）"
   target_artifact: "${data_model_dir}schema.dbml"
    change_type: add_column | modify_column | add_table | add_scenario | modify_permission | update_seed | update_constraint | update_scope | update_traceability | mark_cic_resolved
    change_description: "在 OrderItem 添加 discountRate decimal(5,4)"
    source_evidence:
      type: clarify_decision
      ref: "${clarify_dir}decisions/batch-{id}.md#Q1"
```

### 4.3 VALIDATE update_plan

ASSERT：
- 每個 update 都有 `source_evidence` 指向 decision log
- 修改範圍在 Artifact Output Contract 內（DBML / haARM / Gherkin / discovery CiC 狀態 / seeds / constraints / traceability）
- 不修改 haAPI / haPDL（那是 rapt-intent 的責任）

### 4.4 EXECUTE updates

依 update_plan，對每個 artifact 執行修改：

**若修改 DBML**：直接 UPDATE（修改前先 READ 確認）  
**若修改 haARM**：直接 UPDATE（修改前先 READ 確認）  
**若修改 Gherkin**：DELEGATE to `rapt-form-gherkin` 重新渲染
**若補值域 / 狀態 / 位元旗標**：UPDATE `${paths.data_model_dir}/seeds.md`
**若補約束 / 補償規則**：UPDATE `${paths.data_model_dir}/constraints.md`
**若同步 scope 或 CiC 狀態**：UPDATE `${paths.business_discovery_dir}/**`，僅限相關 CiC 狀態、decision reference、scope 同步段
**若補 traceability**：UPDATE `${paths.traceability_file}` 的 L2 / L3 / Decision Traceability 區段

### 4.5 UPDATE backlog 和 batch 狀態

```
UPDATE ${clarify_dir}backlog.md：
  - 已處理的 CiC → status: RESOLVED，附 decision log 引用
  
UPDATE ${clarify_dir}decisions/batch-{id}.md：
  - 狀態改為 APPLIED
```

### 4.6 EMIT 套用結果

```
已套用的決策：
  - DBML 更新：{N} 處
  - haARM 更新：{M} 處
  - Gherkin 更新：{P} 個 Feature

RESOLVED CiC：{X} 個
剩餘 OPEN CiC：{Y} 個
```

---

## 邊界規則

- **BDY（超界）類型**不在此步驟處理，已轉送 `rapt-reconcile` 或留在 backlog
- **若修改幅度超出預期**（如需要新增大量 Table），EMIT 警告，ASK 確認後才繼續
- **deferred 項目**必須落在 `deferred-mvp-out`、`deferred-needs-decision`、`accepted-risk` 三者之一，並寫入 traceability 或 backlog
- **RAscore 來源決策**必須保留 finding id 與 criterion，方便重跑 RAscore 比對
