# Domain Constraints

> 最後更新：2026-06-12
> 來源：`docs/discovery/04-vision-kpi-scope.md`、`docs/ssot/habdd/*.ha.feature`

## Constraint Catalog

| constraint_id | type | owner_table | owner_field | rule | source | related_scenarios | enforcement |
|---|---|---|---|---|---|---|---|
| CON-CATALOG-001 | lifecycle | Product | productStatus | 商品上架前必須至少有一個 SKU，且 SKU 需有售價與庫存資料。 | product-catalog.ha.feature | SCN-CATALOG-002, SCN-CATALOG-003 | haAPI |
| CON-CATALOG-002 | price | ProductSku | salePrice | SKU 售價必須大於 0。 | raw-input/3-draftSpec.md#1.2 | SCN-CATALOG-001 | haAPI |
| CON-INVENTORY-001 | quantity | InventoryItem | availableQty | 可販售庫存不得小於 0。 | inventory-control.ha.feature | SCN-INV-002, SCN-INV-004 | haAPI |
| CON-INVENTORY-002 | state-transition | InventoryMovement | movementType | 銷售扣減、人工調整、退貨回補都必須產生庫存異動紀錄。 | inventory-control.ha.feature | SCN-INV-002, SCN-INV-003 | haAPI |
| CON-ORDER-001 | state-transition | SalesOrder | orderStatus | 訂單狀態至少支援待付款、已付款、已確認、已出貨、已送達、已取消、已退款。 | docs/discovery/04-vision-kpi-scope.md#範圍邊界 | SCN-CHECKOUT-001, SCN-CHECKOUT-002, SCN-ORDER-002, SCN-RETURN-003 | haAPI |
| CON-ORDER-002 | snapshot | OrderItem | productNameSnapshot | 訂單項目必須保留商品名稱、SKU 代碼與單價快照，避免商品改價影響歷史訂單。 | raw-input/3-draftSpec.md#4.1 | SCN-CATALOG-004 | haAPI |
| CON-PAYMENT-001 | sensitive-data | Payment | paymentMethod | 平台不得保存信用卡等敏感支付資訊，付款明細由金流服務商處理。 | docs/discovery/04-vision-kpi-scope.md#Out-of-Scope | OOS-002 | haAPI |
| CON-COUPON-001 | uniqueness | CouponRedemption | orderId | 一筆訂單最多使用一張優惠券。 | promotion-coupon.ha.feature | SCN-PROMO-003 | haAPI |
| CON-COUPON-002 | eligibility | Coupon | memberLevelId | 限定會員等級的優惠券只能由符合等級資格的會員使用。 | promotion-coupon.ha.feature | SCN-PROMO-002, SCN-MEMBER-004 | haAPI |
| CON-AUTH-001 | tenant-scope | Merchant | merchantId | 商家只能管理自己商店的商品、訂單、庫存、促銷、報表與退貨資料。 | access-boundary.ha.feature | SCN-AUTH-001 | haARM |
| CON-AUTH-002 | owner-scope | ConsumerProfile | consumerId | 消費者只能查看與處理自己的訂單、地址、購物車、願望清單、點數與退貨申請。 | access-boundary.ha.feature | SCN-AUTH-002 | haARM |
| CON-REPORT-001 | empty-result | SalesOrder | placedAt | 指定期間無訂單時，報表必須呈現零銷售結果，不得產生推估數字。 | merchant-reporting.ha.feature | SCN-REPORT-003 | generated-test |

## Resolved CiC Constraints (historical)

<!-- CiC GAP #001 -->
**類型**：GAP
**位置**：docs/ssot/dbml/constraints.md#CON-OPEN-INVENTORY-RESERVATION
**描述**：庫存預留、扣庫存時點、預留釋放時間已依 DEC-CLR-001 裁決。
**影響**：`InventoryItem.availableQty`、`InventoryMovement`、`SalesOrder.orderStatus`、結帳與付款狀態轉換。
**推薦**：在 rapt-clarify 決定下單扣庫存、付款扣庫存或預留制。
<!-- /CiC -->

<!-- CiC GAP #002 -->
**類型**：GAP
**位置**：docs/ssot/dbml/constraints.md#CON-OPEN-DISCOUNT-STACKING
**描述**：活動價、優惠券、會員折扣、點數折抵的計算順序與互斥規則已依 DEC-CLR-002 裁決。
**影響**：`Promotion`、`Coupon`、`CouponRedemption`、`PointLedger`、`SalesOrder.discountAmount`。
**推薦**：在 rapt-clarify 決定折扣疊加矩陣與金額計算順序。
<!-- /CiC -->

<!-- CiC GAP #003 -->
**類型**：GAP
**位置**：docs/ssot/dbml/constraints.md#CON-OPEN-LOYALTY-RULES
**描述**：會員分級、升降級排程與點數 MVP 範圍已依 DEC-CLR-003 裁決。
**影響**：`MemberLevel`、`ConsumerProfile.memberLevelId`、`PointLedger`。
**推薦**：在 rapt-clarify 先決定 MVP 會員等級與點數生命週期。
<!-- /CiC -->

<!-- CiC GAP #004 -->
**類型**：GAP
**位置**：docs/ssot/dbml/constraints.md#CON-OPEN-ORDER-CANCEL-REFUND
**描述**：待付款保留時間、逾時取消時限、已付款取消與退款關係已依 DEC-CLR-004 裁決。
**影響**：`SalesOrder.orderStatus`、`Payment.paymentStatus`、`Refund`、庫存釋放。
**推薦**：在 rapt-clarify 決定訂單狀態轉換圖。
<!-- /CiC -->

<!-- CiC GAP #005 -->
**類型**：GAP
**位置**：docs/ssot/dbml/constraints.md#CON-OPEN-TAX-BASE
**描述**：5% 營業稅稅基已依 DEC-CLR-005 裁決。
**影響**：`SalesOrder.taxAmount`、`SalesOrder.totalAmount`、發票與報表。
**推薦**：由財務或稅務口徑確認後回寫 constraints。
<!-- /CiC -->

<!-- CiC GAP #006 -->
**類型**：GAP
**位置**：docs/ssot/dbml/constraints.md#CON-OPEN-RETURN-POLICY
**描述**：退貨期限、不可退商品與退款路徑已依 DEC-CLR-006 裁決。
**影響**：`ReturnRequest.returnStatus`、`Refund.refundStatus`、`Payment.paymentMethod`。
**推薦**：在 rapt-clarify 決定平台統一或商家自訂退貨政策。
<!-- /CiC -->

## Compatibility Decisions

| item | decision | risk | compensating_rule | source |
|---|---|---|---|---|
| OrderItem product snapshot fields | 保留商品名稱、SKU 代碼、單價快照 | 商品後續改名或改價時，快照與商品主檔不一致是預期行為 | CON-ORDER-002 | raw-input/3-draftSpec.md#4.1 |
## Clarification Decision Constraints

> 更新日期：2026-06-13
> 來源：`.clarify/decisions/batch-CLR-260613-001.md`、`.clarify/decisions/batch-CLR-260613-002.md`

| constraint_id | type | owner_table | owner_field | rule | source | related_scenarios | enforcement |
|---|---|---|---|---|---|---|---|
| CON-CLARIFY-001 | inventory-reservation | InventoryItem | availableQty | 下單成立時建立庫存預留，付款完成時正式扣減；未付款訂單逾時取消時，預留庫存必須自動釋放。 | `.clarify/decisions/batch-CLR-260613-001.md#q1-cic-gap-001庫存扣減與預留策略` | SCN-INV-002, SCN-INV-005, SCN-ORDER-005 | haAPI |
| CON-CLARIFY-002 | discount-stacking | SalesOrder | discountAmount | 活動價可與優惠券或會員折扣擇一疊加；優惠券與會員折扣互斥；點數折抵最後計算。 | `.clarify/decisions/batch-CLR-260613-001.md#q2-cic-gap-002折扣疊加與計算順序` | SCN-PROMO-004, SCN-CHECKOUT-003 | haAPI |
| CON-CLARIFY-003 | loyalty-mvp | PointLedger | pointType | MVP 啟用點數累積與折抵；會員分級固定手動維護；自動升降級排程延後。 | `.clarify/decisions/batch-CLR-260613-001.md#q3-cic-gap-003會員分級與點數生命週期` | SCN-MEMBER-002, SCN-MEMBER-003, SCN-MEMBER-004, SCN-MEMBER-005 | haAPI |
| CON-CLARIFY-004 | order-timeout-cancel | SalesOrder | orderStatus | 未付款訂單保留 30 分鐘後自動取消；已付款訂單出貨前可取消並原路退款。 | `.clarify/decisions/batch-CLR-260613-001.md#q4-cic-gap-004付款逾時取消與退款` | SCN-ORDER-005, SCN-INV-005 | haAPI |
| CON-CLARIFY-005 | tax-base | SalesOrder | taxAmount | 5% 營業稅以商品小計扣除活動、優惠券、會員折扣與點數折抵後的商品金額作為稅基，不含運費。 | `.clarify/decisions/batch-CLR-260613-001.md#q5-cic-gap-0055-營業稅稅基` | SCN-CHECKOUT-003, SCN-CHECKOUT-005 | haAPI |
| CON-CLARIFY-006 | return-policy | ReturnRequest | returnStatus | 到貨後 7 天內可申請退貨；已拆封、個人化商品、耗材不可退；退款必須原路退回。 | `.clarify/decisions/batch-CLR-260613-002.md#q6-cic-gap-006退貨期限不可退範圍與退款路徑` | SCN-RETURN-001, SCN-RETURN-002, SCN-RETURN-003, SCN-RETURN-004 | haAPI |
