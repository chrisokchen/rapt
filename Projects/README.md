# Projects 專案目錄

本目錄 (`Projects/`) 用於存放使用 **RAPTor** 規格體系與流程所建立的實際專案與示範案例。

## 📂 專案列表

- **[smallBiz](smallBiz/)**  
  基礎的小型企業範例專案，包含初步的 `raw-input` 與基本的 `.agents` 設定，用於測試與驗證初期的規格發掘流程。

- **[smallBiz-Fable](smallBiz-Fable/)**  
  進階的 `smallBiz` 專案分支，完整包含了 RAPTor 的專案結構（如 `.raptor/`, `docs/`, `.clarify/`），展示了如何從原始需求逐步發展成完整的規格文件與模型。初期使用 Fable 5，discovery 之後模型停用，之後改用 Opus 4.8。

- **[smallBiz-codex](smallBiz-codex/)**  
  另一個 `smallBiz` 的衍生分支，同樣包含完整的 `docs` 與 `.raptor` 結構，使用 Codex gpt-5.5。

## 🚀 如何在此目錄建立新專案

若要使用 RAPTor 建立新專案，請參考以下步驟：

1. **建立專案資料夾**：在 `Projects/` 目錄下建立一個新的資料夾（例如 `Projects/my-app`）。
2. **準備原始需求**：在新資料夾中建立 `raw-input` 目錄，並放入您的原始需求草稿、訪談記錄或初步的系統構想。
3. **連結 AI 技能庫**：為了能呼叫 `rapt-*` 技能，請在您的專案目錄內開啟終端機（Terminal）並建立 Junction 連結：
   ```powershell
   mkdir .agents
   cmd /c mklink /J .agents\skills ..\..\RAPTor\.agents\skills
   cmd /c mklink /J DSLspec ..\..\RAPTor\DSLspec
   ```
   *(註：若使用 Claude，建好後再把 .agents 目錄名稱改成 .claude)*
4. **初始化專案**：在您的專案目錄下啟動並呼叫 `rapt-kickoff` 技能（Agent），AI 會自動幫您生成 `.raptor/arguments.yml` 專案設定檔與標準目錄結構。
5. **展開探索之旅**：參考 [RAPTor Skills 使用手冊](RAPTor\.agents\skills\UserGuide.md)，依序使用 `rapt-discovery`、`rapt-modeling`、`rapt-intent` 等 AI 代理，將模糊的想法一步步提煉成結構化的 `DBML` 與 `haPDL`、`haAPI`、`haARM` 等可執行規格！

## CiC 整理 prompt

CiC（Critical Issue & Concern）是 RAPTor 規格體系中用於記錄與追蹤專案中關鍵議題、疑慮或待解決問題的工具。每個 CiC 都有唯一的編號、標題、類型（CON 或 GAP）、以及相關選項與影響 

請把目前所有 CiC 整理出來，包括它們的編號、標題、以及它們的類型（CON 或 GAP），以及有哪些選項、各選項造成的影響，並整理成表格。寫在 CWD 目錄下的 0716-Cic-01.md 檔案中。