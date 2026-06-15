# 03 Clarification Session SOP

**目的**：以批次 ASK 方式向使用者呈現問題集，等待回應，記錄決策。

---

## 步驟

### 3.1 READ 最優先的 PENDING batch

```
READ: ${clarify_dir}decisions/batch-{最新批次}.md
DERIVE: PENDING 狀態的問題清單
```

### 3.2 DELEGATE `rapt-clarify-loop`

DELEGATE to `rapt-clarify-loop` 執行互動 session：

```yaml
payload:
  batch_file: "${clarify_dir}decisions/batch-{id}.md"
  batch_id: CLR-{id}
  questions: [<question list from batch>]
  max_per_ask: {policy.clarify_batch_size}
```

`rapt-clarify-loop` 負責：
- 呈現問題（格式見 `rapt-clarify-loop::references/question-format.md`）
- 等待回應（ASK yield）
- 記錄回答到 batch 檔案

### 3.3 LOOP until all questions answered

```
WHILE batch 中有 PENDING 問題：
  DELEGATE rapt-clarify-loop（下一批）
  等待回應
  繼續下一批
```

### 3.4 UPDATE batch 狀態為 ANSWERED

當所有問題回答完畢：
- UPDATE `${clarify_dir}decisions/batch-{id}.md` → 狀態改為 `ANSWERED`
- UPDATE `${clarify_dir}backlog.md` → 相關 CiC 標記為 `ANSWERED`

### 3.5 EMIT session 摘要

```
已回答的問題：
  GAP → {決策摘要}
  ASM → {確認/拒絕}
  CON → {裁決結果}
  BDY → {已轉 reconcile/clarify}

尚未處理的 CiC：{N} 個
```
