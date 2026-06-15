# RAPTor (Requirements Analysis & Prototype Tools)

> **RAPTor** 是一套結合 BDD (Behavior-Driven Development) 與 AI 技術的「規格即程式碼」(Specification-as-Code) 開發體系與工具集。

## 🎯 核心理念

RAPTor 的核心目標是解決傳統軟體開發中「需求文件與程式碼脫節」的問題。透過建立「Single Source of Truth (SSoT)」的規格體系，結合 AI Agents 的自動化生成與驗證能力，實現：

- **以終為始 (Start with the End in Mind)**：寫好規格，自動生成原型、UI 與測試程式碼。
- **人類中心 (Human-centric)**：提供人類易讀易寫的高階規格語言 (如 haPDL、haAPI、High-Level Gherkin)，降低溝通門檻。
- **AIxBDD 共構**：將嚴謹的 BDD 流程與結構化語意，內化為 AI Agent 的操作規範與驗證機制。

## 📂 目錄結構

本目錄 (`RAPTor/`) 包含了整個 RAPTor 體系的核心流程指南、AI 技能庫 (Skills) 以及培訓教材：

- **[0_reqDevProcess/](0_reqDevProcess/)**  
  **需求發掘與分析流程 (Requirements Discovery & Analysis Process)**。包含了從業務探索 (Phase 1) 到迭代精煉 (Phase 7) 的完整七階段流程文件，指導人類團隊如何進行高質量的需求探索與規格撰寫。
  
- **[.agents/skills/](.agents/skills/)**  
  **RAPTor AI Skill Family**。這是一系列專為 RAPTor 流程打造的 AI 技能庫 (`rapt-*`)，涵蓋了從 Kickoff、需求發掘 (Discovery)、領域建模 (Modeling)、規格驗證 (Verify) 到各類 DSL 的生成與預覽 (Preview) 工作。

- **[course_script.md](course_script.md)**  
  **RAPTor 新手村旅程：以終為始的規格驅動開發**。引導團隊理解從高階意圖 (haPDL) 到最終程式碼 (HyVue3) 的生成魔法與七劍規格體系。

- **[requirements_discovery_course.md](requirements_discovery_course.md)**  
  **需求發掘與分析旅程：從混沌到秩序**。深入探討如何透過 Event Storming、User Journey 等方法論，萃取出高品質的領域模型與高階規格。

## ⚔️ 七劍下天山：規格體系 (The Seven Specifications)

RAPTor 建立了一套從「業務意圖」到「技術實作」的規格轉換鏈：

1. **DBML (資料模型)**：Single Source of Truth，定義核心實體與關聯 (Phase 2)。
2. **High-Level Gherkin**：描述業務意圖的行為規格 (Phase 1.5)。
3. **haAPI (後端意圖)**：宣告式的 API 意圖設計 (Phase 4.1)。
4. **haPDL (前端意圖)**：人類友好的頁面/UI 意圖描述 (Phase 4.1)。
5. **TypeSpec**：自動生成的後端 API 規格契約 (Phase 4.2)。
6. **PDL**：自動生成的前端頁面詳細規格 (Phase 4.2)。
7. **Low-Level Gherkin**：自動生成的 UI 測試驗證腳本 (Phase 4.2)。

## 🚀 工作流程 (Workflow)

RAPTor 建議的工作流是由「人類負責高階決策與意圖」交由「AI 負責驗證與生成低階實作」：

1. **Kickoff & Discovery**：初始化專案，建立願景與影響地圖 (`rapt-kickoff`, `rapt-discovery`)。
2. **Modeling**：產出 DBML 與權限模型 (`rapt-modeling`)。
3. **Clarify**：透過 AI 找出規格矛盾與模糊點 (`rapt-clarify`)。
4. **Intent & Verify**：撰寫 haPDL/haAPI 後，交由 AI 驗證規格一致性 (`rapt-verify`)，並產出可執行的原型。

> 詳細的 AI Agent 執行流程與目錄規範，請參閱：[.agents/skills/README.md](.agents/skills/README.md)

## 🌐 關聯目錄結構 (Workspace Directories)

除本目錄之外，根目錄 (`../`) 中還有以下重要目錄，構成了完整的開發環境：

- **[Projects/](../Projects/)**  
  **專案與示範案例**。用於存放使用 RAPTor 體系建立的實際專案（如 `smallBiz` 系列專案），展示從原始需求到可執行規格的轉化過程。

- **[ccwLog/](../ccwLog/)**  
  **工作日誌與備忘錄**。開發過程中的討論紀錄、AI 協作指令、以及各類設計筆記與臨時記錄。

