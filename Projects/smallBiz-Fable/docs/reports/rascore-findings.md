# RAscore Findings


## Medium

### RA-F1-001

- Criterion: F1
- Category: cross-spec-gap
- Artifact: ``
- Location: 
- Issue: 會員等級門檻金額未定，tier 場景無法量化斷言
- Recommendation: 待平台提案後補門檻金額並量化 Then；目前以規則層變數承接
- Owner Skill: `rapt-clarify`
- Recommended Action Type: `traceability_mapping`


## Low

### RA-B5-001

- Criterion: B5
- Category: naming-drift
- Artifact: ``
- Location: 
- Issue: feature 內 entities 偶用『物流單』『SKU』等同義詞
- Recommendation: 下一輪重渲染時統一為 glossary canonical term
- Owner Skill: `rapt-behavior`
- Recommended Action Type: `manual_review`

### RA-D3-001

- Criterion: D3
- Category: data-orphan
- Artifact: ``
- Location: 
- Issue: AuditLog/Invoice/Payment/Refund 等支援實體無直接行為場景
- Recommendation: 可選擇補稽核/發票/退款的明確 scenario，或維持為支援實體保留
- Owner Skill: `rapt-behavior`
- Recommended Action Type: `manual_review`
