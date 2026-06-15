# rapt 說明文件

# > 為 RAPTor 目錄，寫個完整的 README.md

我已經為 RAPTor 目錄建立了一份完整的 README.md。
這份文件整合了 RAPTor 目錄內現有的資源（包含 AI 技能庫、需求探索流程、以及相關的培訓課程內容），為整個目錄提供了一個清晰的入口與全貌總覽。

📄 新增的檔案：/d:/0WK/rapt/RAPTor/README.md

### 文件涵蓋的重點內容：

1. 核心理念：闡述「規格即程式碼」(Specification-as-Code)、Single Source of Truth (SSoT) 以及 AI 輔助 BDD 的核心精神。
2. 目錄結構導覽：介紹目錄下的 .agents/skills（AI 技能庫）、0_reqDevProcess（需求發掘流程）以及相關的新手/進階教材 (course_script.md, requirements_discovery_course.md)。
3. 七劍規格體系：明確列出從業務意圖（DBML, High-Level Gherkin, haAPI, haPDL）到技術實作（TypeSpec, PDL, Low-Level Gherkin）的規格轉換階層。
4. 工作流程：概述從 Kickoff、Modeling、Clarify 到 Verify 的 AIxBDD 協作流程。

# > 為 Projects 目錄，寫個完整的 README.md


# > 我的 rapt-* skill 是參考 https://github.com/Waterball-Software-Academy/aixbdd 的做法，再配合自訂的 Requirement Development 流程與 RAPTor DSLs 體系發展的。在 repo 的 LICENSE 檔 與 NOTICE 檔裡，要如何清楚的註明參考出處呢 (參見水球的 LICENSE_waterBall 與 NOTICE-_waterBall)？

在 Apache 2.0 的開源授權規範中，若您的專案參考或衍生自同樣為 Apache 2.0 授權的專案（如水球的 AIxBDD Workflow），標準的做法是將歸屬聲明集中在 NOTICE 檔中，而 LICENSE 檔則保持一份標準條款即可。

我已經自動幫您將參考資訊正確地合併到了專案根目錄的 NOTICE 檔中。

具體的做法與規範說明：
關於 LICENSE 檔：

因為兩個專案皆採用 Apache 2.0，授權條款本身是一模一樣的，所以專案根目錄只需要保留您現有的那一份 LICENSE 檔即可。不需要另外保留 LICENSE_waterBall。
關於 NOTICE 檔：

根據 Apache 2.0 第 4(d) 節的規定：若衍生專案包含 NOTICE 檔，則必須在其中包含原始專案的 NOTICE 內容（即版權聲明與致謝）。
我已經將您的 NOTICE 檔更新為以下標準格式，明確註明了您參考了水球的設計：
text
rapt - Requirement Analysis and Prototype Tools
Copyright 2026 - Chris Chen
This product includes software developed or derived from the AIxBDD Workflow project
(https://github.com/Waterball-Software-Academy/aixbdd).
=========================================================================
Portions of this software (specifically the `rapt-*` skills and workflow concepts)
were adapted from or inspired by the AIxBDD Workflow:
AIxBDD Workflow
Copyright 2026 - 水球球特務有限公司 (Waterball Agent Limited)
=========================================================================
建議的下一步：
既然已經將歸屬聲明正確整併到了正式的 NOTICE 檔中，為了保持專案根目錄的整潔，您可以直接將原本參考用的 LICENSE_waterBall 與 NOTICE-_waterBall 檔案刪除。這樣既符合開源規範，也能清楚交代出處！

# > 我希望在 README.md 裡也提到這段

我已經將這段致謝資訊加入到專案根目錄的 README.md 的最下方。

現在 README.md 包含了一個 「🙏 致謝 (Acknowledgments)」 區塊，明確感謝並附上了 AIxBDD Workflow 專案的連結，同時指引讀者查閱 NOTICE 檔了解詳細的版權聲明細節。

您可以點擊 /d:/0WK/rapt/README.md 查看更新後的內容！如果有其他需要調整或補充的地方，請隨時告訴我。

# > 幫忙寫 README.md 裡的 ## 試試自己的專案 的內容 (標題也要有 emoji 圖示 :-)
我已經幫您補上了 「🛠️ 試試自己的專案 (Try It Yourself)」 這個區塊！

裡面的內容包含了一個帶有 emoji 的標題，以及引導使用者在本地端建立新專案的 4 個簡單步驟（建立資料夾、準備原始需求、呼叫 rapt-kickoff 初始化、再接著呼叫後續的代理進行探索）。

您可以前往 /d:/0WK/rapt/README.md 查看這段新加入的內容。如果有需要微調語氣或補充其他細節，請隨時告訴我！

# 2 跟 3 之間要有在將 RAPTor\.agents\skills 建立成自己目錄下 Junction 的步驟，否則沒有 rapt-* skills 可呼叫。可參考 sync-skills.ps1 是從整個 repo 角度為 Projects 裡各專案建，可以有個從專案角度為 Project建 junction 的做法嗎?

我已經將「建立 Junction 連結」的重要步驟補充到教學指南中了！

現在，不僅是根目錄的 README.md，連同 Projects\README.md 的教學步驟也都同步更新了。新的步驟被安插在「準備原始需求」與「初始化專案」之間：

1. 教導使用者在自己的專案目錄下開啟終端機。
2. 建立 .agents 資料夾。
3. 執行 cmd /c mklink /J .agents\skills ..\..\RAPTor\.agents\skills 指令建立 Junction。
4. （同時也備註了若要批次管理，依然可以透過根目錄的 sync-skills.ps1 來執行）。

您可以點擊查看更新後的檔案：
 * /d:/0WK/rapt/README.md
 * /d:/0WK/rapt/Projects/README.md
這樣使用者從單一專案的角度出發時，就能很順暢地把技能庫掛載進來並開始使用 rapt-* 指令了！


# > 我有一份相關的論文 (ccwLog\TCSE_2026_paper_14_v2.pdf, md版 ccwLog\0609-TCSE.md)，以及兩份 rapt skills set 的簡報 (都在 ccwLog 目錄下)，要怎麼在 README.md 提及？合適嗎?

將相關文獻與簡報放在 README.md 中是非常合適且強烈建議的！這不僅能幫助使用者更深入了解 RAPTor 背後的設計哲學，還能提升專案的學術與工程信譽。

我已經為您在 README.md 中新增了 「📚 研究成果與簡報 (Publications & Presentations)」 區塊，並將它放置在「展開探索之旅」與「致謝」之間。

在這個新區塊中，我列出了：

1. 學術論文 (TCSE 2026)：同時附上 PDF 與 Markdown 版本的連結。
2. RAPTor 30 分鐘導覽簡報：附上 PPTX 下載與 Markdown 講稿的連結，方便快速了解 SA 指南。
3. rapt-human-sync 專題簡報：附上關於人工修改 SSoT 同步機制的專題簡報與講稿連結。

您可以前往 /d:/0WK/rapt/README.md 查看更新後的排版。

(小提醒：目前的連結指向 ccwLog 目錄，這在專案內部參考是沒問題的。未來如果專案要對外公開，或許可以考慮建一個 docs/papers/ 或 docs/presentations/ 將這些重要產出集中管理，看起來會更加正式哦！)

---

| codex gpt-5.5 :-

• 合適，但建議用「背景資料 / 研究成果 / 簡報」的定位，不要把它寫成正式規格文件。你目前 README 已經有一段方向正確的區塊：

  ## 📚 研究成果與簡報 (Publications & Presentations)

  這樣放在 README 裡是合理的，因為這些資料可以幫讀者理解 RAPTor 的理論背景、設計脈絡與 skills set 的使用方式。

  我會建議稍微注意一點：ccwLog/README.md 目前把 ccwLog 定義成「工作日誌、臨時設計筆記」。如果根 README 直接連到 ccwLog
  裡的論文與簡報，語意上會有一點衝突。比較乾淨的做法有兩種：

  1. 短期做法：保留在 ccwLog，README 明確標成參考資料
     適合目前還在整理階段。

  2. 較正式做法：把論文與簡報移到 docs/publications/ 或 docs/references/
     ccwLog 保留工作紀錄，正式對外文件放在 docs/，README 連到 docs/。

  我建議 README 可以這樣寫：

  ## 📚 研究成果與簡報 (Publications & Presentations)

  以下資料提供 RAPTor 的理論背景、設計脈絡與 skills set 使用導覽，適合想進一步理解方法論與實作流程的讀者參考。

  - **學術論文：TCSE 2026**
    [PDF](ccwLog/TCSE_2026_paper_14_v2.pdf) / [Markdown 閱讀版](ccwLog/0609-TCSE.md)

    說明 RAPTor 如何結合 BDD、AI 輔助需求分析與 Specification-as-Code 的開發流程。

  - **RAPTor 30 分鐘導覽簡報**
    [PPTX](ccwLog/0612-RAPTor-30minSAguide_cc-Fable5.pptx) / [Markdown 講稿](ccwLog/0612-RAPTor簡報-30min導覽.md)

    快速介紹 RAPTor 的核心架構、skills set 與系統分析流程。

  - **rapt-human-sync 專題簡報**
    [PPTX](ccwLog/0613plan-rapt-human-sync_presentation_cc-Opus48.pptx) / [Markdown 講稿](ccwLog/0613plan-rapt-human-
    sync_presentation_cc-Opus48.md)

    說明人工修改 SSoT 後，如何處理同步、追蹤與影響分析。

  結論：可以提，而且應該提。只是如果這個 repo 會對外公開，我會建議下一步把這幾份「正式參考資料」從 ccwLog/ 移到 docs/
  publications/，讓 README 的資訊架構更一致。

────────────────────────────────────────────────────