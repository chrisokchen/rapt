# RAscore Findings


## Low

### RA-B4-001

- Criterion: B4
- Category: gherkin-quality
- Artifact: ``
- Location: 
- Issue: 部分資料變更 feature（play-session/assignment/graduated-hint）缺個別負向/失敗 scenario。
- Recommendation: 視需要補拒絕/失敗 scenario 或於 story-index matrix 標不適用。
- Owner Skill: `rapt-behavior`
- Recommended Action Type: `behavior_revision`

### RA-D3-001

- Criterion: D3
- Category: cross-spec-gap
- Artifact: ``
- Location: 
- Issue: 9 個 DBML table 未直接出現在任何 scenario # entities（identity/infra 或僅由 L3 intent 承接）。
- Recommendation: 於 traceability 標註保留理由，或在相關 scenario 補 # entities 以顯式關聯。
- Owner Skill: `rapt-reconcile`
- Recommended Action Type: `traceability_mapping`

### RA-F1-001

- Criterion: F1
- Category: gherkin-quality
- Artifact: ``
- Location: 
- Issue: 少數 Then 以教學語氣/語用描述，缺可機械斷言的觀察點。
- Recommendation: 為質性教學 scenario 補可觀察代理指標（如 hint level 對應、用語層級標記）。
- Owner Skill: `rapt-behavior`
- Recommended Action Type: `behavior_revision`
