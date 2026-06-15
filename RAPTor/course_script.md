# WA-RAPTor 新手村旅程：以終為始的規格驅動開發

- **時間**: 120 分鐘
- **目標**: 讓團隊成員理解 WA-RAPTor 的核心理念「Specification-as-Code」，並掌握從 haPDL 到最終程式碼的生成流程。
- **核心策略**: "Start with the End in Mind" (以終為始) - 先看結果，再探究原理。

---

## 課程大綱 (Agenda)

1.  **開場與動機 (Introduction)** - 5 mins
2.  **Module 1: 終局之戰 - PDL 與 HyVue3 (The Destination)** - 30 mins
    *   演示：從 PDL 生成現代化前端頁面
    *   解析：PDL 的角色與結構
3.  **Module 2: 源頭活水 - haPDL (The Source)** - 25 mins
    *   痛點：為什麼我們不直接寫 PDL？
    *   解法：haPDL (Human-centric / High-level)
4.  **Module 3: 七劍下天山 - 規格體系 (The Ecosystem)** - 30 mins
    *   全貌：從 DBML 到 Gherkin 的七種規格檔案
    *   案例：UserManage 的完整旅程
5.  **Module 4: 開發流程與 SSoT (The Process)** - 25 mins
    *   流程：從需求探索到自動化測試
    *   心法：Single Source of Truth
6.  **結語與 Q&A** - 5 mins

> [!NOTE]
> **延伸閱讀**：本課程聚焦於 WA-RAPTor 的「工具鏈」（haPDL → App）。若想深入了解如何從業務需求「思考」出高品質的 haPDL，請參閱 [需求發掘與分析流程](0_reqDevProcess/README.md)，其中涵蓋了 Event Storming、User Journey Mapping 等七階段方法論。

---

## 詳細腳本 (Script)

### 0. 開場與動機 (5 mins)

*   **開場白**: "大家好，今天我們要介紹的 WA-RAPTor 專案，不是一個單純的框架，而是一套『規格即程式碼』(Specification-as-Code) 的開發體系。我們通常習慣先寫 Code 再補文件，或者文件跟 Code 永遠對不上。今天我們要展示一種新的工作流：**寫好規格，程式碼就完成了 80%**。"
*   **破題**: "我們不從枯燥的理論開始，我們直接看結果。"
*   **[Tour Map](https://miro.com/app/board/uXjVJKs6u2M=/)**: "以防迷路"
---

### Module 1: 終局之戰 - PDL 與 HyVue3 (30 mins)

**目標**: 讓學員親眼看到「規格變程式碼」的魔術，建立對 PDL 的具體認知。

#### 1.1 演示：一鍵生成 (15 mins)
*   **情境**: "假設我們需要一個『預約列表』的功能。在傳統開發中，我們需要寫 HTML, CSS, JS, API 串接... 現在，我們只需要一個檔案。"
*   **操作演示**:
    1.  **展示 PDL**: 打開 [`PageDL/reservation-list.rui.yaml`](PageDL/reservation-list.rui.yaml) (或 [`haPDL/UserManage/6-PDL.yaml`](haPDL/UserManage/6-PDL.yaml)、更簡化的 [`haPDL/examples/urser-list.pdl.yaml](haPDL/examples/user-list.pdl.yaml))。
        *   *解說*: "這就是 PDL (Page Description Language)。它不是程式碼，它是**頁面的規格書**。大家可以看到 `type: list`, `columns`, `actions` 等關鍵字。"
    2.  **執行生成**:
        ```powershell
        # 假設在專案根目錄
        node Opus4.1/dsl-code-generator.ts --input PageDL/reservation-list.rui.yaml --target vue --out generated/reservation-list
        ```
        *   *強調*: "注意看，我執行了一個指令。它讀取了 YAML，然後產生了 Vue 的程式碼。"
    3.  **展示成果**:
        *   切換到 [`https://github.com/chrisokchen/sysAnA`](https://github.com/chrisokchen/sysAnA/blob/main/CLAUDE.md) (或本地跑起來的 HyVue 專案)。
        *   展示生成的列表頁：有表格、有分頁、有搜尋、有按鈕。
        *   *互動*: 點擊「編輯」，彈出表單；點擊「搜尋」，列表更新。
    4.  **Mock Data**: "大家可能會問，後端還沒好怎麼辦？Generator 同時產生了 Mock Data，所以前端完全可以獨立開發、展示。"

#### 1.2 解析：PDL 的結構 (15 mins)
*   **概念**: "PDL 是前端工程師與機器的合約。它描述了『頁面長什麼樣』(View) 以及『資料從哪來』(Data)。"
*   **代碼走讀** ([`PageDL/reservation-list.rui.yaml`](PageDL/reservation-list.rui.yaml)): [PDL 語法規格](PageDL/pdl-syntax.md) 
    *   `page.type`: 頁面類型 (List, Form, Dashboard...)
    *   `datasource`: API 端點定義
    *   `columns`: 表格欄位定義 (Label, Key, Type)
    *   `actions`: 互動行為 (Navigate, API Call)
*   **小結**: "PDL 很強大，它精確地描述了 UI。但是... 大家覺得寫這個 YAML 容易嗎？它有 80-100 行，還有很多括號和縮排。如果每個頁面都要手寫這個，其實也很累。"

---

### Module 2: 源頭活水 - haPDL (25 mins)

**目標**: 介紹 haPDL 如何解決 PDL 過於繁瑣的問題，並連結到業務需求。

#### 2.1 痛點與解法 (10 mins)
*   **提問**: "PDL 雖然比寫 Vue 快，但還是太『技術』了。業務分析師 (BA) 或 PM 寫得出來嗎？很難。"
*   **引入 haPDL**: "所以我們有了 haPDL (Human-centric / High-level PDL)。它是給人寫的，特別是給 BA/PM 寫的。"
*   **對比**:
    *   PDL: "我要一個表格，第一欄是 ID，寬度 50px；第二欄是 Name..." (Imperative/Detailed)
    *   haPDL: "我要一個管理 User 的列表頁，顯示 Name 和 Email。" (Declarative/Intent)

#### 2.2 實例演示 (15 mins)
*   **檔案**: 打開 [`haPDL/examples/user-list.hapdl.yaml`](haPDL/examples/user-list.hapdl.yaml) (極簡版，32 行) 或 [`haPDL/UserManage/4-haPDL.yaml`](haPDL/UserManage/4-haPDL.yaml) (完整版，689 行)。
*   **特點解說**:
    *   **極簡**: 
        *   "看，`user-list.hapdl.yaml` 只有 **32 行**，就定義了完整的列表頁！"
        *   對比：`haPDL/UserManage/4-haPDL.yaml` 有 689 行，但包含了 4 個完整頁面（列表、詳細、表單、儀表板）
    *   **符號魔法** (參考 `user-list.hapdl.yaml` 第 12-14, 19-22 行):
        *   `name~`: 模糊搜尋 (第 12 行)
        *   `email@`: Email 格式驗證 (第 13 行)
        *   `status=`: 精確匹配 → 下拉選單 (Enum) (第 14 行)
        *   `name!`: 重要欄位 (第 19 行)
        *   `status:badge`: 徽章顯示 (第 21 行)
        *   `created_at|date`: 日期格式化 (第 22 行)
    *   **自動推導** (對照 [`haPDL/UserManage/1-DBML.dbml`](haPDL/UserManage/1-DBML.dbml)):
        *   "為什麼 haPDL 可以這麼短？因為它會去查『字典』——也就是 DBML (資料庫定義)。"
        *   **印證 1**: DBML 第 13 行定義 `email varchar(255) [unique, not null]`，所以 haPDL 的 `email@` 自動加上唯一性驗證
        *   **印證 2**: DBML 第 14 行定義 `status enum('active', 'inactive', 'suspended')`，所以 haPDL 的 `status=` 自動變成下拉選單，選項來自 DBML
        *   **印證 3**: DBML 第 15 行定義 `createdAt timestamp`，所以 haPDL 的 `created_at|date` 知道要用日期格式化
    *   **[haPDL 語法規格](haPDL/haPDL-specification.md)**: 這些符號和規則都有詳細的說明在這份文件裡
*   **轉換演示**:
    *   "我們用工具把 haPDL 轉成 PDL。" (口頭說明或執行轉換腳本)
    *   "32 行的 `user-list.hapdl.yaml` 會轉成約 200+ 行的 PDL，包含完整的欄位定義、驗證規則、API 端點等。"
    *   對比展示:[`haPDL/examples/user-list.hapdl.yaml`](haPDL/examples/user-list.hapdl.yaml) (32 行) vs [`haPDL/examples/user-list.pdl.yaml`](haPDL/examples/user-list.pdl.yaml) (93 行)

* YAML 對非技術人員不友善（縮排敏感、語法錯誤難查）❌ Business Analyst、Product Owner 難以直接編輯規格
    - haPDL linter 提供即時語法檢查與提示，降低錯誤率✅
    - haPDL 語法高亮編輯器（VSCode extension）提升編輯體驗✅
    - haPDL Playground 提供視覺化編輯介面 ([Projectional Editor](https://github.com/dslmeinte/Building-User-Friendly-DSLs-code))，讓非技術人員也能輕鬆撰寫規格 --TODO--
    - [以 markdown 寫 haPDL 規格，結合說明文件與規格定義？](haPDL/9_以md寫haPDL的可行性.md)
    - AI 輔助生成✅
---

### Module 3: 七劍下天山 - 規格體系 (30 mins)

**目標**: 建立完整的規格檔案視圖，理解各檔案間的依賴關係。

#### 3.1 全貌圖 (5 mins)


```
                  ┌─────────────────────────┐
                  │ 2. 高階 Gherkin          │ (業務意圖 "Why & What")
                  │ (Phase 1.5 產出)         │
                  └───────────┬─────────────┘
                              │ Informs
                              ▼
┌─────────────────────────────────────────────────────────┐
│              1. DBML (資料模型)                         │ (Phase 2 產出)
│              Single Source of Truth                    │
└───────────┬─────────────────────────────┬───────────────┘
            │                             │
    Guides  ▼                     Guides  ▼
┌───────────────────┐         ┌───────────────────┐
│ 3. haAPI          │         │ 4. haPDL          │
│ (後端意圖)         │         │ (前端意圖)         │
│ Phase 4.1 產出    │         │ Phase 4.1 產出    │
└─────────┬─────────┘         └─────────┬─────────┘
          │ Generates                   │ Generates
          ▼                             ▼
┌─────────────────┐         ┌─────────────────────────────┐
│ 5. TypeSpec     │         │ 6. PDL  +  7. 低階 Gherkin  │
│ (API 技術規格)   │         │ (頁面規格) (驗證規格)        │
│ Phase 4.2 產出  │         │ Phase 4.2 產出             │
└─────────────────┘         └─────────────────────────────┘
```


*   **概念**: "WA-RAPTor 不只有 PDL。我們有一套完整的『七種武器』，對應軟體開發的不同層面。"
*   **目錄展示**: 打開 [`haPDL/UserManage/`](haPDL/UserManage/) 資料夾。
    *   "這裡有 1 到 7 號檔案，這就是一個 Feature 的完整生命週期。"

#### 3.2 逐一擊破 (25 mins)
*   **1-DBML.dbml (The Foundation)**:
    *   *內容*: 資料庫 Schema。
    *   *地位*: **Single Source of Truth (SSoT)**。所有的欄位型別、關聯，都以這裡為準。
    *   別的都往高階走，這裡想往下加些預設細節 (e.g., 代碼參照、預設頁面呈現、欄位權限...)。
*   **2-HighLevel-Gherkin.feature (The Why)**:
    *   *內容*: "Given/When/Then" 的業務故事。
    *   *對象*: 業務與客戶溝通的語言。
*   **3-haAPI.yaml (The Backend Intent)**:
    *   *內容*: 定義 API 的意圖 (e.g., `list-users`, `ban-user`)。
    *   *對象*: 後端架構設計。
    *   **[hyAPI 語法規格](haPDL/haAPI-specification.md)**
*   **4-haPDL.yaml (The Frontend Intent)**:
    *   *內容*: 我們剛剛看過的，定義頁面意圖。
    *   *對象*: 前端/UI 設計。
*   **5-TypeSpec.tsp (The API Contract)**:
    *   *內容*: **(自動生成)** 微軟開發的 API 定義語言，比 OpenAPI 更簡潔。
    *   *用途*: 生成後端 Controller 介面與前端 API Client。
*   **6-PDL.yaml (The UI Contract)**:
    *   *內容*: **(自動生成)** 我們一開始看的詳細頁面規格。
    *   *用途*: 生成 Vue/React 程式碼。
*   **7-LowLevel-Gherkin.feature (The Verification)**:
    *   *內容*: **(自動生成)** 詳細的 UI 測試步驟 (e.g., "點擊 ID 為 btn-submit 的按鈕")。
    *   *用途*: 自動化測試 (E2E Testing)。

---

### Module 4: 開發流程與 SSoT (25 mins)

**目標**: 串聯所有知識，說明實際工作流與核心價值。

#### 4.1 開發流程 (15 mins)

**前言：規格的誕生**
*   \"WA-RAPTor 讓我們可以『快速建造』，但在建造之前，我們要先搞清楚『建造什麼』。\"
*   \"在寫 haPDL 之前，我們有一套**需求發掘與分析流程**（詳見 [`0_reqDevProcess`](0_reqDevProcess/README.md) 目錄），涵蓋七個階段。今天只提重點：\"

**需求探索的三階段（The Upstream）**：
1.  **Phase 1: 業務探索 (Business Discovery)**
    *   透過 Event Storming、User Journey Mapping 與利害關係人訪談，理解「使用者真正要什麼」。
    *   產出：User Journey Maps、Event Storming 輸出、業務願景文件。

2.  **Phase 2: 領域建模 (Domain Modeling)**
    *   從 Event Storming 中萃取領域實體，建立 `1-DBML` (這是最重要的一步！)。
    *   定義通用語言詞彙表、限界上下文。
    *   產出：DBML、領域實體模型。

3.  **Phase 3: 需求澄清 (Requirements Clarification)**
    *   系統化掃描規格中的模糊點（例如：「訂單金額可以是零嗎？」）。
    *   結構化提問與回答，更新 DBML 與業務規則。
    *   產出：澄清問題清單與答案、更新後的 DBML。

**規格制定與生成（The WA-RAPTor Zone）**：

4.  **Phase 4: 規格制定 (Specification Formulation)**
    *   BA 寫 `2-HighLevel-Gherkin`（業務故事）。
    *   BA 寫 `4-haPDL`（我要什麼畫面）。
    *   SA 寫 `3-haAPI`（我要什麼 API）。

5.  **Phase 5-6: 驗證與生成 (Validation & Generation)**  — **The Magic**
    *   執行 Generator（自動驗證規格完整性）。
    *   `1-DBML` + `3-haAPI` → `5-TypeSpec` → Backend Code Stub。
    *   `1-DBML` + `4-haPDL` → `6-PDL` → Frontend Code (HyVue3)。
    *   `1-DBML` + `4-haPDL` → `7-LowLevel-Gherkin` → Test Scripts。

6.  **Phase 7: 迭代精煉 (Iterative Refinement)**
    *   工程師填空 (Fill in the blanks) — 補上 Generator 無法生成的客製邏輯。
    *   跑 CI/CD 自動測試 (`7-LowLevel-Gherkin`)。
    *   收集反饋，更新 haPDL/DBML，重新生成。

**「快」與「對」的平衡**
*   WA-RAPTor 讓開發變快（Phase 5-7），但**前三階段（Phase 1-3）決定我們是否在建造『對』的東西**。
*   \"我們不只是追求速度，我們追求『快速建造正確的產品』。\"

#### 4.2 核心價值 (10 mins)
*   **Specification-as-Code**: 規格不再是死文件，它是 **可執行規格** (會編譯成程式碼)。規格錯了，程式就會錯；程式對了，規格就是對的。
*   **Single Source of Truth (SSoT)**:
    *   資料的真理在 DBML。
    *   意圖的真理在 haPDL/haAPI。
    *   **不要手動改 PDL 或 TypeSpec！** 就像你不會手動改 `.o` 檔或 `.class` 檔一樣。要改就改源頭 (haPDL/DBML)，然後重新生成。

---

### 5. 結語與 Q&A (5 mins)

*   **總結**: "我們今天從 HyVue3 的畫面 (End)，一路回溯到 PDL，再到 haPDL，最後看到 DBML (Start)。這就是 WA-RAPTor 的力量：用結構化的規格，串起軟體開發的整條鏈路。"
*   **Call to Action**: "Discussions, Issues, PRs 都歡迎PO到 [WA-RAPTor GitHub Repo](https://github.com/chrisokchen/WA-RAPTor)

**延伸討論**：
*   [說好的 AI 呢？ 跟 SDD 有什麼關係？](AISE/SDDvsWA-RAPTor.md)

**延伸閱讀**：
*   [WA-RAPTor 影響分析：邁向極速開發的轉型](impact_analysis.md)
*   [WA-RAPTor 規格寫作指南：如何寫出「好」的規格？](spec_writing_guide.md)
*   [WA-RAPTor 流程對應圖：從業務需求到可執行程式碼](process_map.md)
*   [需求發掘與分析流程完整文件](0_reqDevProcess/README.md)
*   Ready for your next trip? [需求發掘與分析旅程：從混沌到秩序](requirements_discovery_course.md)

**延伸架構**：
*   [從專案 RAPTor 到企業 RAPTor：規格驅動的組織轉型藍圖](SPLE/enterprise_raptor.md)
*   [從專案 RAPTor 到組織 SPLE：軟體產品線工程在 WA-RAPTor 的應用](SPLE/raptor2sple.md)
