# 04 Coverage Check SOP

**目的**：計算 Story Index 的覆蓋率指標，確保 must-have 故事全部有對應的高階 Gherkin。

---

## 步驟

### 4.1 READ story index

READ `${paths.high_gherkin_dir}/story-index.md`，提取：
```
stories = [{story_id, title, priority, feature_ref}]
```

若舊專案只有 `${paths.business_discovery_dir}/02-story-index.md`，可作 fallback，但必須在報告中記 warning，並建議遷移到 `${paths.high_gherkin_dir}/story-index.md`。

### 4.2 CALCULATE coverage by priority

```
must_have_total = count(priority == must-have)
must_have_covered = count(priority == must-have AND feature_ref != null)
must_have_coverage = must_have_covered / must_have_total

should_have_total = ...
could_have_total = ...
```

### 4.3 EVALUATE 閘門

```
Phase 5 Gate：
  - must-have coverage >= 100%   → PASS（不到則 FAIL）
  - should-have coverage >= 80%  → PASS（不到則 WARNING）
  - overall coverage metric       → 記錄（無閘門）
```

### 4.4 OUTPUT coverage_result

```yaml
coverage:
  status: PASS | PARTIAL | FAIL
  must_have: {total: N, covered: M, pct: "100%"}
  should_have: {total: N, covered: M, pct: "85%"}
  could_have: {total: N, covered: M, pct: "40%"}
  overall: "78%"
  uncovered_must_have: []
```
