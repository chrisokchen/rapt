# 02 Static Precheck SOP

**目的**：產生半自動 evidence，供 LLM 依 rubric 評分時引用。precheck 不取代評分。

---

## 步驟 2.1：執行 precheck

```
RUN: python {skill_dir}/scripts/rascore_precheck.py \
       --features {paths.high_gherkin_dir} \
       --dbml {paths.data_model_dir} \
       --glossary {paths.data_model_dir}/glossary.md \
       --seeds {paths.data_model_dir}/seeds.md \
       --constraints {paths.data_model_dir}/constraints.md \
       --trace {paths.traceability_file} \
       --output {paths.reports_dir}/rascore-precheck.json
```

若 glossary、seeds、constraints 或 traceability 不存在，仍傳入路徑；script 會將其標為 missing。

---

## 步驟 2.2：檢查 precheck 結果

READ `${paths.reports_dir}/rascore-precheck.json`。

若 script exit code != 0：

- 若原因是找不到 `.feature` 或 `.dbml`：停止。
- 其他原因：EMIT warning，改用純 LLM 人工 evidence 評分。

---

## 步驟 2.3：使用 evidence

precheck evidence 可用於：

- B1：UI / 技術細節洩漏詞。
- B2：過長 Scenario。
- B3：Given / When / Then 缺漏。
- C1-C3：Table、Enum、Ref、PK 基本缺口。
- D1-D3：詞彙候選、unmatched terms、orphan tables 初篩。
- D1-D3：glossary-aware mapping、L2 Scenario Data Mapping 覆蓋率、orphan tables after glossary。
- D4：seeds / constraints 是否存在與可掃描。
- E1-E2：traceability 檔案是否存在與可掃描的 trace 線索。

所有 evidence 都要視為「提示」，最終分數仍由 LLM 依 rubric 與 artifact 內容判斷。
