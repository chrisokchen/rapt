# rapt-human-sync 設計導覽（簡報插頁）

> 受眾：BA / PO / PM、以及已看過《RAPTor 30 分鐘導覽》的團隊
> 形式：可獨立講 5–8 分鐘的小段落，也可整段插進主簡報（建議插在主簡報 Slide 20「需求變更時：迴圈，不是重做」之後）
> 對應實作計畫：`ccwLog/0613plan-rapt-human-sync_cc-Opus48.md`
> 產出檔：`0613plan-rapt-human-sync_presentation_cc-Opus48.pptx`（5 張，16:9，沿用主簡報視覺風格）
>
> 一句話定位：**rapt-human-sync 是「人工改動進入 RAPTor 可追蹤世界的海關」——讓你親手改的 SSoT，也能被流程認得、被驗證、被追溯。**

---

## Slide 1 — 封面 / 缺口

**人工改了規格之後，流程怎麼接？**
rapt-human-sync：把人工改動納入 RAPTor 的追蹤體系

副標：你照樣用 VSCode 改 SSoT，AI 負責登錄「誰、何時、改了什麼、為什麼」並接回驗證

缺口場景（封面下方一行）：
> Phase 跑完，你打開 `schema.dbml` 手動加了兩個欄位——這時 RAPTor 不知道你改了什麼、影響哪些下游、為什麼改。traceability 就在這裡斷鏈。

> 講者備註：先點痛。RAPTor 的五份 SSoT 由 skill 產生時都帶 source_evidence 與 traceability，唯獨「人親手改」這條路徑是個黑洞。這頁就是要讓聽眾認同「人工改動需要一道登錄關卡」，而不是預設大家都會乖乖手寫 impact-matrix。

---

## Slide 2 — 設計理念：做得少，接得準

四個原則（卡片）：

| 原則 | 說明 |
|---|---|
| **海關，不是修復器** | 只負責「登錄」人工改動，**絕不改 SSoT、不自動 reconcile、不重產下游**。判斷對錯交給既有的 verify → reconcile → clarify 迴圈 |
| **Git 是唯一事實來源** | Who / When / What 全部從 `git diff` / `git log` 拿，不另造一套追蹤機制（避免雙重真相來源） |
| **Why 用問的，不用猜** | Git 能回答「改了什麼」，回答不了「為什麼改」——用 ASK 補 `human_note` 與 `decision_ref`，才不會 traceability 斷鏈 |
| **零設定、不依賴 git 紀律** | 預設支援「還沒 commit」就能跑（working-tree 模式）；baseline 自動從 git 推導，**不必改任何既有 skill** |

在流程中的位置：

```
人工修改 SSoT（VSCode 手改）
        │
        ▼
/rapt-human-sync   ← 新增的「海關」：偵測 diff → 問原因 → 寫登錄紀錄
        │
        ▼
/rapt-verify       ← 既有：重跑驗證（只讀、出報告）
        │
   ┌────┴─────┐
   ▼          ▼
/rapt-reconcile   /rapt-clarify   ← 既有：機械性自動修 / 語意性退給人
```

> 講者備註：這頁是全段核心。強調「少發明、多接線」——RAPTor 已經有完整的驗證迴圈，human-sync 不重造輪子，只補上 verify 之前缺的那一塊「人工變更事件登錄」。第四點是最大的好用度賣點：使用者不需要懂 git、不需要事先 commit，跑一個指令就好。

---

## Slide 3 — 使用情境：三個時間點，兩條 git 命令

時間線：

```
時間軸 ───────────────────────────────────────────────────────►
  ① Phase 結束              ② 人工修改                ③ 接回 RAPTor
     │                         │                          │
     ▼                         ▼                          ▼
  （skill 收手，             用 VSCode 手改 SSoT       /rapt-human-sync
   session.md 已記錄）        例：Order 加 totalWeight   → 偵測 diff
                              shippingMethod 兩個欄位     → ASK：為什麼改？
                                                          → 寫登錄紀錄 + impact-matrix
                                                         /rapt-verify
                                                          → 驗證人工改動後的一致性
```

**最精簡：只要記兩條 git 命令（進階者用，新手可略）**

| 時機 | 命令 | 為什麼 |
|---|---|---|
| 改之前 | `git commit -m "raptor: Phase N done"` | 畫一條 baseline 線，讓 diff 知道從哪裡算起 |
| 改之後 | `git commit -m "human: 加入物流欄位"` | 記下 who / when，`human:` 前綴方便區分人工 vs skill |

**但你也可以什麼都不記**：直接改、直接 `/rapt-human-sync`。它會偵測到未 commit 的變更，提醒你 who/when 只能記成「目前操作者 + 掃描時間」，仍照常登錄。

> 講者備註：呼應討論裡使用者問的「改前改後要下什麼 git 命令」。重點是給兩種人兩條路：(1) 重視 provenance 的人 → 兩條 commit 命令，who/when 完整可信；(2) 不想記指令的人 → 零設定直接跑，可信度標示清楚但不擋路。不要把「先 commit」當成硬性前置條件，那是最大的採用門檻。

---

## Slide 4 — 操作步驟：跑 `/rapt-human-sync` 發生了什麼

| 步驟 | 動作 | 產出 / 行為 |
|---|---|---|
| **0 解析 baseline** | 自動從 git 推導上次 skill 收手點（`--baseline` 可手動指定）；找不到就**停下來問**，絕不亂猜 | 確定「從哪裡開始算人工改動」 |
| **1 掃描變更** | `git diff` 找出 `docs/ssot/**` 改了哪些檔（排除 `.raptor/`、`generate/`，避免自我餵食） | 結構化變更清單（檔案、hunk、entity） |
| **2 問原因（ASK）** | 先問這批改動的**共同原因**，再只針對高風險變更追問 | 填入 `human_note`、`decision_ref` |
| **3 評估影響** | 依 DSL 類型推下游：改 DBML → 需驗 haAPI / haPDL / haARM | 標記 `affected_dsls`、風險等級（刪除/改名→高） |
| **4 寫登錄紀錄** | 產 `.raptor/human-sync/HSYNC-*.yml`；用既有工具寫 `impact-matrix.yml`（`status: open`） | 人工改動正式進入追蹤檔 |
| **5 接回流程** | 在 traceability 加一筆人工變更；EMIT 建議下一步 | 「建議執行 `/rapt-verify` 驗證一致性」 |

產出物（都在 `.raptor/`，不碰你的 SSoT）：
`human-sync/HSYNC-YYYYMMDD-NNN.yml` ・ 更新 `impact-matrix.yml` ・ 更新 `traceability.md` ・ 追加 `session.md` 摘要

> 講者備註：強調三件落地保證：(1) 全程**不寫任何 SSoT 檔**，只寫 `.raptor/` 下的追蹤檔；(2) impact-matrix 一律透過既有的 `manage_impact_matrix.py` 寫入並 validate，格式不會跑掉；(3) 同樣狀態重跑不會產生重複紀錄（用內容決定性 id 去重）。這頁回答「它到底動了我什麼」——答案是：只動追蹤檔，你的規格一個字都不改。

---

## Slide 5 — 邊界與常見疑問

**human-sync 不做的事（白紙黑字的不變式）**

- ❌ 不改任何 SSoT artifact　❌ 不重產 OpenAPI / Lo-Fi 等下游
- ❌ 不自動 reconcile　❌ 不替你做語意決策（該不該改，交 clarify）
- ❌ baseline 不明就停下來問，不用時間推估亂猜

| 疑問 | 回答 |
|---|---|
| 一定要先 commit 才能用嗎？ | 不用。working-tree 模式可掃未 commit 的改動，只是 who/when 會標成「操作者 + 掃描時間」 |
| 它會不會把我的規格改壞？ | 不會。它只寫 `.raptor/` 下的追蹤檔，對 SSoT 是唯讀 |
| 改動的「為什麼」一定要填嗎？ | 建議填（進 traceability）；可 skip，但該筆紀錄的可追溯性會降低 |
| 多人改怎麼辦？ | git author 記真實改動者，operator 記執行登錄的人，兩者分開 |
| 下游（API 文件、wireframe）過期了？ | human-sync 只**提示**哪些下游 stale，重產仍由 `/rapt-openapi`、`/rapt-lofi` 負責 |

> 講者備註：收尾用一句話定錨——human-sync 要做得少、但每筆紀錄都「可重跑、可追溯、可被 verify/reconcile 穩定消費」。它是海關，不是修復器。最後可帶到實作計畫文件 `0613plan-rapt-human-sync_cc-Opus48.md` 供想深入的人參考。

---
---

# 附錄：給簡報製作者的備註（不放進簡報）

1. **內容來源**：本稿的設計理念、SOP 步驟、不變式、git 命令全部取自 `ccwLog/0613plan-rapt-human-sync_cc-Opus48.md`（落地版實作計畫）與 `ccwLog/0613dis-SSoThumanModified.md`（原始討論）。與 antiOpus46 / codex 兩份計畫的差異（如 schema enum 對齊、不改 planner 取得 baseline、working-tree 優先）已在實作計畫中說明，簡報層級不展開。
2. **刻意不講的東西**：HSYNC YAML 完整 schema、fingerprint 去重的雜湊細節、`manage_impact_matrix.py` 的 CLI 參數、CJK/Windows 編碼處理、skill 多拷貝同步問題——這些是工程落地細節，培訓/介紹會場合不需要，留給實作計畫。
3. **視覺風格**：沿用 `gen_raptor_pptx.py` 的調色盤與版型（NAVY/TEAL/AMBER、Microsoft JhengHei、16:9），讓這 5 張能無縫插進《30 分鐘導覽》。footer 標題改為「RAPTor｜rapt-human-sync 設計導覽」。
4. **插入位置建議**：主簡報 Slide 20 講完「需求變更走 verify⇄reconcile 迴圈」後，正好承接「那如果是人**親手**改的呢？」→ 切入本段 5 張。
