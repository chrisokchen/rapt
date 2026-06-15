# RAPTor (Requirements Analysis & Prototype Tools)

> **RAPTor** 是一套結合 BDD (Behavior-Driven Development) 與 AI 技術的「規格即程式碼」(Specification-as-Code) 開發體系與工具集。

## 🌐 專案目錄結構 (Workspace Directories)

本工作區包含了 RAPTor 核心工具、實作專案：

- **[RAPTor/](RAPTor/)**  
  **核心流程與工具庫**。包含了完整的七階段需求發掘流程指南 (`0_reqDevProcess/`)、AI 技能庫 (`.agents/skills/`) 以及相關的新手與進階培訓教材。

- **[Projects/](Projects/)**  
  **專案與示範案例**。用於存放使用 RAPTor 體系建立的實際專案（如 `smallBiz` 系列專案），展示從原始需求到可執行規格的轉化過程。

## 🚀 快速開始

若您是第一次接觸 RAPTor，建議按照以下順序探索：
1. 閱讀 **[RAPTor/README.md](RAPTor/README.md)** 了解核心理念與規格體系。
2. 查看 **[WA-RAPTor 新手村旅程：以終為始的規格驅動開發](RAPTor/course_script.md)** 體驗「以終為始」的開發旅程。
3. 閱讀 **[需求發掘與分析旅程：從混沌到秩序](RAPTor/requirements_discovery_course.md)** 了解需求探索流程。
4. 進入 **[Projects/](Projects/)** 查看實際專案的 `docs/ssot/` (Single Source of Truth) 與生成的規格。

## 🛠️ 試試自己的專案 (Try It Yourself)

準備好讓 AI 幫您梳理需求與生成規格了嗎？您可以透過以下簡單的步驟，在本地建立您的第一個 RAPTor 專案：

1. **建立專案資料夾**：在 `Projects/` 目錄下建立一個新的資料夾（例如 `Projects/my-app`）。
2. **準備原始需求**：在新資料夾中建立 `raw-input` 目錄，並放入您的原始需求草稿、訪談記錄或初步的系統構想。
3. **連結 AI 技能庫**：為了能呼叫 `rapt-*` 技能，請在您的專案目錄內開啟終端機（Terminal）並建立 Junction 連結：
   ```powershell
   mkdir .agents
   cmd /c mklink /J .agents\skills ..\..\RAPTor\.agents\skills
   ```
   *(註：若使用 Claude，結束後再把 .agents 目錄名稱改成 .claude)*
4. **初始化專案**：在您的專案目錄下啟動並呼叫 `rapt-kickoff` 技能（Agent），AI 會自動幫您生成 `.raptor/arguments.yml` 專案設定檔與標準目錄結構。
5. **展開探索之旅**：參考 [RAPTor Skills 使用手冊](RAPTor\.agents\skills\UserGuide.md)，依序使用 `rapt-discovery`、`rapt-modeling`、`rapt-intent` 等 AI 代理，將模糊的想法一步步提煉成結構化的 `DBML` 與 `haPDL`、`haAPI`、`haARM` 等可執行規格！

## 📚 研究成果與簡報 (Publications & Presentations)

如果您對 RAPTor 背後的理論基礎、設計思維或系統分析細節感興趣，歡迎參閱我們整理的文獻與導覽簡報：

- **學術論文 (TCSE 2026)**：AI 產力左移與 Spec-as-Source 工程框架：以四維意圖規格體系與多層驗證鏈收斂生成式 AI 之隨機性  [pdf](RAPTor/references/TCSE_2026_paper_14_v2.pdf) / [Markdown 閱讀版](RAPTor/references/2026TCSE.md)
  > 深入探討 RAPTor 規格體系如何結合 BDD 與 AI 技術的學術研究。
- **RAPTor 30 分鐘導覽簡報**：
  [PPTX](RAPTor/references/0612-RAPTor-30minSAguide_cc-Fable5.pptx) / [Markdown 講稿](RAPTor/references/0612-RAPTor簡報-30min導覽.md)
  > 快速了解 RAPTor 的核心架構、系統分析 (SA) 指南與實務展示。
- **rapt-human-sync 專題簡報**：
  [PPTX](RAPTor/references/0613plan-rapt-human-sync_presentation_cc-Opus48.pptx) / [Markdown 講稿](RAPTor/references/0613plan-rapt-human-sync_presentation_cc-Opus48.md)
  > 介紹 RAPTor 中如何妥善處理「人工修改 SSoT」的同步與影響分析機制。

## 🙏 致謝 (Acknowledgments)

本專案的 `rapt-*` AI 技能庫（Skills）設計與工作流程，部分參考並啟發自 [Waterball-Software-Academy/aixbdd](https://github.com/Waterball-Software-Academy/aixbdd) (AIxBDD Workflow) 專案。我們將其核心精神與 WA-RAPTor 專屬的需求發掘流程與 DSLs 體系進行了整合與發展。特此向水球軟體學院致謝。

詳細的授權與版權聲明請參閱專案根目錄下的 [NOTICE](NOTICE) 檔。
