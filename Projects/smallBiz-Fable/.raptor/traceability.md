# Traceability

> 建立：2026-06-12（rapt-behavior，L1 + L2 草稿）
> Schema：rapt-core::traceability-schema.md
> 註：read_tables / write_tables / fields 留待 rapt-modeling / rapt-intent 精確化，不以猜測填入。

## L1 Requirement Coverage

| req_or_story | source | feature | scenario_count | status | notes |
|---|---|---|---:|---|---|
| US-001 | docs/discovery/02-user-journeys.md | member-account.ha.feature | 4 | covered | |
| US-002 | docs/discovery/02-user-journeys.md | product-browsing.ha.feature | 3 | covered | |
| US-003 | docs/discovery/02-user-journeys.md | shopping-cart.ha.feature | 4 | covered | |
| US-004 | docs/discovery/02-user-journeys.md | checkout-order.ha.feature | 4 | covered | 扣庫存時點依 PRD 2.1，細則 GAP #006 |
| US-005 | docs/discovery/02-user-journeys.md | payment-invoice.ha.feature | 5 | covered | 付款期限值 GAP #006 |
| US-006 | docs/discovery/02-user-journeys.md | order-tracking.ha.feature | 3 | covered | |
| US-007 | docs/discovery/02-user-journeys.md | loyalty-points.ha.feature | 3 | covered | 折抵上限/效期/回饋基準 GAP #010 |
| US-008 | docs/discovery/02-user-journeys.md | returns.ha.feature | 5 | covered | 期限/排除品項/退款路徑 GAP #011 |
| US-009 | docs/discovery/02-user-journeys.md | merchant-onboarding.ha.feature | 3 | covered | 與 US-017 共用 feature |
| US-010 | docs/discovery/02-user-journeys.md | product-management.ha.feature | 5 | covered | |
| US-011 | docs/discovery/02-user-journeys.md | inventory-management.ha.feature | 4 | covered | 防超賣機制 GAP #006 |
| US-012 | docs/discovery/02-user-journeys.md | order-fulfillment.ha.feature | 4 | covered | 狀態機觸發者 ASM #008 |
| US-013 | docs/discovery/02-user-journeys.md | returns.ha.feature | 5 | covered | 與 US-008 共用 feature |
| US-014 | docs/discovery/02-user-journeys.md | merchant-reporting.ha.feature | 2 | covered | |
| US-015 | docs/discovery/02-user-journeys.md | promotion-campaign.ha.feature | 4 | covered | 疊加順序 GAP #007 |
| US-016 | docs/discovery/02-user-journeys.md | coupon.ha.feature | 6 | covered | |
| US-017 | docs/discovery/02-user-journeys.md | merchant-onboarding.ha.feature | 3 | covered | 平台功能範圍 GAP #005 |
| US-018 | docs/discovery/04-vision-kpi-scope.md（PRD 5.2） | member-tier.ha.feature | 4 | covered | F-017；門檻金額 deferred-needs-decision（CON-MBR-003），以規則層變數承接 |
| US-019 | docs/discovery/04-vision-kpi-scope.md（訪談 2） | wishlist.ha.feature | 4 | covered | F-016；入 MVP（CON-WSH-001） |
| US-020 | docs/discovery/04-vision-kpi-scope.md（PRD 2.4） | — | 0 | deferred-mvp-out | 多倉庫，未來版本 |
| US-021 | docs/discovery/04-vision-kpi-scope.md | — | 0 | deferred-mvp-out | GAP #009 RESOLVED：月租計費不入 MVP，人工/外部處理 |

## L2 Scenario Data Mapping

| scenario_id | feature | scenario | entities | glossary_terms | read_tables | write_tables | fields | constraints | confidence | source |
|---|---|---|---|---|---|---|---|---|---|---|
| SCN-MEMBER-001 | member-account.ha.feature | 以 Email 成功註冊會員 | 會員 | | | | | | medium | docs/ssot/habdd/member-account.ha.feature |
| SCN-MEMBER-002 | member-account.ha.feature | 完成信箱驗證後會員生效 | 會員 | | | | | | medium | docs/ssot/habdd/member-account.ha.feature |
| SCN-MEMBER-003 | member-account.ha.feature | 重複 Email 註冊被拒絕 | 會員 | | | | | | medium | docs/ssot/habdd/member-account.ha.feature |
| SCN-MEMBER-004 | member-account.ha.feature | 儲存常用收件地址 | 會員, 收件地址 | | | | | | medium | docs/ssot/habdd/member-account.ha.feature |
| SCN-CART-001 | shopping-cart.ha.feature | 將上架商品加入購物車 | 購物車, 商品 | | | | | | medium | docs/ssot/habdd/shopping-cart.ha.feature |
| SCN-CART-002 | shopping-cart.ha.feature | 調整購物車內商品數量 | 購物車 | | | | | | medium | docs/ssot/habdd/shopping-cart.ha.feature |
| SCN-CART-003 | shopping-cart.ha.feature | 購物車跨裝置保留 | 購物車 | | | | | | medium | docs/ssot/habdd/shopping-cart.ha.feature |
| SCN-CART-004 | shopping-cart.ha.feature | 已下架商品無法加入購物車 | 購物車, 商品 | | | | | | medium | docs/ssot/habdd/shopping-cart.ha.feature |
| SCN-CHECKOUT-001 | checkout-order.ha.feature | 成功提交訂單 | 訂單, 商品快照, 庫存 | | | | | | medium | docs/ssot/habdd/checkout-order.ha.feature |
| SCN-CHECKOUT-002 | checkout-order.ha.feature | 依滿額門檻計算運費 | 訂單 | | | | | | medium | docs/ssot/habdd/checkout-order.ha.feature |
| SCN-CHECKOUT-003 | checkout-order.ha.feature | 訂單金額自動含稅 | 訂單, 發票 | | | | | | low | docs/ssot/habdd/checkout-order.ha.feature |
| SCN-CHECKOUT-004 | checkout-order.ha.feature | 庫存不足時訂單不成立 | 訂單, 庫存 | | | | | | medium | docs/ssot/habdd/checkout-order.ha.feature |
| SCN-PAY-001 | payment-invoice.ha.feature | 信用卡付款成功 | 訂單, 付款 | | | | | | medium | docs/ssot/habdd/payment-invoice.ha.feature |
| SCN-PAY-002 | payment-invoice.ha.feature | 付款失敗時訂單保留待付款 | 訂單, 付款 | | | | | | medium | docs/ssot/habdd/payment-invoice.ha.feature |
| SCN-PAY-003 | payment-invoice.ha.feature | 銀行轉帳以後五碼對帳 | 訂單, 付款 | | | | | | medium | docs/ssot/habdd/payment-invoice.ha.feature |
| SCN-PAY-004 | payment-invoice.ha.feature | 逾時未付款訂單自動取消 | 訂單, 庫存 | | | | | | low | docs/ssot/habdd/payment-invoice.ha.feature |
| SCN-PAY-005 | payment-invoice.ha.feature | 付款完成後開立發票 | 訂單, 發票 | | | | | | medium | docs/ssot/habdd/payment-invoice.ha.feature |
| SCN-TRACK-001 | order-tracking.ha.feature | 訂單狀態變更時收到通知 | 訂單, 通知 | | | | | | medium | docs/ssot/habdd/order-tracking.ha.feature |
| SCN-TRACK-002 | order-tracking.ha.feature | 查詢訂單物流進度 | 訂單, 物流單 | | | | | | medium | docs/ssot/habdd/order-tracking.ha.feature |
| SCN-TRACK-003 | order-tracking.ha.feature | 無法查詢他人的訂單 | 訂單, 會員 | | | | | | medium | docs/ssot/habdd/order-tracking.ha.feature |
| SCN-ONBOARD-001 | merchant-onboarding.ha.feature | 商家註冊開店申請 | 商家, 店面 | | | | | | medium | docs/ssot/habdd/merchant-onboarding.ha.feature |
| SCN-ONBOARD-002 | merchant-onboarding.ha.feature | 平台開通商家店面 | 商家, 店面 | | | | | | low | docs/ssot/habdd/merchant-onboarding.ha.feature |
| SCN-ONBOARD-003 | merchant-onboarding.ha.feature | 平台停權違規商家 | 商家, 店面 | | | | | | medium | docs/ssot/habdd/merchant-onboarding.ha.feature |
| SCN-PRODUCT-001 | product-management.ha.feature | 建立商品並儲存為草稿 | 商品 | | | | | | medium | docs/ssot/habdd/product-management.ha.feature |
| SCN-PRODUCT-002 | product-management.ha.feature | 設定規格組合與 SKU | 商品, SKU | | | | | | medium | docs/ssot/habdd/product-management.ha.feature |
| SCN-PRODUCT-003 | product-management.ha.feature | 售價為零的 SKU 設定被拒絕 | SKU | | | | | | medium | docs/ssot/habdd/product-management.ha.feature |
| SCN-PRODUCT-004 | product-management.ha.feature | 上架商品 | 商品 | | | | | | medium | docs/ssot/habdd/product-management.ha.feature |
| SCN-PRODUCT-005 | product-management.ha.feature | 下架商品不影響既有訂單 | 商品, 訂單 | | | | | | medium | docs/ssot/habdd/product-management.ha.feature |
| SCN-STOCK-001 | inventory-management.ha.feature | 設定 SKU 庫存量 | 庫存, SKU | | | | | | medium | docs/ssot/habdd/inventory-management.ha.feature |
| SCN-STOCK-002 | inventory-management.ha.feature | 訂單成立時自動扣減庫存 | 庫存, 訂單 | | | | | | medium | docs/ssot/habdd/inventory-management.ha.feature |
| SCN-STOCK-003 | inventory-management.ha.feature | 低於水位時通知補貨 | 庫存, 通知 | | | | | | medium | docs/ssot/habdd/inventory-management.ha.feature |
| SCN-STOCK-004 | inventory-management.ha.feature | 最後一件商品不被超賣 | 庫存, 訂單 | | | | | | low | docs/ssot/habdd/inventory-management.ha.feature |
| SCN-FULFILL-001 | order-fulfillment.ha.feature | 依狀態篩選訂單 | 訂單 | | | | | | medium | docs/ssot/habdd/order-fulfillment.ha.feature |
| SCN-FULFILL-002 | order-fulfillment.ha.feature | 商家確認已付款訂單 | 訂單 | | | | | | low | docs/ssot/habdd/order-fulfillment.ha.feature |
| SCN-FULFILL-003 | order-fulfillment.ha.feature | 標記出貨並填入物流單號 | 訂單, 物流單 | | | | | | medium | docs/ssot/habdd/order-fulfillment.ha.feature |
| SCN-FULFILL-004 | order-fulfillment.ha.feature | 無法查看其他商家的訂單 | 訂單, 商家 | | | | | | medium | docs/ssot/habdd/order-fulfillment.ha.feature |
| SCN-RETURN-001 | returns.ha.feature | 線上申請退貨 | 退貨申請, 訂單 | | | | | | low | docs/ssot/habdd/returns.ha.feature |
| SCN-RETURN-002 | returns.ha.feature | 商家核准退貨並安排取件 | 退貨申請, 物流單 | | | | | | medium | docs/ssot/habdd/returns.ha.feature |
| SCN-RETURN-003 | returns.ha.feature | 商家拒絕退貨申請 | 退貨申請 | | | | | | medium | docs/ssot/habdd/returns.ha.feature |
| SCN-RETURN-004 | returns.ha.feature | 確認退回商品後退款 | 訂單, 退款 | | | | | | low | docs/ssot/habdd/returns.ha.feature |
| SCN-RETURN-005 | returns.ha.feature | 超過退貨期限的申請不成立 | 退貨申請 | | | | | | low | docs/ssot/habdd/returns.ha.feature |
| SCN-POINT-001 | loyalty-points.ha.feature | 訂單完成後獲得消費點數 | 點數, 訂單 | | | | | | low | docs/ssot/habdd/loyalty-points.ha.feature |
| SCN-POINT-002 | loyalty-points.ha.feature | 結帳時折抵點數 | 點數, 訂單 | | | | | | low | docs/ssot/habdd/loyalty-points.ha.feature |
| SCN-POINT-003 | loyalty-points.ha.feature | 折抵超過餘額的點數被拒絕 | 點數 | | | | | | medium | docs/ssot/habdd/loyalty-points.ha.feature |
| SCN-PROMO-001 | promotion-campaign.ha.feature | 建立有檔期的促銷活動 | 促銷活動 | | | | | | medium | docs/ssot/habdd/promotion-campaign.ha.feature |
| SCN-PROMO-002 | promotion-campaign.ha.feature | 檔期開始時活動自動生效 | 促銷活動 | | | | | | medium | docs/ssot/habdd/promotion-campaign.ha.feature |
| SCN-PROMO-003 | promotion-campaign.ha.feature | 檔期結束時活動自動失效 | 促銷活動 | | | | | | medium | docs/ssot/habdd/promotion-campaign.ha.feature |
| SCN-PROMO-004 | promotion-campaign.ha.feature | 依活動類型套用優惠 | 促銷活動, 訂單 | | | | | | low | docs/ssot/habdd/promotion-campaign.ha.feature |
| SCN-COUPON-001 | coupon.ha.feature | 發行優惠券 | 優惠券 | | | | | | medium | docs/ssot/habdd/coupon.ha.feature |
| SCN-COUPON-002 | coupon.ha.feature | 達門檻訂單成功套用優惠券 | 優惠券, 訂單 | | | | | | medium | docs/ssot/habdd/coupon.ha.feature |
| SCN-COUPON-003 | coupon.ha.feature | 未達最低消費門檻無法套用 | 優惠券, 訂單 | | | | | | medium | docs/ssot/habdd/coupon.ha.feature |
| SCN-COUPON-004 | coupon.ha.feature | 一筆訂單最多使用一張優惠券 | 優惠券, 訂單 | | | | | | high | docs/ssot/habdd/coupon.ha.feature |
| SCN-COUPON-005 | coupon.ha.feature | 總使用張數達上限後無法套用 | 優惠券 | | | | | | medium | docs/ssot/habdd/coupon.ha.feature |
| SCN-COUPON-006 | coupon.ha.feature | 等級限定券拒絕不符資格的會員 | 優惠券, 會員 | | | | | | low | docs/ssot/habdd/coupon.ha.feature |
| SCN-REPORT-001 | merchant-reporting.ha.feature | 查看期間銷售概況 | 訂單 | | | | | | medium | docs/ssot/habdd/merchant-reporting.ha.feature |
| SCN-REPORT-002 | merchant-reporting.ha.feature | 查看商品排行 | 商品, 訂單 | | | | | | medium | docs/ssot/habdd/merchant-reporting.ha.feature |
| SCN-WISH-001 | wishlist.ha.feature | 將商品加入願望清單 | 願望清單, 商品 | 願望清單, 商品 | Product | Wishlist | Wishlist.memberId, Wishlist.productId | CON-WSH-001 | high | docs/ssot/habdd/wishlist.ha.feature |
| SCN-WISH-002 | wishlist.ha.feature | 收藏商品降價時收到通知 | 願望清單, 通知 | 願望清單, 通知 | Wishlist, ProductVariant | NotificationLog | | CON-WSH-001 | medium | docs/ssot/habdd/wishlist.ha.feature |
| SCN-WISH-003 | wishlist.ha.feature | 從願望清單移除商品 | 願望清單 | 願望清單 | | Wishlist | | | high | docs/ssot/habdd/wishlist.ha.feature |
| SCN-WISH-004 | wishlist.ha.feature | 重複收藏同一商品不重複建立 | 願望清單, 商品 | 願望清單 | Wishlist | Wishlist | | | high | docs/ssot/habdd/wishlist.ha.feature |
| SCN-TIER-001 | member-tier.ha.feature | 近一年累計消費達門檻時升級 | 會員, 會員等級 | 會員 | Order | Member | Member.tierCode | CON-MBR-003 | medium | docs/ssot/habdd/member-tier.ha.feature |
| SCN-TIER-002 | member-tier.ha.feature | 累計消費未達門檻時維持原等級 | 會員, 會員等級 | 會員 | Order | Member | Member.tierCode | CON-MBR-003 | medium | docs/ssot/habdd/member-tier.ha.feature |
| SCN-TIER-003 | member-tier.ha.feature | 累計消費下滑時降級 | 會員, 會員等級 | 會員 | Order | Member | Member.tierCode | CON-MBR-003 | medium | docs/ssot/habdd/member-tier.ha.feature |
| SCN-TIER-004 | member-tier.ha.feature | 升級後可使用等級限定優惠券 | 會員, 會員等級, 優惠券 | 會員, 優惠券 | Coupon, Member | | Coupon.tierLimit, Member.tierCode | CON-CPN-003 | medium | docs/ssot/habdd/member-tier.ha.feature |

> confidence 標記原則：涉及未決 CiC（GAP #006/#007/#010/#011 等）的 scenario 標 low；其餘 medium；有明文共識者（一單一券）標 high。
> 純讀取且無資料變更/授權/狀態轉換的 scenario（SCN-BROWSE 類）未標 entities，未列入 L2：product-browsing.ha.feature 的 3 個 scenario、SCN-FULFILL-001/SCN-REPORT 類為讀取型，其中已標 entities 者仍列入以供測試資料準備。
> **Phase 3 信心修正（2026-06-13）**：原因 GAP #006/#007/#010/#011 及 ASM #008 已解決，下列原標 low 的 scenario 升為 medium：SCN-CHECKOUT-001/003、SCN-PAY-004、SCN-STOCK-004、SCN-RETURN-001/004/005、SCN-POINT-001/002、SCN-FULFILL-002、SCN-PROMO-004、SCN-COUPON-006。對應精確 table/field 由 rapt-intent 補全。

## L3 Intent Mapping

> 由 rapt-intent 維護（Phase 4，2026-06-13）。Scenario → haAPI operation / haPDL page / haARM permission。

| scenario_id | haapi_operation | hapdl_page | haarm_permissions | source |
|---|---|---|---|---|
| SCN-MEMBER-001 | member.create | member-form | member_create | docs/ssot/haapi/member.haapi.yaml |
| SCN-MEMBER-002 | member.verify_email | member-form | (public) | docs/ssot/haapi/member.haapi.yaml |
| SCN-MEMBER-004 | member.update | member-form | member_address_create_own | docs/ssot/haapi/member.haapi.yaml |
| SCN-CART-001 | cart.add_item | cart-detail | cart_item_create_own | docs/ssot/haapi/cart.haapi.yaml |
| SCN-CART-004 | cart.add_item | cart-detail | cart_item_create_own | docs/ssot/haapi/cart.haapi.yaml |
| SCN-CHECKOUT-001 | order.create | order-form | order_create_own | docs/ssot/haapi/order.haapi.yaml |
| SCN-CHECKOUT-003 | order.create | order-form | order_create_own | docs/ssot/haapi/order.haapi.yaml |
| SCN-PAY-001 | order.apply_payment | order-detail | payment_create_own | docs/ssot/haapi/order.haapi.yaml |
| SCN-PAY-004 | order.cancel | order-detail | order_update_store | docs/ssot/haapi/order.haapi.yaml |
| SCN-TRACK-002 | shipment.read | order-detail | shipment_read_store | docs/ssot/haapi/shipment.haapi.yaml |
| SCN-TRACK-003 | order.read | order-detail | order_read_own | docs/ssot/haapi/order.haapi.yaml |
| SCN-ONBOARD-001 | merchant.create | merchant-form | (public) | docs/ssot/haapi/merchant.haapi.yaml |
| SCN-ONBOARD-002 | merchant.activate | merchant-list | merchant_update_status | docs/ssot/haapi/merchant.haapi.yaml |
| SCN-ONBOARD-003 | merchant.suspend | merchant-list | merchant_update_status | docs/ssot/haapi/merchant.haapi.yaml |
| SCN-PRODUCT-001 | product.create | product-form | product_create_store | docs/ssot/haapi/product.haapi.yaml |
| SCN-PRODUCT-004 | product.publish | product-list | product_update_store | docs/ssot/haapi/product.haapi.yaml |
| SCN-STOCK-001 | stock-item.update | stock-item-form | stock_item_update_store | docs/ssot/haapi/stock-item.haapi.yaml |
| SCN-STOCK-004 | order.create | order-form | order_create_own | docs/ssot/haapi/order.haapi.yaml |
| SCN-FULFILL-002 | order.confirm | order-list | order_update_store | docs/ssot/haapi/order.haapi.yaml |
| SCN-FULFILL-003 | shipment.create | shipment-form | shipment_create_store | docs/ssot/haapi/shipment.haapi.yaml |
| SCN-FULFILL-004 | order.list | order-list | order_list_store | docs/ssot/haapi/order.haapi.yaml |
| SCN-RETURN-001 | return-request.create | return-request-form | return_request_create_own | docs/ssot/haapi/return-request.haapi.yaml |
| SCN-RETURN-002 | return-request.approve | return-request-list | return_request_update_store | docs/ssot/haapi/return-request.haapi.yaml |
| SCN-RETURN-004 | return-request.refund | return-request-list | refund_create_store | docs/ssot/haapi/return-request.haapi.yaml |
| SCN-POINT-001 | point-ledger.list | point-ledger-list | point_ledger_read_own | docs/ssot/haapi/point-ledger.haapi.yaml |
| SCN-POINT-002 | order.create | order-form | order_create_own | docs/ssot/haapi/order.haapi.yaml |
| SCN-PROMO-001 | campaign.create | campaign-form | campaign_create_store | docs/ssot/haapi/campaign.haapi.yaml |
| SCN-PROMO-002 | campaign.update | campaign-list | campaign_update_store | docs/ssot/haapi/campaign.haapi.yaml |
| SCN-COUPON-001 | coupon.create | coupon-form | coupon_create_store | docs/ssot/haapi/coupon.haapi.yaml |
| SCN-COUPON-002 | coupon.redeem | order-form | coupon_redemption_create_own | docs/ssot/haapi/coupon.haapi.yaml |
| SCN-COUPON-006 | coupon.redeem | order-form | coupon_redemption_create_own | docs/ssot/haapi/coupon.haapi.yaml |
| US-019（wishlist） | wishlist.create | wishlist-list | wishlist_create_own | docs/ssot/haapi/wishlist.haapi.yaml |
| SCN-PRODUCT-002 | product-variant.create | product-variant-form | product_variant_create_store | docs/ssot/haapi/product-variant.haapi.yaml |
| SCN-PRODUCT-003 | product-variant.create | product-variant-form | product_variant_create_store | docs/ssot/haapi/product-variant.haapi.yaml |
| SCN-MEMBER-004 | member-address.create | member-address-form | member_address_create_own | docs/ssot/haapi/member-address.haapi.yaml |
| SCN-TRACK-001 | notification-log.list | notification-log-list | notification_list_own | docs/ssot/haapi/notification-log.haapi.yaml |
| SCN-REPORT-001 | merchant-report.sales_summary | merchant-report-dashboard | merchant_report_read | docs/ssot/haapi/merchant-report.haapi.yaml |
| SCN-REPORT-002 | merchant-report.product_ranking | merchant-report-dashboard | merchant_report_read | docs/ssot/haapi/merchant-report.haapi.yaml |
| SCN-ONBOARD-001（store） | store.update | store-form | store_update_own | docs/ssot/haapi/store.haapi.yaml |
| ASM#004（operator） | merchant-operator.create | merchant-operator-form | operator_create_store | docs/ssot/haapi/merchant-operator.haapi.yaml |
| GAP#013（audit） | audit-log.list | audit-log-list | audit_log_read_store, audit_log_read_all | docs/ssot/haapi/audit-log.haapi.yaml |

> L2 精確 table 對應：haAPI `entity:` 已綁定 DBML Table（case-sensitive），各 scenario 的 read/write_tables 可由對應 haAPI entity 推導；報表（SCN-REPORT）對應 merchant_report view（本輪未產 haAPI，讀 Order/OrderItem）。

## Decision Traceability

| decision_id | cic_id | status | affected_artifacts | summary |
|---|---|---|---|---|
| CLR-260613-01#Q1 | GAP #006 | applied | dbml/schema.dbml(StockItem), constraints.md(CON-STK-001/003, CON-ORD-002) | 下單即預留+逾時釋放；付款期限 72h；StockItem 加 reservedQuantity |
| CLR-260613-01#Q2 | GAP #007 | applied | constraints.md(CON-ORD-006/008) | 計算順序 活動→券→點數→運費→稅；稅基折後不含運 |
| CLR-260613-01#Q3 | GAP #011 | applied | constraints.md(CON-RTN-001, CON-ORD-011, CON-CPN-004) | 退貨 7 天、原路退款、未出貨可取消、券退還 |
| CLR-260613-01#Q4 | GAP #010 | applied | seeds.md(MemberTier), dbml(PointLedger.expireAt), constraints.md(CON-MBR-003, CON-PNT-003/004/005) | 四級依12月累計消費；點數效期1年、上限50%、折後實付回饋；門檻待平台提案 |
| CLR-260613-02#Q1 | GAP #005 | applied | discovery/02-user-journeys.md | 平台後台僅開通/停權+商家清單；完整審核流程 deferred-mvp-out |
| CLR-260613-02#Q2 | GAP #009 | applied | traceability(US-021), discovery/04 | 月租計費 deferred-mvp-out |
| CLR-260613-02#Q3 | GAP #013 | applied | dbml(AuditLog), seeds.md(AuditAction/ActorType), haarm(audit_log), constraints.md(CON-AUD-001) | 新增 AuditLog 通用稽核 |
| CLR-260613-03#GAP#012 | GAP #012 | applied | constraints.md(CON-SHP-001) | 不支援部分出貨；一單整單出貨 |
| CLR-260613-03#GAP#002 | GAP #002 | applied | dbml(Wishlist), haarm(wishlist), constraints.md(CON-WSH-001), traceability(US-019) | 願望清單入 MVP（accepted scope-add） |
| CLR-260613-03#ASM#003 | ASM #003/#001 | confirmed | seeds.md(PlatformRole), discovery/01 | 平台拆 admin/marketer 兩角色 |
| CLR-260613-03#ASM#004 | ASM #004 | rejected | dbml(MerchantOperator), haarm(merchant_operator), constraints.md(CON-MOP-001) | 拒絕「一商家一帳號」→ 支援一店多操作帳號（scope-add） |
| CLR-260613-03#ASM#008 | ASM #008 | confirmed | constraints.md(CON-ORD-001) | 訂單狀態機觸發者邊界確認 |
| CLR-260613-03#ASM#014 | ASM #014 | confirmed | dbml(ProductVariant) | 原價設於 SKU 層級 |
