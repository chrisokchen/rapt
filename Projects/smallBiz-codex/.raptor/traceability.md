# RAPTor Traceability

> 最後更新：2026-06-12
> schema: rapt-core traceability-schema

## L1 Requirement Coverage

| req_or_story | source | feature | scenario_count | status | notes |
|---|---|---|---:|---|---|
| US-001 | docs/discovery/02-user-journeys.md#建立商品與銷售單位 | product-catalog.ha.feature | 2 | covered | 建立商品與 SKU。 |
| US-002 | docs/discovery/02-user-journeys.md#建立商品與銷售單位 | product-catalog.ha.feature | 2 | covered | 上架、下架與負向場景。 |
| US-003 | docs/discovery/02-user-journeys.md#尋找商品 | product-discovery.ha.feature | 1 | covered | 商品資訊與價格理解。 |
| US-004 | docs/discovery/02-user-journeys.md#收藏或加入購物車 | product-discovery.ha.feature | 3 | covered | 願望清單、購物車保留、售完商品。 |
| US-005 | docs/discovery/02-user-journeys.md#設定庫存與補貨水位 | inventory-control.ha.feature | 2 | covered | 庫存水位與補貨提醒。 |
| US-006 | docs/discovery/03-event-timeline.md#庫存 | inventory-control.ha.feature | 3 | covered | 庫存預留已由 DEC-CLR-001 裁決。 |
| US-007 | docs/discovery/02-user-journeys.md#結帳與付款 | checkout-payment.ha.feature | 1 | covered | 提交訂單。 |
| US-008 | docs/discovery/02-user-journeys.md#結帳與付款 | checkout-payment.ha.feature | 1 | covered | 三種付款方式。 |
| US-009 | docs/discovery/04-vision-kpi-scope.md#範圍邊界 | checkout-payment.ha.feature | 3 | covered | 稅基已由 DEC-CLR-005 裁決。 |
| US-010 | docs/discovery/02-user-journeys.md#處理訂單與出貨 | order-fulfillment.ha.feature | 2 | covered | 訂單篩選與出貨。 |
| US-011 | docs/discovery/02-user-journeys.md#追蹤訂單與配送 | order-fulfillment.ha.feature | 1 | covered | 消費者追蹤配送。 |
| US-012 | docs/discovery/04-vision-kpi-scope.md#範圍邊界 | membership-loyalty.ha.feature | 3 | covered | 點數 MVP 範圍已由 DEC-CLR-003 裁決。 |
| US-013 | docs/discovery/02-user-journeys.md#設計會員分級行銷 | membership-loyalty.ha.feature | 2 | covered | 分級規則已由 DEC-CLR-003 裁決。 |
| US-014 | docs/discovery/02-user-journeys.md#規劃促銷工具 | promotion-coupon.ha.feature | 4 | covered | 折扣疊加已由 DEC-CLR-002 裁決。 |
| US-015 | docs/discovery/02-user-journeys.md#申請退貨 | return-refund.ha.feature | 4 | covered | 退貨政策已由 DEC-CLR-006 裁決。 |
| US-016 | docs/discovery/02-user-journeys.md#查看營運報表 | merchant-reporting.ha.feature | 3 | covered | 銷售概況與商品排行。 |
| US-017 | docs/discovery/04-vision-kpi-scope.md#範圍邊界 | access-boundary.ha.feature | 3 | covered | 商家、消費者與平台管理員權限邊界。 |
| US-018 | docs/discovery/02-user-journeys.md#追蹤訂單與配送 | order-fulfillment.ha.feature | 1 | covered | 狀態通知。 |
| OOS-001 | docs/discovery/04-vision-kpi-scope.md#Out-of-Scope | out-of-scope | 0 | out-of-scope | 專案型客製建站已排除。 |
| OOS-002 | docs/discovery/04-vision-kpi-scope.md#Out-of-Scope | out-of-scope | 0 | out-of-scope | 平台保存敏感付款資訊已排除。 |

## L2 Scenario Data Mapping

| scenario_id | feature | scenario | entities | glossary_terms | read_tables | write_tables | fields | constraints | confidence | source |
|---|---|---|---|---|---|---|---|---|---|---|
| SCN-CATALOG-001 | product-catalog.ha.feature | 建立多規格商品 | 商品, SKU, 分類 | 商品, SKU, 分類 |  |  |  |  | medium | docs/ssot/habdd/product-catalog.ha.feature |
| SCN-CATALOG-002 | product-catalog.ha.feature | 上架已完成設定的商品 | 商品, SKU | 商品, SKU |  |  |  |  | medium | docs/ssot/habdd/product-catalog.ha.feature |
| SCN-CATALOG-003 | product-catalog.ha.feature | 缺少可銷售規格時維持草稿 | 商品, SKU | 商品, SKU |  |  |  |  | medium | docs/ssot/habdd/product-catalog.ha.feature |
| SCN-CATALOG-004 | product-catalog.ha.feature | 下架不再販售的商品 | 商品 | 商品 |  |  |  |  | medium | docs/ssot/habdd/product-catalog.ha.feature |
| SCN-DISC-001 | product-discovery.ha.feature | 取得可販售商品資訊 | 商品, 分類, SKU | 商品, 分類, SKU |  |  |  |  | medium | docs/ssot/habdd/product-discovery.ha.feature |
| SCN-DISC-002 | product-discovery.ha.feature | 收藏尚未立即購買的商品 | 商品, 願望清單 | 商品, 願望清單 |  |  |  |  | low | docs/ssot/habdd/product-discovery.ha.feature |
| SCN-DISC-003 | product-discovery.ha.feature | 保留購物車內容 | 購物車, SKU | 購物車, SKU |  |  |  |  | medium | docs/ssot/habdd/product-discovery.ha.feature |
| SCN-DISC-004 | product-discovery.ha.feature | 商品售完時不可加入購物車 | 商品, SKU | 商品, SKU |  |  |  |  | medium | docs/ssot/habdd/product-discovery.ha.feature |
| SCN-INV-001 | inventory-control.ha.feature | 設定 SKU 庫存與補貨水位 | SKU, 庫存水位 | SKU, 庫存水位 |  |  |  |  | medium | docs/ssot/habdd/inventory-control.ha.feature |
| SCN-INV-002 | inventory-control.ha.feature | 訂單成立後扣減庫存 | SKU, 庫存異動, 訂單 | SKU, 庫存異動, 訂單 |  |  |  | CiC GAP #001 | low | docs/ssot/habdd/inventory-control.ha.feature |
| SCN-INV-003 | inventory-control.ha.feature | 庫存低於水位時提醒商家 | SKU, 庫存水位 | SKU, 庫存水位 |  |  |  |  | medium | docs/ssot/habdd/inventory-control.ha.feature |
| SCN-INV-004 | inventory-control.ha.feature | 庫存不足時不建立可履約訂單 | SKU, 訂單 | SKU, 訂單 |  |  |  |  | medium | docs/ssot/habdd/inventory-control.ha.feature |
| SCN-INV-005 | inventory-control.ha.feature | 庫存預留規則已裁決 | SKU, 訂單 | SKU, 訂單 |  |  |  | DEC-CLR-001 | medium | docs/ssot/habdd/inventory-control.ha.feature |
| SCN-CHECKOUT-001 | checkout-payment.ha.feature | 以必要資訊提交訂單 | 購物車, 訂單, 收件資訊 | 購物車, 訂單, 收件資訊 |  |  |  |  | medium | docs/ssot/habdd/checkout-payment.ha.feature |
| SCN-CHECKOUT-002 | checkout-payment.ha.feature | 使用支援的付款方式完成付款 | 訂單, 付款 | 訂單, 付款 |  |  |  |  | medium | docs/ssot/habdd/checkout-payment.ha.feature |
| SCN-CHECKOUT-003 | checkout-payment.ha.feature | 顯示可追溯的訂單金額 | 訂單, 優惠, 運費, 稅金 | 訂單, 優惠, 運費, 稅金 |  |  |  | CiC GAP #005 | low | docs/ssot/habdd/checkout-payment.ha.feature |
| SCN-CHECKOUT-004 | checkout-payment.ha.feature | 優惠不符合資格時維持原訂單金額 | 訂單, 優惠 | 訂單, 優惠 |  |  |  |  | medium | docs/ssot/habdd/checkout-payment.ha.feature |
| SCN-CHECKOUT-005 | checkout-payment.ha.feature | 稅基規則已裁決 | 訂單, 稅金 | 訂單, 稅金 |  |  |  | DEC-CLR-005 | medium | docs/ssot/habdd/checkout-payment.ha.feature |
| SCN-ORDER-001 | order-fulfillment.ha.feature | 依狀態查看待處理訂單 | 訂單, 訂單狀態 | 訂單, 訂單狀態 |  |  |  |  | medium | docs/ssot/habdd/order-fulfillment.ha.feature |
| SCN-ORDER-002 | order-fulfillment.ha.feature | 標記訂單出貨 | 訂單, 出貨, 物流 | 訂單, 出貨, 物流 |  |  |  |  | medium | docs/ssot/habdd/order-fulfillment.ha.feature |
| SCN-ORDER-003 | order-fulfillment.ha.feature | 消費者追蹤配送進度 | 訂單, 物流 | 訂單, 物流 |  |  |  |  | medium | docs/ssot/habdd/order-fulfillment.ha.feature |
| SCN-ORDER-004 | order-fulfillment.ha.feature | 訂單狀態變更時通知消費者 | 訂單, 通知 | 訂單, 通知 |  |  |  |  | medium | docs/ssot/habdd/order-fulfillment.ha.feature |
| SCN-ORDER-005 | order-fulfillment.ha.feature | 付款逾時與取消規則已裁決 | 訂單, 退款, 庫存 | 訂單, 退款, 庫存 |  |  |  | DEC-CLR-004 | medium | docs/ssot/habdd/order-fulfillment.ha.feature |
| SCN-MEMBER-001 | membership-loyalty.ha.feature | 使用 Email 註冊會員 | 會員, Email | 會員, Email |  |  |  |  | medium | docs/ssot/habdd/membership-loyalty.ha.feature |
| SCN-MEMBER-002 | membership-loyalty.ha.feature | 依消費金額累積點數 | 會員, 點數, 訂單 | 會員, 點數, 訂單 |  |  |  | CiC GAP #003 | low | docs/ssot/habdd/membership-loyalty.ha.feature |
| SCN-MEMBER-003 | membership-loyalty.ha.feature | 使用點數折抵訂單 | 會員, 點數, 訂單 | 會員, 點數, 訂單 |  |  |  | CiC GAP #003 | low | docs/ssot/habdd/membership-loyalty.ha.feature |
| SCN-MEMBER-004 | membership-loyalty.ha.feature | 會員等級符合專屬優惠資格 | 會員, 會員等級, 優惠券 | 會員, 會員等級, 優惠券 |  |  |  | CiC GAP #003 | low | docs/ssot/habdd/membership-loyalty.ha.feature |
| SCN-MEMBER-005 | membership-loyalty.ha.feature | 會員分級與點數生命週期已裁決 | 會員, 會員等級, 點數 | 會員, 會員等級, 點數 |  |  |  | DEC-CLR-003 | medium | docs/ssot/habdd/membership-loyalty.ha.feature |
| SCN-PROMO-001 | promotion-coupon.ha.feature | 建立有檔期的促銷活動 | 促銷活動, 商品, 分類 | 促銷活動, 商品, 分類 |  |  |  |  | medium | docs/ssot/habdd/promotion-coupon.ha.feature |
| SCN-PROMO-002 | promotion-coupon.ha.feature | 建立有限制條件的優惠券 | 優惠券, 會員等級 | 優惠券, 會員等級 |  |  |  |  | medium | docs/ssot/habdd/promotion-coupon.ha.feature |
| SCN-PROMO-003 | promotion-coupon.ha.feature | 一筆訂單最多使用一張優惠券 | 優惠券, 訂單 | 優惠券, 訂單 |  |  |  |  | high | docs/ssot/habdd/promotion-coupon.ha.feature |
| SCN-PROMO-004 | promotion-coupon.ha.feature | 折扣疊加規則已裁決 | 促銷活動, 優惠券, 會員折扣, 點數 | 促銷活動, 優惠券, 會員折扣, 點數 |  |  |  | DEC-CLR-002 | medium | docs/ssot/habdd/promotion-coupon.ha.feature |
| SCN-RETURN-001 | return-refund.ha.feature | 消費者申請退貨 | 訂單, 退貨申請 | 訂單, 退貨申請 |  |  |  | CiC GAP #006 | low | docs/ssot/habdd/return-refund.ha.feature |
| SCN-RETURN-002 | return-refund.ha.feature | 商家核准退貨後安排取件 | 退貨申請, 物流, 退款 | 退貨申請, 物流, 退款 |  |  |  | CiC GAP #006 | low | docs/ssot/habdd/return-refund.ha.feature |
| SCN-RETURN-003 | return-refund.ha.feature | 退回商品確認後完成退款 | 退貨申請, 退款, 訂單 | 退貨申請, 退款, 訂單 |  |  |  | CiC GAP #006 | low | docs/ssot/habdd/return-refund.ha.feature |
| SCN-RETURN-004 | return-refund.ha.feature | 退貨政策已裁決 | 退貨申請, 訂單 | 退貨申請, 訂單 |  |  |  | DEC-CLR-006 | medium | docs/ssot/habdd/return-refund.ha.feature |
| SCN-REPORT-001 | merchant-reporting.ha.feature | 查看指定期間的銷售概況 | 報表, 訂單, 銷售摘要 | 報表, 訂單, 銷售摘要 |  |  |  |  | medium | docs/ssot/habdd/merchant-reporting.ha.feature |
| SCN-REPORT-002 | merchant-reporting.ha.feature | 查看商品銷售排行 | 報表, 商品 | 報表, 商品 |  |  |  |  | medium | docs/ssot/habdd/merchant-reporting.ha.feature |
| SCN-REPORT-003 | merchant-reporting.ha.feature | 無銷售資料時呈現空報表 | 報表, 商家 | 報表, 商家 |  |  |  |  | medium | docs/ssot/habdd/merchant-reporting.ha.feature |
| SCN-AUTH-001 | access-boundary.ha.feature | 商家只能管理自己的商店資料 | 商家, 商品, 訂單 | 商家, 商品, 訂單 |  |  |  |  | medium | docs/ssot/habdd/access-boundary.ha.feature |
| SCN-AUTH-002 | access-boundary.ha.feature | 消費者只能查看自己的訂單 | 消費者, 訂單 | 消費者, 訂單 |  |  |  |  | medium | docs/ssot/habdd/access-boundary.ha.feature |
| SCN-AUTH-003 | access-boundary.ha.feature | 平台管理員管理平台層級資料 | 平台管理員, 商家 | 平台管理員, 商家 |  |  |  |  | medium | docs/ssot/habdd/access-boundary.ha.feature |

| SCN-INV-006 | inventory-control.ha.feature | 依決策建立庫存預留並於付款完成扣減 | SKU, 庫存預留, 訂單 | SKU, 庫存預留, 訂單 | InventoryItem, SalesOrder | InventoryItem, InventoryMovement, SalesOrder | InventoryItem.availableQty, SalesOrder.orderStatus, InventoryMovement.movementType | CON-CLARIFY-001 | high | docs/ssot/habdd/inventory-control.ha.feature |
| SCN-CHECKOUT-006 | checkout-payment.ha.feature | 依決策計算 5% 營業稅 | 訂單, 稅金, 優惠, 運費 | 訂單, 稅金, 優惠, 運費 | SalesOrder, Promotion, Coupon, PointLedger | SalesOrder | SalesOrder.subtotalAmount, SalesOrder.discountAmount, SalesOrder.shippingFee, SalesOrder.taxAmount, SalesOrder.totalAmount | CON-CLARIFY-005 | high | docs/ssot/habdd/checkout-payment.ha.feature |
| SCN-MEMBER-006 | membership-loyalty.ha.feature | MVP 啟用點數並手動維護會員分級 | 會員, 會員等級, 點數 | 會員, 會員等級, 點數 | ConsumerProfile, MemberLevel, PointLedger | PointLedger, ConsumerProfile | ConsumerProfile.memberLevelId, PointLedger.pointType, PointLedger.points | CON-CLARIFY-003 | high | docs/ssot/habdd/membership-loyalty.ha.feature |
| SCN-ORDER-006 | order-fulfillment.ha.feature | 依決策處理付款逾時與出貨前取消 | 訂單, 退款, 庫存 | 訂單, 退款, 庫存 | SalesOrder, Payment, InventoryItem | SalesOrder, Refund, InventoryItem | SalesOrder.orderStatus, Payment.paymentStatus, Refund.refundStatus, InventoryItem.availableQty | CON-CLARIFY-004 | high | docs/ssot/habdd/order-fulfillment.ha.feature |
| SCN-PROMO-005 | promotion-coupon.ha.feature | 依決策計算可疊加折扣 | 促銷活動, 優惠券, 會員折扣, 點數, 訂單 | 促銷活動, 優惠券, 會員折扣, 點數, 訂單 | Promotion, Coupon, MemberLevel, PointLedger, SalesOrder | SalesOrder, CouponRedemption, PointLedger | SalesOrder.discountAmount, CouponRedemption.couponId, PointLedger.points | CON-CLARIFY-002 | high | docs/ssot/habdd/promotion-coupon.ha.feature |
| SCN-RETURN-005 | return-refund.ha.feature | 依決策審核退貨期限與退款路徑 | 退貨申請, 訂單, 退款 | 退貨申請, 訂單, 退款 | ReturnRequest, SalesOrder, Refund | ReturnRequest, Refund | ReturnRequest.returnStatus, Refund.refundStatus, Payment.paymentMethod | CON-CLARIFY-006 | high | docs/ssot/habdd/return-refund.ha.feature |

## L3 Intent Mapping

| scenario_id | haapi_operation | hapdl_page | haarm_permissions | source |
|---|---|---|---|---|
| SCN-CATALOG-001 | product-catalog.create | merchant-product-management | product_crud_merchant | docs/ssot/haapi/product-catalog.haapi.yaml |
| SCN-CATALOG-002 | product-catalog.publish_product | merchant-product-management | product_crud_merchant | docs/ssot/haapi/product-catalog.haapi.yaml |
| SCN-CATALOG-003 | product-catalog.update | merchant-product-management | product_crud_merchant | docs/ssot/haapi/product-catalog.haapi.yaml |
| SCN-DISC-001 | product-catalog.list | public-product-list | product_read_public, category_read_public | docs/ssot/hapdl/public-product-list.hapdl.yaml |
| SCN-DISC-003 | cart-checkout.add_cart_item | consumer-cart-checkout | cart_item_crud_own | docs/ssot/haapi/cart-checkout.haapi.yaml |
| SCN-INV-001 | inventory.adjust_inventory | inventory-dashboard | inventory_item_crud_merchant | docs/ssot/haapi/inventory.haapi.yaml |
| SCN-INV-005 | inventory.reserve_inventory | consumer-cart-checkout | system_inventory_adjust | docs/ssot/haapi/inventory.haapi.yaml |
| SCN-CHECKOUT-001 | cart-checkout.calculate_checkout | consumer-cart-checkout | cart_crud_own | docs/ssot/haapi/cart-checkout.haapi.yaml |
| SCN-CHECKOUT-002 | payment-refund.provider_payment_update | consumer-order-history | payment_provider_update | docs/ssot/haapi/payment-refund.haapi.yaml |
| SCN-CHECKOUT-005 | cart-checkout.calculate_checkout | consumer-cart-checkout | sales_order_create_own | docs/ssot/haapi/cart-checkout.haapi.yaml |
| SCN-ORDER-001 | sales-order.list | merchant-order-list | sales_order_read_merchant | docs/ssot/hapdl/merchant-order-list.hapdl.yaml |
| SCN-ORDER-002 | sales-order.mark_shipped | merchant-order-list | shipment_crud_merchant | docs/ssot/haapi/sales-order.haapi.yaml |
| SCN-ORDER-005 | sales-order.cancel_unpaid_order | merchant-order-list | system_order_process | docs/ssot/haapi/sales-order.haapi.yaml |
| SCN-MEMBER-002 | loyalty.create | consumer-order-history | system_order_process | docs/ssot/haapi/loyalty.haapi.yaml |
| SCN-MEMBER-003 | loyalty.redeem_points | consumer-cart-checkout | point_ledger_read_own | docs/ssot/haapi/loyalty.haapi.yaml |
| SCN-MEMBER-005 | loyalty.adjust_member_level | promotion-coupon-management | member_level_admin | docs/ssot/haapi/loyalty.haapi.yaml |
| SCN-PROMO-001 | promotion-coupon.create | promotion-coupon-management | promotion_crud_merchant | docs/ssot/haapi/promotion-coupon.haapi.yaml |
| SCN-PROMO-004 | promotion-coupon.calculate_discount_stack | consumer-cart-checkout | sales_order_create_own | docs/ssot/haapi/promotion-coupon.haapi.yaml |
| SCN-RETURN-001 | return-refund.create | return-refund-workbench | return_request_create_own | docs/ssot/haapi/return-refund.haapi.yaml |
| SCN-RETURN-002 | return-refund.approve_return | return-refund-workbench | return_request_update_merchant | docs/ssot/haapi/return-refund.haapi.yaml |
| SCN-RETURN-003 | return-refund.complete_original_refund | return-refund-workbench | refund_provider_update | docs/ssot/haapi/return-refund.haapi.yaml |
| SCN-REPORT-001 | merchant-report.sales_summary | merchant-report-dashboard | merchant_report_read | docs/ssot/hapdl/merchant-report-dashboard.hapdl.yaml |
| SCN-REPORT-002 | merchant-report.product_performance | merchant-report-dashboard | merchant_report_read | docs/ssot/hapdl/merchant-report-dashboard.hapdl.yaml |
| SCN-AUTH-001 | sales-order.list | merchant-order-list | sales_order_read_merchant | docs/ssot/haarm/smallbiz.haarm.yaml#CON-AUTH-001 |
| SCN-AUTH-002 | sales-order.list | consumer-order-history | sales_order_read_own | docs/ssot/haarm/smallbiz.haarm.yaml#CON-AUTH-002 |

| SCN-AUTH-003 | platform-admin.review_merchant_boundary | platform-admin-access | account_admin, merchant_admin | docs/ssot/haapi/platform-admin.haapi.yaml |
| SCN-CATALOG-004 | product-catalog.deactivate_product | merchant-product-management | product_crud_merchant | docs/ssot/haapi/product-catalog.haapi.yaml |
| SCN-CHECKOUT-003 | cart-checkout.calculate_checkout | consumer-cart-checkout | sales_order_create_own | docs/ssot/haapi/cart-checkout.haapi.yaml |
| SCN-CHECKOUT-004 | promotion-coupon.validate_coupon | consumer-cart-checkout | sales_order_create_own | docs/ssot/haapi/promotion-coupon.haapi.yaml |
| SCN-CHECKOUT-006 | cart-checkout.calculate_checkout | consumer-cart-checkout | sales_order_create_own | docs/ssot/haapi/cart-checkout.haapi.yaml |
| SCN-DISC-002 | product-catalog.list | public-product-list | product_read_public | docs/ssot/hapdl/public-product-list.hapdl.yaml |
| SCN-DISC-004 | product-catalog.read | public-product-list | product_read_public | docs/ssot/hapdl/public-product-list.hapdl.yaml |
| SCN-INV-002 | inventory.reserve_inventory | consumer-cart-checkout | system_inventory_adjust | docs/ssot/haapi/inventory.haapi.yaml |
| SCN-INV-003 | inventory.adjust_inventory | inventory-dashboard | inventory_item_crud_merchant | docs/ssot/haapi/inventory.haapi.yaml |
| SCN-INV-004 | cart-checkout.create_order | consumer-cart-checkout | sales_order_create_own | docs/ssot/haapi/cart-checkout.haapi.yaml |
| SCN-INV-006 | inventory.reserve_inventory | consumer-cart-checkout | system_inventory_adjust | docs/ssot/haapi/inventory.haapi.yaml |
| SCN-MEMBER-001 | member-account.register_with_email | member-registration | consumer_profile_update_own | docs/ssot/haapi/member-account.haapi.yaml |
| SCN-MEMBER-004 | promotion-coupon.validate_coupon | consumer-cart-checkout | sales_order_create_own | docs/ssot/haapi/promotion-coupon.haapi.yaml |
| SCN-MEMBER-006 | loyalty.create | consumer-order-history | system_order_process | docs/ssot/haapi/loyalty.haapi.yaml |
| SCN-ORDER-003 | sales-order.read | consumer-order-history | sales_order_read_own | docs/ssot/hapdl/consumer-order-history.hapdl.yaml |
| SCN-ORDER-006 | sales-order.cancel_unpaid_order | consumer-order-history | system_order_process | docs/ssot/haapi/sales-order.haapi.yaml |
| SCN-PROMO-002 | promotion-coupon.create | promotion-coupon-management | promotion_crud_merchant | docs/ssot/haapi/promotion-coupon.haapi.yaml |
| SCN-PROMO-003 | promotion-coupon.validate_coupon | consumer-cart-checkout | sales_order_create_own | docs/ssot/haapi/promotion-coupon.haapi.yaml |
| SCN-PROMO-005 | promotion-coupon.calculate_discount_stack | consumer-cart-checkout | sales_order_create_own | docs/ssot/haapi/promotion-coupon.haapi.yaml |
| SCN-REPORT-003 | merchant-report.sales_summary | merchant-report-dashboard | merchant_report_read | docs/ssot/haapi/merchant-report.haapi.yaml |
| SCN-RETURN-004 | return-refund.create | return-refund-workbench | return_request_create_own | docs/ssot/haapi/return-refund.haapi.yaml |
| SCN-RETURN-005 | return-refund.create | return-refund-workbench | return_request_create_own | docs/ssot/haapi/return-refund.haapi.yaml |

## Decision Traceability

| decision_id | cic_id | status | affected_artifacts | summary |
|---|---|---|---|---|
| DEC-CLR-001 | CiC-GAP-001 | applied | `docs/ssot/dbml/constraints.md`, `docs/ssot/habdd/inventory-control.ha.feature`, `docs/ssot/habdd/order-fulfillment.ha.feature` | 下單成立時建立庫存預留，付款完成時正式扣減；未付款訂單逾時取消時釋放預留庫存。 |
| DEC-CLR-002 | CiC-GAP-002 | applied | `docs/ssot/dbml/constraints.md`, `docs/ssot/habdd/promotion-coupon.ha.feature`, `docs/ssot/habdd/checkout-payment.ha.feature` | 活動價可與優惠券或會員折扣擇一疊加；優惠券與會員折扣互斥；點數最後折抵。 |
| DEC-CLR-003 | CiC-GAP-003 | applied | `docs/ssot/dbml/constraints.md`, `docs/ssot/dbml/seeds.md`, `docs/ssot/habdd/membership-loyalty.ha.feature` | MVP 啟用點數累積與折抵；會員分級固定手動維護；自動升降級排程延後。 |
| DEC-CLR-004 | CiC-GAP-004 | applied | `docs/ssot/dbml/constraints.md`, `docs/ssot/dbml/seeds.md`, `docs/ssot/habdd/order-fulfillment.ha.feature` | 未付款訂單保留 30 分鐘後自動取消；已付款訂單出貨前可取消並原路退款。 |
| DEC-CLR-005 | CiC-GAP-005 | applied | `docs/ssot/dbml/constraints.md`, `docs/ssot/dbml/glossary.md`, `docs/ssot/habdd/checkout-payment.ha.feature` | 5% 營業稅稅基為扣除折扣與點數後的商品金額，不含運費。 |
| DEC-CLR-006 | CiC-GAP-006 | applied | `docs/ssot/dbml/constraints.md`, `docs/ssot/dbml/seeds.md`, `docs/ssot/habdd/return-refund.ha.feature` | 到貨後 7 天內可退；已拆封、個人化商品、耗材不可退；退款必須原路退回。 |
