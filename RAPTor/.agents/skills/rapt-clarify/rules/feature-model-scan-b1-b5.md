# 行為模型掃描規則（B1-B5）

本文件定義 `rapt-clarify/01-gap-scan` 對高階 Gherkin feature files 執行的結構性掃描規則。

---

## B1：每個 Feature 必須有 source_evidence comment

```
規則：每個 .feature 檔案開頭必須有 # source: <引用>
嚴重度：WARNING
處理：CREATE CiC ASM，提醒補上來源引用
```

**掃描方法**：READ 每個 .feature 的前 5 行，SEARCH `# source:`。

---

## B2：每個 Scenario 必須有完整 Given-When-Then

```
規則：每個 Scenario 必須包含 Given、When、Then 三段
嚴重度：ERROR
處理：CREATE CiC GAP，不完整的 Scenario 需補全
```

**例外**：若 Background 已提供 Given，Scenario 可以省略 Given。

---

## B3：Story Index 中的 must-have story 必須有對應 Feature

```
規則：story-index.md 中 priority = must-have 的 story，Feature 欄位不得為空
嚴重度：WARNING
處理：CREATE CiC GAP，標明哪個 story 尚未有 Feature
```

---

## B4：Feature 不得含技術語彙（AP-G01~AP-G04）

```
規則：依 rapt-behavior::rules/high-level-gherkin-rules.md 反模式 AP-G01~AP-G04
嚴重度：AP-G01~AP-G04 為 ERROR
處理：CREATE CiC BDY，建議回 rapt-behavior 修正
```

**掃描關鍵字**：
- AP-G01：click / button / 點擊 / 按鈕 / form submit
- AP-G02：url / api / http / post / get / patch / delete（不含業務上下文的）
- AP-G03：status code / response body / json / xml
- AP-G04：sql / database / db / redis / queue / kafka

---

## B5：When 步驟不應有過多動作

```
規則：單一 Scenario 中，When + And 超過 2 個動作（>2 個 When/And）
嚴重度：WARNING
處理：CREATE CiC ASM，建議拆成多個 Scenario
```

---

## 掃描輸出格式

```markdown
## 結構掃描發現（行為模型 B1-B5）

| 規則 | 位置 | 問題 | 嚴重度 | 建議 |
|------|------|------|-------|------|
| B1 | order-checkout.feature | 缺少 # source: comment | WARNING | 補上 source 引用 |
| B2 | payment.feature#Scenario:付款失敗 | 缺少 Then 段 | ERROR | 補上預期業務結果 |
| B4 | user-login.feature#Scenario:登入 | When 含 "點擊登入按鈕" | ERROR | 改為業務語言 |
```
