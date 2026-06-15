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

1. 在此目錄下建立新的資料夾（例如 `Projects/my-new-app`）。
2. 在新資料夾中放置 `raw-input`（原始需求文件）。
3. 使用 `rapt-kickoff` 等 AI Agent 進行初始化，生成 `.raptor/arguments.yml` 與基礎目錄結構。
4. 依循 RAPTor 的七階段流程，開始進行規格發掘與建模。
