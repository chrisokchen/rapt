# Clarify Backlog

> 更新日期：2026-06-13
> OPEN 總數：0
> ANSWERED 總數：0
> RESOLVED 總數：6
> 來源：`docs/discovery/04-vision-kpi-scope.md`、`docs/ssot/dbml/constraints.md`、`.raptor/traceability.md`

## GAP：需求缺口或規則未定

| ID | 位置 | 描述 | 影響 | 狀態 | 決策來源 |
|----|------|------|------|------|----------|
| CiC-GAP-001 | `docs/discovery/04-vision-kpi-scope.md#待釐清議題`、`docs/ssot/dbml/constraints.md#CON-OPEN-INVENTORY-RESERVATION` | 庫存只剩 1 件而多位消費者同時結帳時，尚未定義扣庫存時機、是否需要庫存預留、預留釋放時間與付款逾時關係。 | `InventoryItem.availableQty`、`InventoryMovement`、`SalesOrder.orderStatus`、庫存與結帳情境。 | RESOLVED | `.clarify/decisions/batch-CLR-260613-001.md#q1-cic-gap-001庫存扣減與預留策略` |
| CiC-GAP-002 | `docs/discovery/04-vision-kpi-scope.md#待釐清議題`、`docs/ssot/dbml/constraints.md#CON-OPEN-DISCOUNT-STACKING` | 活動價、優惠券、會員折扣、點數折抵的可疊加、互斥與計算順序未定；目前僅確認一筆訂單最多一張優惠券。 | `Promotion`、`Coupon`、`CouponRedemption`、`PointLedger`、`SalesOrder.discountAmount`、促銷與結帳情境。 | RESOLVED | `.clarify/decisions/batch-CLR-260613-001.md#q2-cic-gap-002折扣疊加與計算順序` |
| CiC-GAP-003 | `docs/discovery/04-vision-kpi-scope.md#待釐清議題`、`docs/ssot/dbml/constraints.md#CON-OPEN-LOYALTY-RULES` | 會員分級依據、計算區間、升降級時機、等級權益、點數折抵上限、點數效期與點數回饋基準未定。 | `MemberLevel`、`ConsumerProfile.memberLevelId`、`PointLedger`、會員忠誠情境與促銷資格。 | RESOLVED | `.clarify/decisions/batch-CLR-260613-001.md#q3-cic-gap-003會員分級與點數生命週期` |
| CiC-GAP-004 | `docs/discovery/04-vision-kpi-scope.md#待釐清議題`、`docs/ssot/dbml/constraints.md#CON-OPEN-ORDER-CANCEL-REFUND` | 下單後未付款保留時間、逾時取消時限、已付款訂單是否可取消，以及取消與退款流程關係未定。 | `SalesOrder.orderStatus`、`Payment.paymentStatus`、`Refund`、庫存釋放與訂單履約情境。 | RESOLVED | `.clarify/decisions/batch-CLR-260613-001.md#q4-cic-gap-004付款逾時取消與退款` |
| CiC-GAP-005 | `docs/discovery/04-vision-kpi-scope.md#待釐清議題`、`docs/ssot/dbml/constraints.md#CON-OPEN-TAX-BASE` | 5% 營業稅稅基未定，不清楚依商品小計、折扣後金額，或折扣後再加運費計算。 | `SalesOrder.taxAmount`、`SalesOrder.totalAmount`、結帳金額明細、發票/金流對帳規則。 | RESOLVED | `.clarify/decisions/batch-CLR-260613-001.md#q5-cic-gap-0055-營業稅稅基` |
| CiC-GAP-006 | `docs/discovery/04-vision-kpi-scope.md#待釐清議題`、`docs/ssot/dbml/constraints.md#CON-OPEN-RETURN-POLICY` | 線上退貨期限、不可退商品範圍、特價品或已拆封品處理方式，以及退款是否必須原路退回未定。 | `ReturnRequest.returnStatus`、`Refund.refundStatus`、`Payment.paymentMethod`、退貨退款情境。 | RESOLVED | `.clarify/decisions/batch-CLR-260613-002.md#q6-cic-gap-006退貨期限不可退範圍與退款路徑` |

## ASM：假設待確認

| ID | 位置 | 假設 | 狀態 |
|----|------|------|------|
| - | - | 目前未掃描到獨立 ASM。 | - |

## BDY：邊界待調和

| ID | 位置 | 描述 | 狀態 |
|----|------|------|------|
| - | - | 目前未掃描到獨立 BDY。 | - |

## CON：衝突待裁決

| ID | 位置 | 描述 | 狀態 |
|----|------|------|------|
| - | - | 目前未掃描到獨立 CON。 | - |

## 結構掃描摘要

| 規則 | 結果 | 備註 |
|------|------|------|
| A1-A6 DBML | PASS | 6 個開放限制已裁決，並補入 `docs/ssot/dbml/constraints.md` 的 Clarification Decision Constraints。 |
| B1-B5 Gherkin | PASS | 待釐清情境保留歷史脈絡，已補入各 feature 的 Clarification Decisions。 |
| C1-C3 haARM | PASS | 權限邊界無新增待釐清項。 |

## RAscore Findings

未發現 `docs/reports/rascore-findings.json`、`docs/reports/rascore-findings.md` 或 `docs/reports/rascore-scorecard.yml`。
