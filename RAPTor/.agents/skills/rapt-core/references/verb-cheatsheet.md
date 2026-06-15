# Verb 速查表

RAPTor skill SOP 使用三類動詞（D / S / I），決定步驟是否可 yield 給使用者。

---

## D 類（Deterministic）：直接輸出，不 yield

無需詢問，直接以讀取、計算、推導或生成完成。

| 動詞 | 語義 |
|------|------|
| `READ` | 讀取檔案、spec、現有 artifact |
| `PARSE` | 解析結構化資料（YAML/JSON/DBML）|
| `DERIVE` | 從已讀內容計算、推導 |
| `ASSERT` | 聲明不變式或前提；失敗則 EMIT 錯誤停止 |
| `THINK / REASON` | 內省/延伸推理（僅當 SOP 明文標示此步才用）|
| `SEARCH` | 搜尋工作區或文件 |
| `VALIDATE` | 對照規則驗證結構/引用 |

---

## S 類（Side-effecting）：寫入，不 yield

有副作用（建立/更新/刪除 artifact），但**無須中斷等待**使用者確認。

| 動詞 | 語義 |
|------|------|
| `CREATE` | 建立新檔案 / 新 artifact |
| `WRITE` | 寫入（覆蓋）現有或新路徑 |
| `UPDATE` | 部分更新現有 artifact |
| `DELETE` | 刪除已授權的 artifact（須 confirm：需先 ASK 或 EMIT）|
| `DELEGATE` | 委派子 skill 完成 payload 中定義的工作 |
| `EMIT` | 輸出訊息 / 摘要 / 進度報告給使用者（不 yield）|

---

## I 類（Interactive）：唯一可 yield 的動詞

**只有 `ASK` 可以讓 skill 在此暫停、等待使用者回應後繼續。**

| 動詞 | 語義 |
|------|------|
| `ASK` | 呈現問題集給使用者，等待回應，繼續 |

### Yield 紀律

1. `ASK` 一次只呈現一批問題（`clarify_batch_size` 上限，預設 5）。
2. `ASK` 之後，在使用者回應前，SOP **絕對停止**；不得自行假設答案繼續。
3. 只有 sub-SOP 中明文標示 `ASK` 的步驟才能 yield；未標示的步驟**不得暗中等待**。
4. `EMIT` 不是 `ASK`——輸出摘要或狀態報告不 yield。

---

## 禁止動詞

| 禁止 | 原因 |
|------|------|
| 以推論替代 `ASK` | 語意不明確時必須 ASK，不得自行填補 |
| 在 `THINK` 步驟中寫入 artifact | THINK 是分析，不是 S 類 |
| 未授權的 `DELETE` | 需明確出現在 SOP + 前置 EMIT 通知 |
