# 從 RFP 到完整規格 — RAPTor 30 分鐘導覽（簡報初稿）

> 受眾：BA / PO / PM（沒用過 RAPTor）
> 形式：30 分鐘導覽，約 23 頁，每階段一張「階段卡」
> 貫穿案例：電商平台 RFP（素材取自 `0_reqDevProcess/05-範例-電商系統.md` 與 `.agents/skills/.tests/ecommerce-minimal`）
>
> 時間配置建議：
> | 段落 | 頁次 | 時間 |
> |---|---|---|
> | 開場與痛點 | 1–3 | 3 min |
> | 成品全貌與流程地圖 | 4–7 | 6 min |
> | 兩個安全機制 | 8–9 | 4 min |
> | 九張階段卡走讀 | 10–18 | 12 min |
> | RAscore 與迭代 | 19–20 | 3 min |
> | 上手與 Q&A | 21–23 | 2 min |

---

## Slide 1 — 封面

**從一份 RFP，到一整套可驗證的規格**
RAPTor：AI 協作的需求分析流程

副標：你提供領域知識，AI 負責結構化、一致性與苦工

> 講者備註：開場一句話定調——RAPTor 不是「AI 幫你寫文件」，而是「一條有品質閘門的需求生產線，人負責決策、AI 負責生產與驗證」。

---

## Slide 2 — 我們都遇過的需求災難

- RFP 一百頁，真正的需求散落在第 37 頁的一句話裡
- 規格寫完三個月後，沒人知道「會員等級」在三份文件裡的定義是否一致
- 開發問「庫存不足時訂單怎麼辦？」——當初沒人問過客戶
- 需求改了一條，沒人說得出影響哪些 API、哪些頁面

> 講者備註：用提問互動：「在座誰的專案規格只有一份 Word？改版時誰負責同步？」

---

## Slide 3 — RAPTor 的三個回答

| 災難 | RAPTor 的回答 |
|---|---|
| 定義不一致、文件互相打架 | **SSoT**：五份規格是唯一事實來源，下游全部自動生成 |
| 該問的沒問、AI 又自作主張 | **CiC 便條 + Clarify**：AI 遇到模糊處不擅自決定，留便條請人定奪 |
| 改一條不知道影響什麼 | **可追溯矩陣 + 影響矩陣**：從 RFP 到 API/頁面的雙向追溯 |

> 講者備註：這三點就是全場主軸，後面每一頁都在展開這三件事。

---

## Slide 4 — 先看成品：跑完一輪你會得到什麼

```
docs/
├── discovery/                ← Phase 1：業務探索摘要
│   ├── 00-source-inventory.md   （RFP/會議記錄盤點）
│   ├── 01-stakeholders.md       （利害關係人）
│   ├── 02-user-journeys.md      （使用者旅程）
│   ├── 03-event-timeline.md     （業務事件時間線）
│   └── 04-vision-kpi-scope.md   （願景/KPI/範圍）
├── ssot/                     ← 五份規格 SSoT（唯一事實來源）
│   ├── habdd/   *.feature        （高階 Gherkin：行為規則）
│   ├── dbml/    schema.dbml + glossary/seeds/constraints（資料模型）
│   ├── haarm/   *.haarm.yaml     （角色與權限）
│   ├── haapi/   *.haapi.yaml     （API 意圖）
│   └── hapdl/   *.hapdl.yaml     （頁面意圖）
├── generate/                 ← 下游生成物（隨時可重生）
│   ├── openapi/  （Swagger 可瀏覽的 API 文件）
│   ├── lofi/     （可開啟的 Lo-Fi wireframe HTML）
│   └── designbrief/ （餵給 AI 設計工具的 Design Brief）
├── reports/                  ← 驗證報告 + RAscore 品質計分卡
.clarify/                     ← 澄清問題 backlog 與決策記錄
.raptor/                      ← session 狀態、可追溯矩陣、影響矩陣
```

> 講者備註：先給終點再講路徑。強調兩層：`ssot/` 是人簽核的資產，`generate/` 是隨時可丟掉重生的投影。

---

## Slide 5 — 五份規格，各回答一個問題

| 規格 | 回答的問題 | 給誰看 |
|---|---|---|
| 高階 Gherkin（habdd） | 系統在什麼規則下**做什麼**？ | 客戶、領域專家都讀得懂（純業務語言，禁止出現按鈕/URL） |
| DBML | 資料**長什麼樣**？值域、狀態、約束是什麼？ | BA + 開發 |
| haARM | **誰**可以做什麼？ | BA + 資安 + 開發 |
| haAPI | 後端要**提供什麼能力**？ | 開發 |
| haPDL | 畫面要**呈現什麼、怎麼互動**？ | UX + 開發 |

五份互相引用、互相檢查——這就是後面「驗證」階段在驗的東西。

> 講者備註：這頁是術語防火牆。之後出現 habdd/haARM 等縮寫，聽眾已有掛勾。不要在這頁展開語法。

---

## Slide 6 — 整條生產線：九個指令

```
/rapt-kickoff      初始化（一次性）
      ↓
/rapt-discovery    Phase 1   業務探索：消化 RFP
      ↓
/rapt-behavior     Phase 1.5 高階 Gherkin：行為規則
      ↓
/rapt-modeling     Phase 2   領域建模：DBML + haARM
      ↓                          ↓ 模糊處留 CiC 便條
/rapt-clarify      Phase 3   澄清：人來定奪 ←──────┐
      ↓                                            │
/rapt-intent       Phase 4   意圖規格：haAPI + haPDL│
      ↓                                            │
/rapt-verify       Phase 5   驗證（只讀，出報告）    │
      ↓                                            │
/rapt-reconcile    Phase 6   調和修復 ──語意性問題──┘
      ↓（驗證通過後）
/rapt-openapi  /rapt-lofi  /rapt-design-brief   預覽生成
（隨時可跑：/rapt-RAscore 品質計分卡）
```

**不是瀑布**：verify → reconcile → clarify 是一個迴圈，跑到驗證全綠為止。

> 講者備註：強調每個 phase 有「品質閘門」，沒過就不建議往下走；session.md 隨時記錄你走到哪。

---

## Slide 7 — 人機分工：誰做什麼

| | AI（RAPTor skills） | BA / PO / PM | 領域專家 |
|---|---|---|---|
| 探索 | 讀完所有材料、結構化摘要 | 備齊 RFP/會議記錄、補商業脈絡 | 驗證角色與旅程沒漏 |
| 規格 | 起草 Gherkin / DBML / 權限模型 | 審 Feature 是否對應目標 | 驗證規則、值域、狀態 |
| 澄清 | 掃出模糊點、打包成**選擇題** | 主持 session、記錄取捨 | **回答問題（主場）** |
| 驗證 | 跨文件一致性、覆蓋率、自動修復 | 評估 WARN 是否接受 | — |
| 預覽 | 生成 Swagger / wireframe | 拿去和客戶確認 | 看 wireframe 挑錯 |

**專家的時間花在刀口上**：不寫文件，只回答排好優先級的選擇題、驗證關鍵產出。

> 講者備註：這頁回應 PM 最大的疑慮——導入後專家負擔是降低不是增加。

---

## Slide 8 — 安全機制 1：AI 不確定時，留便條而不是猜

**CiC 便條（Clarification-in-Context）**，四種型態：

- `GAP` 缺口：RFP 沒講（「退貨期限是幾天？」）
- `ASM` 假設：AI 暫時假設，待確認（「假設一個客戶一台購物車」）
- `BDY` 邊界：邊界條件未定（「金額剛好為 0 算不算有效訂單？」）
- `CON` 衝突：兩份來源互相矛盾（「RFP 說 7 天、會議記錄說 14 天」）

便條直接嵌在規格旁邊，`/rapt-clarify` 統一收割成問題集。

**澄清問題長這樣（真實格式）**：

> **Q：商品庫存不足時，建立訂單應如何處理？**（優先級：High）
> A. 完全拒絕，顯示錯誤　B. 允許建立，標記待補貨
> C. 部分成立　D. 允許超賣，後續通知
> 影響範圍：建立訂單 Feature、庫存檢查、訂單狀態定義

> 講者備註：這是 RAPTor 與「直接叫 ChatGPT 寫規格」最大的差異——模糊處不會被一個看似合理的幻覺蓋掉。決策有 decision log，半年後還查得到「為什麼當初選 A」。

---

## Slide 9 — 安全機制 2：每個 skill 只能寫自己的地盤

**Artifact Output Contract（deny-by-default）**

- 探索階段的 skill **碰不到**規格檔；驗證階段的 skill **只能讀、只能出報告**
- 修復（reconcile）只准動「機械性問題」（改名、補引用），動手前先建 snapshot
- **語意性問題一律不准自己改**——退回 clarify 請人決定
- 所有路徑由 `.raptor/arguments.yml` 統一管理，skill 不能自創目錄

> 講者備註：回答「AI 會不會亂改我的文件」。每張階段卡的產出物範圍都是白紙黑字的合約，超出範圍直接 DENY。

---

## Slide 10 — 階段卡 0：初始化 `/rapt-kickoff`

| | |
|---|---|
| **時機** | 專案開始，repo 第一次跑 RAPTor（一次性） |
| **目標** | 建立路徑設定與進度追蹤的基礎 |
| **你提供** | 專案名稱、一句話描述、語言、模式、文件根目錄（5 個問題，2 分鐘） |
| **產出** | `.raptor/arguments.yml`（路徑 SSoT）、`KICKOFF_PLAN.md`、`session.md`（phase 進度表） |
| **BA/PO 要理解** | 之後所有產出位置都由這份設定決定；`session.md` 是隨時可看的進度儀表板 |

> 講者備註：快速帶過，重點只有一個：跑一次，之後不用管。

---

## Slide 11 — 階段卡 1：業務探索 `/rapt-discovery`

| | |
|---|---|
| **時機** | 收到 RFP / 標書 / 會議記錄之後 |
| **目標** | 把散落的原始材料消化成結構化的業務圖像 |
| **你提供** | 所有拿得到的材料：RFP、訪談記錄、現有系統文件、競品分析 |
| **產出** | 來源盤點、**利害關係人清單**、**使用者旅程**、**事件時間線**、**Vision/KPI/範圍邊界** |
| **BA/PO 驗證** | 範圍邊界（in/out of scope）是否與商業判斷一致；KPI 是否可衡量 |
| **專家驗證** | 角色有沒有漏（隱性角色：客服、稽核）；旅程是否符合實際作業 |
| **閘門** | ≥2 個角色、有 vision、≥2 個 KPI、範圍邊界明確——缺的直接記成 GAP 便條 |

案例片段：電商 RFP 進來，AI 從附錄挖出「加盟主」這個正文沒提的角色。

> 講者備註：強調「材料給越齊，後面的澄清問題越少」。閘門沒過不會硬往下走。

---

## Slide 12 — 階段卡 1.5：行為規則 `/rapt-behavior`

| | |
|---|---|
| **時機** | 探索閘門通過後 |
| **目標** | 把使用者故事寫成**業務語言**的高階 Gherkin——這是第一份 SSoT |
| **輸入** | Phase 1 全部產出（自動讀取） |
| **產出** | `*.feature` 檔、story-index 索引、可追溯矩陣 L1/L2 草稿 |
| **BA/PO 驗證** | 每個 Feature 都能對回某個旅程階段或痛點；沒有憑空多出來的功能 |
| **專家驗證** | 規則對不對、Example 的數字是否符合實務、邊界案例有沒有漏 |
| **閘門** | 禁技術語彙（按鈕/URL/HTTP）；每個 Feature 有來源證據；Then 不准寫「阻擋**或**警示」這種未決定的替代策略 |

案例片段：
```gherkin
Rule: 訂單商品數量不可超過庫存
  Example: 剛好等於庫存數量應成功
    Given 商品 "iPhone 15" 庫存為 10
    When 客戶訂購 10 件
    Then 應成功建立訂單，庫存變為 0
```

> 講者備註：兩個重點：(1) 客戶看得懂、可以直接拿去簽核；(2)「Then 不准有替代策略」就是強迫在規格期把決策做掉，而不是留給工程師猜。

---

## Slide 13 — 階段卡 2：領域建模 `/rapt-modeling`

| | |
|---|---|
| **時機** | 高階 Gherkin 就緒後 |
| **目標** | 建立資料模型與權限模型兩份 SSoT |
| **輸入** | Gherkin + discovery 產出（自動讀取） |
| **產出** | annotated DBML、**詞彙表 glossary**、**值域 seeds**、**約束 constraints**、haARM 權限模型 |
| **BA/PO 驗證** | 詞彙表——同一個概念全專案只有一個名字（「會員」vs「客戶」二選一） |
| **專家驗證** | 狀態機（訂單有哪些狀態、怎麼轉）、值域（幣別？稅別？）、誰有權做什麼 |
| **閘門** | 每個代碼欄位有值域或 OPEN 便條；高風險狀態/刪除限制有明確約束；權限角色涵蓋所有利害關係人 |

**關鍵行為**：值域、約束查不到時，AI 不編造——記 CiC 便條等下一階段問你。

> 講者備註：這是便條產量最大的階段，剛好示範「AI 起草 + 人定奪」的節奏。

---

## Slide 14 — 階段卡 3：澄清 `/rapt-clarify` ★ 專家主場

| | |
|---|---|
| **時機** | 建模完成後（或任何時候便條累積夠多） |
| **目標** | 清空所有模糊點，把決策正式寫回規格 |
| **流程** | 掃描全部便條 → 打包成**有優先級的選擇題** → 澄清 session → 決策套用回 SSoT |
| **BA/PO 要做** | 主持 session、安排專家、對商業取捨類問題拍板 |
| **專家要做** | 回答問題——High 優先必答，答案多半是 A/B/C/D 一個字母 |
| **產出** | 決策記錄（decision log）、更新後的 SSoT、便條標記 RESOLVED |
| **閘門** | 無 OPEN 的缺口與衝突；所有假設被確認或否決；暫緩項目有明確狀態（MVP 外 / 待決策 / 接受風險） |

> 講者備註：三個賣點講滿：(1) 問題已排好優先級，專家一場 session 集中解決；(2) 每個答案直接改寫規格，不會開完會沒下文；(3) decision log 讓「當初為什麼這樣決定」永遠可查。

---

## Slide 15 — 階段卡 4：意圖規格 `/rapt-intent`

| | |
|---|---|
| **時機** | 澄清閘門通過後（規格的模糊點已清空） |
| **目標** | 從三份上游 SSoT 切出 API 意圖（haAPI）與頁面意圖（haPDL） |
| **輸入** | DBML + haARM + Gherkin（自動讀取，只讀不改） |
| **產出** | `*.haapi.yaml`、`*.hapdl.yaml`、可追溯矩陣補到 Scenario 層級 |
| **BA/PO 驗證** | 頁面意圖是否走得完使用者旅程；每個 Scenario 都有承接的 API/頁面 |
| **專家** | 此階段幾乎不需出席——素材在前四個階段已備齊 |
| **閘門** | 每個主要資料表有對應 API；每個 API 至少有 list + form 頁面；追溯矩陣完整 |

**「意圖」不是實作**：haAPI 說「需要能查詢訂單、依狀態篩選」，不寫 URL 與 JSON 格式——那些是下游自動生成的事。

> 講者備註：點出前期投資在這裡回收：上游夠乾淨，這一步幾乎全自動。

---

## Slide 16 — 階段卡 5：驗證 `/rapt-verify`

| | |
|---|---|
| **時機** | 五份 SSoT 到齊後；之後每次修改都可重跑 |
| **目標** | 像 CI 一樣檢查整套規格 |
| **四項檢查** | **完整性**（檔案齊不齊）、**跨文件一致性**（haPDL 引用的 API 存在嗎？權限對得上嗎？）、**可追溯性**（每個 Scenario 有承接嗎？）、**覆蓋率**（must-have 100%？） |
| **產出** | 驗證報告（人讀的 md + 機器讀的 yml），每個 finding 標好：可自動修 / 需要人決定 / 僅備註 |
| **BA/PO 要做** | 看報告首頁的 PASS / PARTIAL / FAIL；決定 WARN 項目「接受」或「要修」 |
| **重要** | 此 skill **只讀不改**——裁判不下場踢球 |

案例片段：「FAIL：3 個 Scenario 無對應 haAPI；覆蓋率 78%（must-have 100%）」

> 講者備註：類比 CI/CD 給 PM 聽：規格也有自動化測試，改完重跑、綠了才出貨。

---

## Slide 17 — 階段卡 6：調和修復 `/rapt-reconcile`

| | |
|---|---|
| **時機** | 驗證報告有 FAIL / WARN 時 |
| **目標** | 把問題分流：機械性自動修，語意性退給人 |
| **機械性（AI 直接修）** | 命名不一致、引用斷鏈、追溯矩陣缺漏——修之前先建 snapshot，可回滾 |
| **語意性（人來決定）** | 「這個 Scenario 沒有 API 承接，是要補 API 還是砍 Scenario？」→ 打包回 clarify |
| **產出** | 修復 session 記錄、**影響矩陣更新**（這次修復波及哪些下游） |
| **BA/PO 要理解** | 修完回去重跑 `/rapt-verify`，verify ⇄ reconcile 迴圈跑到全綠 |

> 講者備註：強調分流邏輯就是第 9 頁合約的落實——AI 永遠不替你做語意決策。

---

## Slide 18 — 階段卡 7：預覽生成（給客戶看得懂的東西）

| 指令 | 產出 | 用途 |
|---|---|---|
| `/rapt-openapi` | OpenAPI 3.0 YAML | Swagger UI 直接瀏覽，開發團隊/外包對接 |
| `/rapt-lofi` | 自包含 wireframe HTML | **寄給客戶用瀏覽器打開**，走一遍流程挑錯 |
| `/rapt-design-brief` | 結構化 Design Brief | 餵 AI 設計工具直接出 Hi-Fi 設計稿 |

- 全部放在 `docs/generate/`，**隨時可刪掉重生**——因為源頭是 SSoT
- 客戶看了 wireframe 說「這裡不對」→ 改的是 SSoT，再重新生成，永遠不會出現「設計稿和規格不同步」

> 講者備註：這是對 PO 最有感的一頁：規格期就有可以拿給客戶確認的東西，而且回饋有明確的回流路徑（下一頁）。

---

## Slide 19 — 品質計分卡 `/rapt-RAscore`

- 隨時可跑、**advisory-only**（建議性質，不擋流程）
- 以 rubric 對整套 Gherkin + DBML 逐準則評分 → 總分 / 等級 / veto 警示
- findings 自動分流：可修的進 reconcile、要問的進 clarify
- 用途：
  - 對內：規格「夠不夠格當 SSoT」的客觀依據
  - 對外：附在交付物上的品質證明
  - 跨專案：不同案子的需求品質可以比較

> 講者備註：PM 視角——這是可以放進管理報告的數字。

---

## Slide 20 — 需求變更時：迴圈，不是重做

```
客戶回饋 / 需求變更
   ↓
影響矩陣查波及範圍（.raptor/impact-matrix.yml）
   ↓
改對應的 SSoT（必要時走一輪 clarify）
   ↓
/rapt-verify 重跑 → 有問題 → /rapt-reconcile → 再 verify
   ↓ 全綠
重新生成 openapi / lofi / design-brief
```

- 改的永遠是 SSoT，下游全部重生——**不存在「忘了同步」**
- decision log + traceability：每條規格查得到「從哪來、為什麼、影響誰」

> 講者備註：收束第 3 頁的三個承諾，首尾呼應。

---

## Slide 21 — 上手：你的第一個專案

```
1. 把 RFP、會議記錄丟進專案資料夾
2. /rapt-kickoff       （2 分鐘，回答 5 個問題）
3. /rapt-discovery     （產出探索摘要 → 找專家確認角色與範圍）
4. /rapt-behavior      （高階 Gherkin → 拿去給客戶/專家審）
5. /rapt-modeling      （資料 + 權限模型，便條開始累積）
6. /rapt-clarify       （★ 排一場 1-2 小時的澄清 session）
7. /rapt-intent → /rapt-verify ⇄ /rapt-reconcile（跑到全綠）
8. /rapt-lofi          （寄 wireframe 給客戶）
9. /rapt-RAscore       （附上品質計分卡，交付）
```

人的關鍵投入只有三處：**備材料（1）、審 Gherkin（4）、澄清 session（6）**。

---

## Slide 22 — 常見疑問

| 疑問 | 回答 |
|---|---|
| AI 會不會亂改文件？ | 每個 skill 有白紙黑字的輸出合約（deny-by-default）；修復前自動 snapshot；語意決策一律退回人 |
| 專家要花多少時間？ | 集中在澄清 session 與關鍵驗證點；問題是排好優先級的選擇題 |
| 中途可以停嗎？ | `session.md` 記錄每個 phase 狀態，隨時中斷、隨時續跑 |
| 既有專案能用嗎？ | 可以——把現有文件當 discovery 材料匯入，照樣往下走 |
| 規格改了下游怎麼辦？ | 下游全是生成物，重新生成即可；影響矩陣先告訴你波及範圍 |

---

## Slide 23 — 結尾

**RAPTor = 一條有品質閘門的需求生產線**

- AI 做苦工：消化材料、起草五份規格、交叉驗證、自動修復
- 人做決策：商業取捨、領域知識、簽核閘門
- 產出可證明：可追溯、可評分、可重生

下一步：拿你手上的一份 RFP，跑 `/rapt-kickoff` 試一輪。

---
---

# 附錄：給簡報製作者的備註（不放進簡報）

1. **以 skill 實際流程為準**：本稿的階段編號、產出路徑、閘門條件全部取自 `.agents/skills/*/SKILL.md` 與 `rapt-core/references/phase-gates.md`，與 `0_reqDevProcess/01-整體流程架構.md` 的七階段有差異（該文件 Phase 4 才寫 BDD、用 TypeSpec、Phase 6 是原型生成）。若聽眾會對照舊文件，可在 Q&A 備一頁對照表。
2. **刻意不講的東西**：planner/worker/DELEGATE 機制（只在 Slide 9 以「合約」帶過）、rapt-form-* 五個 worker、rapt-clarify-loop、rapt-core、v3.3 DSL 語法細節、arguments schema。BA/PO/PM 場合都不需要。
3. **案例片段待補**：Slide 11/12/16 的案例片段建議從 `.agents/skills/.tests/ecommerce-minimal` 與 `rapt-RAscore/.tests/minimal-gherkin-dbml` 抓真實檔案截圖，比文字框更有說服力。
4. **Slide 8 的問題卡**：格式取自 `0_reqDevProcess/01-整體流程架構.md` 的澄清問題範例，與 `rapt-clarify-loop/references/question-format.md` 的實際格式做過比對後可再校準。
5. **Phase 6 命名**：phase-gates.md 中 Phase 6 標為 Prototype（Wave 7 延後實作），skill 流程中 `/rapt-reconcile` 佔 Phase 6 位置；簡報迴避編號爭議，階段卡用「調和修復」與「預覽生成」兩張卡呈現。
