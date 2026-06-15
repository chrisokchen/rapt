# CiC 便條紙（Contextual in-Context Notes）政策

CiC 便條紙是 RAPTor skill 在執行過程中，對**無法立即解決**的問題所留下的結構化記錄，供後續流程處理或人工決策。

---

## 四種 CiC 類型

| 類型 | 觸發情境 | 主要處理方 |
|------|---------|---------|
| `GAP` | 資訊缺失，無法從現有 artifact 推斷 | `rapt-clarify`（需人工回答）|
| `ASM` | 做了假設，但來源不確定，需確認 | `rapt-clarify`（請確認假設是否正確）|
| `BDY` | 超出本 skill 授權邊界的操作 | `rapt-reconcile`（機械性）或 `rapt-clarify`（語意性）|
| `CON` | 兩個來源有衝突，需裁決 | `rapt-clarify`（輔以 rapt-verify 掃描）|

---

## CiC 便條紙格式

```markdown
<!-- CiC [GAP|ASM|BDY|CON] #{序號} -->
**類型**：GAP / ASM / BDY / CON
**位置**：<檔案路徑>#<L行號 或 §節標題>
**描述**：<簡短描述問題>
**影響**：<如果不解決，會影響哪些下游 artifact>
**推薦**：<推薦的處理方向（可選）>
<!-- /CiC -->
```

### 範例

```markdown
<!-- CiC GAP #001 -->
**類型**：GAP
**位置**：docs/02-data-model/schema.dbml#OrderItem.discountRate
**描述**：`discountRate` 的業務規則不明——是訂單級折扣還是商品級折扣？
**影響**：haARM permission scope 設計、haAPI 計算邏輯
**推薦**：向業主確認折扣計算層級
<!-- /CiC -->
```

---

## CiC 存放位置

| 情境 | 存放位置 |
|------|---------|
| 關於某個 SSoT 檔案的問題 | 直接內嵌在該 SSoT 檔案的相關位置（用 HTML 注釋）|
| 跨多個 artifact 的問題 | `{paths.clarify_dir}/backlog.md` |
| 執行日誌中的問題摘要 | `.raptor/session.md` |

---

## CiC 生命週期

```
1. EMIT：skill 發現問題 → 記 CiC 便條
2. COLLECT：rapt-clarify `01-gap-scan` 收集所有 CiC
3. PACKAGE：rapt-clarify `02-question-packaging` 打包成問題集
4. SESSION：rapt-clarify `03-clarification-session` → ASK 使用者
5. APPLY：rapt-clarify `04-decision-apply` → 決策回寫 SSoT
6. CLOSE：CiC 標記為 RESOLVED，附上 decision log 引用
```

---

## CiC 處理規則

1. **不得跳過 CiC**：即使有把握的推斷，若無可追溯的 source evidence，仍需記 `ASM`。
2. **GAP 不得自行填補**：`GAP` 類型必須由 `rapt-clarify` 通過 ASK 解決，skill 本身不得自行填入任何值。
3. **BDY 的跳轉規則**：
   - 機械性缺失（missing id）→ DELEGATE to `rapt-reconcile`
   - 語意不明（需設計決策）→ DELEGATE to `rapt-clarify`
4. **CON 的跳轉規則**：先記 CiC，再由 `rapt-verify` 的 cross-dsl consistency 掃描確認範圍，最後由 `rapt-reconcile` 修正。
5. **cic_notes_enabled = false 時**：跳過 CiC 記錄；遇到 GAP 改為 EMIT 錯誤並停止流程。
