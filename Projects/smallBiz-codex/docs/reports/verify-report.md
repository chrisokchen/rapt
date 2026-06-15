# RAPTor Verify Report

> 報告 ID：VERIFY-260613-002
> 產生時間：2026-06-13T10:15:00+08:00
> 結論：PASS

## Status Summary

| 項目 | 狀態 | 摘要 |
|---|---|---|
| Completeness | PASS | 必要 SSoT artifact 都存在且非空。 |
| Cross-DSL Consistency | PASS | haAPI/haPDL YAML 可解析，`schema_version` 皆為 `3.3`，entity 可對應 DBML table，permission refs 可對應 haARM。 |
| Traceability | PASS | 45/45 scenarios 有 L2 mapping，45/45 scenarios 有 L3 intent mapping。 |
| Coverage | PASS | Must-have 15/15，Should-have 3/3，整體 18/18。 |

## Phase Gate

Phase 5 gate：PASS。

`can_continue: true`，沒有 blocker，也沒有 NEED_TO_CLARIFY。

## NEED_TO_FIX

目前沒有 NEED_TO_FIX findings。

## NEED_TO_CLARIFY

目前沒有 NEED_TO_CLARIFY findings。

## NOTE_ONLY

### FIND-260613-004：L2 confidence 仍偏低

嚴重度：low  
Owner：`rapt-reconcile`

9 個 L2 row 仍為 `low` confidence：

- `SCN-DISC-002`
- `SCN-INV-002`
- `SCN-CHECKOUT-003`
- `SCN-MEMBER-002`
- `SCN-MEMBER-003`
- `SCN-MEMBER-004`
- `SCN-RETURN-001`
- `SCN-RETURN-002`
- `SCN-RETURN-003`

這不阻擋 Phase 5 gate，但會影響 RAscore readiness。後續可補 read/write tables、fields 與 constraints。

## RAscore Readiness

| 檢查 | 狀態 |
|---|---|
| glossary / DBML mapping | PASS |
| ref_code / seeds coverage | PASS |
| constraints coverage | PASS |
| L3 intent traceability | PASS |
| L2 evidence strength | PARTIAL |

## Next Actions

1. 可進入 `/rapt-RAscore` 做 advisory scoring。
2. 若要提高 RAscore，可先補強 NOTE_ONLY 中 9 個 low-confidence L2 row。

