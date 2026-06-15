# RAPTor Skills — 五項核心執行原則

本文件定義所有 `rapt-*` skill 共用的五項執行原則。各 skill 在 SKILL.md 中以標題行引用，不重複貼完整內容。

---

## PRINCIPLE 1：CWD 為產出錨點

- 本 skill 與其 sub-SOP **所有經授權產生或修改的 artifact**，**一律**落在當次執行的工作目錄（**CWD**）所涵蓋之專案樹內。
- 相對路徑自 **CWD** 解析；`.raptor/arguments.yml` 中的所有 `paths.*` 亦以 CWD 為錨。
- **【嚴禁】** 把應屬本流程的產物寫到 CWD 外的任意絕對路徑，或以「方便」為由落到未載明的其他根目錄。

---

## PRINCIPLE 2：Artifact Output Contract（硬限制）

- 本 SOP **唯一允許產生或修改**的 artifact，**只能**來自於當步 SOP 中透過 CREATE / WRITE / UPDATE 明確標注的產出物。
- **【嚴禁】** 除上述 target 外，其他任何 READ / SEARCH / THINK / DERIVE 所觀察到的路徑，都只可作為分析依據，**不得被順手建立、寫入、更新或補骨架**。
- 各 skill 的 Artifact Output Contract 定義見 `rapt-core::planner-worker-contract.md`。

---

## PRINCIPLE 3：STRICT SOP

1. **依序不漏步**：自底下列 SOP 逐一執行；每做一步，在訊息中**明示該步編號**。
2. **限縮延長推理**：僅當 sub-SOP 當步**明文**標示須 `THINK / REASONING` 時，才拉長內省與推演；否則以最直接可做之 `READ` / `PARSE` / `DERIVE` / `WRITE` / `UPDATE` / 工具呼叫達成該步，省略與該步授權範圍無關的冗長鋪墊。
3. **嚴禁自行增步**：SOP 沒有的步驟不得擅自新增，遇到障礙應記 CiC 或 EMIT 給使用者決定，不得繞過。

---

## PRINCIPLE 4：長流程待辦（Tier 0 / Tier 1）

長流程會跨多輪對話；在 conversation compact 後，執行者仍要靠**同一套待辦**還原位置。

- **Tier 0（phase）**：對應 SOP 最外層每一項 phase；這一層的勾選語意是「該 phase 的細項已全部展開**且**依 SOP 跑完」。
- **Tier 1（phase 內細項）**：僅在目前執行中的 phase 建立；對應該 phase sub-SOP 的第一層編號步驟。
- **必須工具化**：使用環境提供的任務/待辦工具（`manage_todo_list` 或等效）建立清單並在步驟間更新狀態。**禁止**只靠口頭列點。
- **進入 phase 前**才展開該 phase 的 Tier 1；**完成後**才標 Tier 0 完成，再展開下一 phase。

---

## PRINCIPLE 5：Deny-by-Default 寫入原則

- **預設禁止寫入任何路徑**。
- 只有當前步驟的 Artifact Output Contract **明確授權** CREATE / UPDATE 的路徑，才允許寫入。
- 跨 skill 委派（DELEGATE）時，被委派 skill 的 contract 獨立計算，不繼承呼叫者的授權範圍。
- Worker skill（`rapt-form-*`）只能寫入 caller 在 payload 中明確指定的 `target_path`，不得推斷或自行擴展。
