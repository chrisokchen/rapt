# Seeds and Value Sets

> 最後更新：2026-06-12
> 來源：`docs/discovery/04-vision-kpi-scope.md`、`docs/ssot/habdd/*.ha.feature`

## AccountType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Account | accountType | M | 商家 | 商家後台使用者 | docs/discovery/01-stakeholders.md | true |
| Account | accountType | C | 消費者 | 前台購物會員 | docs/discovery/01-stakeholders.md | true |
| Account | accountType | A | 平台管理 | 平台管理員或營運人員 | docs/discovery/01-stakeholders.md | true |

## AccountStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Account | accountStatus | P | 待驗證 | 已註冊但 Email 尚未驗證 | membership-loyalty.ha.feature#SCN-MEMBER-001 | true |
| Account | accountStatus | A | 啟用 | 可登入與操作 | membership-loyalty.ha.feature#SCN-MEMBER-001 | true |
| Account | accountStatus | S | 停用 | 帳號暫停使用 | docs/discovery/04-vision-kpi-scope.md#權限區隔 | true |

## MerchantPlanStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Merchant | planStatus | A | 月租有效 | 商家月租有效 | docs/discovery/04-vision-kpi-scope.md#Vision | true |
| Merchant | planStatus | P | 待付款 | 商家月租待付款 | docs/discovery/04-vision-kpi-scope.md#Vision | true |
| Merchant | planStatus | S | 暫停 | 商家月租暫停 | docs/discovery/04-vision-kpi-scope.md#Vision | true |

## ProductStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Product | productStatus | D | 草稿 | 商品尚未可販售 | product-catalog.ha.feature#SCN-CATALOG-001 | true |
| Product | productStatus | A | 上架 | 商品可販售 | product-catalog.ha.feature#SCN-CATALOG-002 | true |
| Product | productStatus | I | 下架 | 商品不接受新購買 | product-catalog.ha.feature#SCN-CATALOG-004 | true |

## SkuStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| ProductSku | skuStatus | A | 啟用 | SKU 可販售 | product-catalog.ha.feature#SCN-CATALOG-002 | true |
| ProductSku | skuStatus | I | 停用 | SKU 不可販售 | product-catalog.ha.feature#SCN-CATALOG-004 | true |

## InventoryMovementType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| InventoryMovement | movementType | S | 銷售扣減 | 因訂單成立或付款扣減庫存 | inventory-control.ha.feature#SCN-INV-002 | true |
| InventoryMovement | movementType | A | 人工調整 | 商家調整庫存 | inventory-control.ha.feature#SCN-INV-001 | true |
| InventoryMovement | movementType | R | 退貨回補 | 退貨確認後回補庫存 | return-refund.ha.feature#SCN-RETURN-003 | true |

## CartStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Cart | cartStatus | A | 使用中 | 可繼續結帳 | product-discovery.ha.feature#SCN-DISC-003 | true |
| Cart | cartStatus | C | 已轉訂單 | 已由購物車產生訂單 | checkout-payment.ha.feature#SCN-CHECKOUT-001 | true |

## OrderStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| SalesOrder | orderStatus | N | 待付款 | 訂單已建立但尚未付款 | checkout-payment.ha.feature#SCN-CHECKOUT-001 | true |
| SalesOrder | orderStatus | P | 已付款 | 付款完成 | checkout-payment.ha.feature#SCN-CHECKOUT-002 | true |
| SalesOrder | orderStatus | C | 已確認 | 商家確認訂單 | order-fulfillment.ha.feature#SCN-ORDER-004 | true |
| SalesOrder | orderStatus | S | 已出貨 | 商家已標記出貨 | order-fulfillment.ha.feature#SCN-ORDER-002 | true |
| SalesOrder | orderStatus | D | 已送達 | 物流已送達 | order-fulfillment.ha.feature#SCN-ORDER-003 | true |
| SalesOrder | orderStatus | X | 已取消 | 訂單取消 | docs/discovery/04-vision-kpi-scope.md#待釐清議題 | true |
| SalesOrder | orderStatus | R | 已退款 | 退款完成 | return-refund.ha.feature#SCN-RETURN-003 | true |

## PaymentMethod

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Payment | paymentMethod | C | 信用卡 | 信用卡付款 | checkout-payment.ha.feature#SCN-CHECKOUT-002 | true |
| Payment | paymentMethod | P | PayPal | PayPal 付款 | checkout-payment.ha.feature#SCN-CHECKOUT-002 | true |
| Payment | paymentMethod | B | 銀行轉帳 | 銀行轉帳付款 | checkout-payment.ha.feature#SCN-CHECKOUT-002 | true |

## PaymentStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Payment | paymentStatus | N | 待付款 | 尚未完成付款 | checkout-payment.ha.feature#SCN-CHECKOUT-001 | true |
| Payment | paymentStatus | P | 已付款 | 付款完成 | checkout-payment.ha.feature#SCN-CHECKOUT-002 | true |
| Payment | paymentStatus | F | 付款失敗 | 付款未成功 | checkout-payment.ha.feature#SCN-CHECKOUT-002 | true |
| Payment | paymentStatus | R | 已退款 | 付款已退款 | return-refund.ha.feature#SCN-RETURN-003 | true |

## ShipmentStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Shipment | shipmentStatus | P | 待出貨 | 尚未出貨 | order-fulfillment.ha.feature#SCN-ORDER-002 | true |
| Shipment | shipmentStatus | S | 已出貨 | 已交付物流 | order-fulfillment.ha.feature#SCN-ORDER-002 | true |
| Shipment | shipmentStatus | T | 配送中 | 物流配送中 | order-fulfillment.ha.feature#SCN-ORDER-004 | true |
| Shipment | shipmentStatus | D | 已送達 | 已送達消費者 | order-fulfillment.ha.feature#SCN-ORDER-003 | true |

## PointType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| PointLedger | pointType | E | 獲得 | 訂單回饋點數 | membership-loyalty.ha.feature#SCN-MEMBER-002 | true |
| PointLedger | pointType | U | 使用 | 訂單折抵點數 | membership-loyalty.ha.feature#SCN-MEMBER-003 | true |
| PointLedger | pointType | X | 到期 | 點數到期失效 | docs/discovery/04-vision-kpi-scope.md#待釐清議題 | true |

## PromotionType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Promotion | promotionType | P | 百分比折扣 | 依比例折扣 | promotion-coupon.ha.feature#SCN-PROMO-001 | true |
| Promotion | promotionType | A | 固定金額折抵 | 滿額折現或固定折抵 | promotion-coupon.ha.feature#SCN-PROMO-001 | true |
| Promotion | promotionType | B | 買 X 送 Y | 購買指定商品贈送商品 | promotion-coupon.ha.feature#SCN-PROMO-001 | true |

## PromotionStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Promotion | promotionStatus | D | 草稿 | 活動尚未生效 | promotion-coupon.ha.feature#SCN-PROMO-001 | true |
| Promotion | promotionStatus | A | 生效 | 活動有效中 | promotion-coupon.ha.feature#SCN-PROMO-001 | true |
| Promotion | promotionStatus | E | 結束 | 活動已結束 | promotion-coupon.ha.feature#SCN-PROMO-001 | true |

## DiscountType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Coupon | discountType | P | 百分比 | 百分比折扣 | promotion-coupon.ha.feature#SCN-PROMO-002 | true |
| Coupon | discountType | A | 固定金額 | 固定金額折抵 | promotion-coupon.ha.feature#SCN-PROMO-002 | true |

## CouponStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Coupon | couponStatus | D | 草稿 | 尚未可使用 | promotion-coupon.ha.feature#SCN-PROMO-002 | true |
| Coupon | couponStatus | A | 生效 | 可使用 | promotion-coupon.ha.feature#SCN-PROMO-002 | true |
| Coupon | couponStatus | E | 失效 | 已過期或停用 | promotion-coupon.ha.feature#SCN-PROMO-002 | true |

## ReturnStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| ReturnRequest | returnStatus | P | 待審核 | 退貨申請等待商家審核 | return-refund.ha.feature#SCN-RETURN-001 | true |
| ReturnRequest | returnStatus | A | 已核准 | 商家核准退貨 | return-refund.ha.feature#SCN-RETURN-002 | true |
| ReturnRequest | returnStatus | R | 已拒絕 | 商家未核准退貨 | return-refund.ha.feature#SCN-RETURN-002 | true |
| ReturnRequest | returnStatus | C | 已完成 | 退貨與退款完成 | return-refund.ha.feature#SCN-RETURN-003 | true |

## RefundStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Refund | refundStatus | P | 待退款 | 尚未完成退款 | return-refund.ha.feature#SCN-RETURN-003 | true |
| Refund | refundStatus | R | 已退款 | 退款完成 | return-refund.ha.feature#SCN-RETURN-003 | true |
| Refund | refundStatus | F | 退款失敗 | 退款未完成 | return-refund.ha.feature#SCN-RETURN-003 | true |

## NotificationType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Notification | notificationType | O | 訂單狀態 | 訂單狀態變更通知 | order-fulfillment.ha.feature#SCN-ORDER-004 | true |
| Notification | notificationType | R | 退貨退款 | 退貨或退款通知 | return-refund.ha.feature#SCN-RETURN-003 | true |

## NotificationChannel

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Notification | channel | L | LINE | LINE 通知 | order-fulfillment.ha.feature#SCN-ORDER-004 | true |
| Notification | channel | E | Email | Email 通知 | order-fulfillment.ha.feature#SCN-ORDER-004 | true |

## NotificationStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Notification | notificationStatus | P | 待送出 | 尚未送出 | order-fulfillment.ha.feature#SCN-ORDER-004 | true |
| Notification | notificationStatus | S | 已送出 | 通知已送出 | order-fulfillment.ha.feature#SCN-ORDER-004 | true |
| Notification | notificationStatus | F | 送出失敗 | 通知未成功送出 | order-fulfillment.ha.feature#SCN-ORDER-004 | true |
## Clarification Value Rules

| item | value | meaning | source | active |
|---|---|---|---|---|
| inventory_reservation_timeout | 30_minutes | 未付款訂單保留 30 分鐘後自動取消，並釋放預留庫存。 | `.clarify/decisions/batch-CLR-260613-001.md#q4-cic-gap-004付款逾時取消與退款` | true |
| tax_rate | 5_percent | 營業稅率為 5%，稅基為折扣與點數折抵後商品金額，不含運費。 | `.clarify/decisions/batch-CLR-260613-001.md#q5-cic-gap-0055-營業稅稅基` | true |
| return_window | 7_days_after_delivery | 到貨後 7 天內可申請退貨。 | `.clarify/decisions/batch-CLR-260613-002.md#q6-cic-gap-006退貨期限不可退範圍與退款路徑` | true |
| refund_route | original_payment_method | 退款必須原路退回。 | `.clarify/decisions/batch-CLR-260613-002.md#q6-cic-gap-006退貨期限不可退範圍與退款路徑` | true |
