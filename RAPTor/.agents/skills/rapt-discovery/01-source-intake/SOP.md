# 01 Source Intake SOP

**目的**：讀取所有輸入 source（需求文件、RFP、會議記錄、現有系統等），建立 source 清單與摘要。

---

## 步驟

### 1.1 READ 輸入路徑

```
READ: arguments.yml → paths.docs_dir, paths.business_discovery_dir, anchors.req_process_root
```

SEARCH 以下位置是否有輸入 source：

- `${paths.docs_dir}` 內所有 `.md` / `.txt` / `.pdf` 檔案
- 使用者在呼叫時提供的附件或貼入文字

### 1.2 ASK（如無任何 source）

若在 `${paths.docs_dir}` 沒有找到任何文件：

```
ASK：
  1. 請貼入或告知需求文件的位置（或直接貼入文字）
  2. 是否有 RFP / 提案書 / 會議記錄？
  3. 本系統是全新開發還是改版現有系統？
```

### 1.3 DERIVE Source Inventory

對每個 source 建立：

```markdown
## Source: <檔名或描述>
- 路徑：<相對路徑或「使用者貼入」>
- 類型：rfp | meeting_notes | existing_system | proposal | other
- 摘要：<2-3 句話描述核心內容>
- 重要業務概念：<列出 3-5 個>
```

### 1.4 WRITE `${disc_dir}00-source-inventory.md`

彙整所有 source 的清單與摘要。格式：

```markdown
# Source Inventory

> 建立時間：{date}
> 來源數量：{N}

## 輸入文件清單

| # | 來源 | 類型 | 核心內容摘要 |
|---|------|------|------------|
| 1 | ...  | ...  | ...        |

## 萃取的關鍵業務概念

1. ...
2. ...
```

---

## 常見問題

- **source 太長**：每份文件只摘 3-5 個關鍵業務概念，細節留給後續步驟深挖
- **無任何 source**：必須 ASK，不得以「一般電商系統」等假設繼續
- **有衝突的多份 source**：記 CiC `CON`，繼續其他步驟
