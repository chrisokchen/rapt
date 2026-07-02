---
name: rapt-clarify-loop
description: "RAPTor 釐清互動循環。僅由 rapt-clarify DELEGATE 呼叫，負責以格式化方式呈現問題集並等待使用者回應。是 skill 家族中主要的 ASK yield 執行者。"
metadata:
  user-invocable: false
  source: project-level
  skill-type: utility
---

# RAPTor Clarify Loop — 釐清互動循環

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::verb-cheatsheet.md]
- LOAD REF [rapt-clarify-loop::references/question-format.md]

## TRIGGER

- `rapt-clarify`（03-clarification-session）透過 DELEGATE 傳入 payload 呼叫 `rapt-clarify-loop`。
- payload 含 `batch_file`、非空的 `questions` 與 `max_per_ask`。

## SKIP

- payload 缺少 `batch_file`，或 `questions` 為空（回傳錯誤給 caller）。
- 使用者未經 `rapt-clarify` 直接呼叫；應改用 `/rapt-clarify` 走完整 Phase 3 流程。
- 需要掃描 CiC、打包問題或將決策回寫 SSoT 的工作；那些屬於 `rapt-clarify` 的 01/02/04 sub-SOP。


## PRINCIPLE: Artifact Output Contract（只更新 payload.batch_file）
## PRINCIPLE: STRICT SOP

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| UPDATE | `payload.batch_file` | 在 batch 檔案中記錄回答 |
| **DENY** | 任何 SSoT artifact | 不修改 DBML / haARM / Gherkin |
| **DENY** | 任何其他路徑 | |

---

## SOP

### 步驟 0：ASSERT payload

```
ASSERT: payload.batch_file 存在
ASSERT: payload.questions 非空
ASSERT: payload.max_per_ask >= 1
若失敗 → EMIT 錯誤，停止
```

### 步驟 1：LOAD question format

LOAD REF [rapt-clarify-loop::references/question-format.md]

### 步驟 2：ASK — 呈現問題集

依 question-format.md 的格式，一次呈現最多 `max_per_ask` 個問題（yield，等待使用者回應）。

### 步驟 3：RECORD 回答

將使用者的回答記錄到 `payload.batch_file` 的「回答記錄」區：

```markdown
## 回答記錄

### Q1 [{CiC-id}] 回答：{選項或自由文字}
> 回答時間：{datetime}
> 決策摘要：{AI 從回答推導的決策}
```

### 步驟 4：UPDATE batch 狀態

若所有問題已回答：UPDATE `payload.batch_file` 狀態為 `ANSWERED`。

### 步驟 5：EMIT 回應確認

```
已記錄回答（{N}/{total} 個問題）
```

然後 RETURN to caller（`rapt-clarify/03-clarification-session`）。
