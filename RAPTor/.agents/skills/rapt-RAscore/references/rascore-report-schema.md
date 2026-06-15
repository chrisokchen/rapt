# RAscore Report Schema

`rapt-RAscore` 輸出四個主要檔案。

## rascore-scorecard.yml

機器可讀，來源是 LLM draft 加上 `rascore_calculate.py` 的 deterministic 計算。

必要欄位：

```yaml
project: <project-name>
rascore_version: "0.1"
advisory_only: true
score:
  total: 78.0
  raw_grade: B
  grade: B
  veto:
    triggered: false
    rules: []
dimensions:
  A:
    name: 需求覆蓋與保真度
    weight: 0.2
    average: 2.33
    weighted_score: 15.56
criteria:
  A1:
    score: 2
    confidence: medium
    reason: "..."
findings: []
```

## rascore-report.md

人類可讀報告。

```markdown
# RAPTor RAscore 評分報告

專案：{project}
評分模式：LLM-assisted advisory-only

## 總覽

| 項目 | 結果 |
|---|---:|
| RAscore | {total} / 100 |
| Raw Grade | {raw_grade} |
| Advisory Grade | {grade} |
| 否決條件 | {veto} |

## 維度分數

## 否決條件

## 前 5 個重要缺口

## Specification Quality Report

## Cross-Spec Consistency Report

## Traceability Report

## 建議行動
```

## rascore-findings.md

依 severity 排序的缺口清單。

```markdown
# RAscore Findings

## Critical

### RA-D2-001

- Criterion:
- Category:
- Artifact:
- Location:
- Issue:
- Recommendation:
- Owner Skill:
- Recommended Action Type:
```

## rascore-findings.json

機器可讀 findings，供 `rapt-reconcile` 優先讀取。

```json
{
  "findings": [
    {
      "id": "RA-D1-001",
      "criterion": "D1",
      "category": "cross-spec-gap",
      "severity": "medium",
      "artifact": ".raptor/reports/rascore-precheck.json",
      "location": "cross_spec",
      "issue": "...",
      "recommendation": "...",
      "owner_skill": "rapt-reconcile",
      "recommended_action_type": "traceability_mapping"
    }
  ]
}
```
