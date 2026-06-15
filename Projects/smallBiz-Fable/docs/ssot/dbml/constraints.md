# Domain Constraints

> DBML 欄位型別 / seeds.md 無法完整表示的業務規則 catalog（rapt-modeling）。
> `constraint_id` 穩定可被 traceability / haAPI / RAscore 引用。
> `enforcement`：haAPI | haARM | manual | generated-test | unknown。
> 規則尚未確認者建立 CiC，不假設。

| constraint_id | type | owner_table | owner_field | rule | source | related_scenarios | enforcement |
|---|---|---|---|---|---|---|---|
| CON-MER-003 | state-sync | Store | status | 店面營運狀態須與所屬商家帳號狀態同步：商家停權→店面暫停營運、前台商品隱藏 | SCN-ONBOARD-003 | SCN-ONBOARD-002, SCN-ONBOARD-003 | haAPI |
| CON-PRD-001 | value-check | ProductVariant | price | SKU 售價必須大於 0，售價為 0 不被接受 | SCN-PRODUCT-003 | SCN-PRODUCT-003 | haAPI |
| CON-PRD-002 | precondition | Product | status | 上架前提：商品資料完整且至少有一個有效 SKU（isActive=1） | SCN-PRODUCT-004 | SCN-PRODUCT-004 | haAPI |
| CON-PRD-003 | ref-delete | ProductVariant | variantId | 已被 OrderItem 引用的 SKU 不可實體刪除；下架以 isActive=0 表示 | SCN-PRODUCT-005 | SCN-PRODUCT-005 | haAPI |
| CON-PRD-004 | state-transition | Product | status | 商品狀態轉換：草稿(D)→上架(A)→下架(X)；下架後可重新上架(X→A) | SCN-PRODUCT-001/004/005 | SCN-PRODUCT-001, SCN-PRODUCT-004, SCN-PRODUCT-005 | haAPI |
| CON-STK-001 | value-check | StockItem | quantity, reservedQuantity | 可售量 = quantity − reservedQuantity ≥ 0；不得超賣 | SCN-STOCK-004；SCN-CHECKOUT-004；CLR-260613-01#Q1 | SCN-STOCK-002, SCN-STOCK-004, SCN-CHECKOUT-004 | haAPI |
| CON-STK-003 | reserve-release | StockItem | reservedQuantity | 下單成立時 reservedQuantity += 數量；付款完成轉為 quantity 扣減並釋放預留；逾時未付款（72h）釋放預留 | CLR-260613-01#Q1 | SCN-CHECKOUT-001, SCN-PAY-004, SCN-STOCK-004 | haAPI |
| CON-STK-002 | threshold-notify | StockItem | restockThreshold | 庫存由高於水位降至低於水位時觸發補貨通知 | SCN-STOCK-003 | SCN-STOCK-003 | haAPI |
| CON-CART-001 | precondition | CartItem | variantId | 已下架商品（Product.status=X 或 ProductVariant.isActive=0）不可加入購物車 | SCN-CART-004 | SCN-CART-001, SCN-CART-004 | haAPI |
| CON-ORD-001 | state-transition | Order | status | 訂單狀態機：N→P→C→S→D；N→X（逾時/取消）；D→R（退貨退款）。觸發者：N→P 金流/對帳、P→C 與 C→S 商家手動、S→D 物流回報、N→X 逾時自動 | 04-vision-kpi-scope.md；CLR-260613-03#ASM#008 | SCN-PAY-001/004, SCN-FULFILL-002/003, SCN-RETURN-004 | haAPI |
| CON-ORD-002 | timeout | Order | createdAt, status | 待付款訂單逾 72 小時未付款自動取消（N→X）並釋放預留庫存 | CLR-260613-01#Q1 | SCN-PAY-004 | haAPI |
| CON-ORD-004 | uniqueness | Order | couponId | 一筆訂單最多使用一張優惠券（CouponRedemption.orderId unique 落實） | SCN-COUPON-004 | SCN-COUPON-004 | haAPI |
| CON-ORD-005 | calculation | Order | shippingFee | 商品小計達免運門檻（暫定滿 1,000）運費為 0，否則收固定運費（暫定 100） | SCN-CHECKOUT-002 | SCN-CHECKOUT-002 | haAPI |
| CON-ORD-006 | calculation | Order | taxAmount | 5% 營業稅以「折扣後商品金額」為稅基：taxBase = subtotal − campaignDiscount − couponDiscount − pointsDiscount；運費不計入稅基 | CLR-260613-01#Q2 | SCN-CHECKOUT-003, SCN-PAY-005 | haAPI |
| CON-ORD-008 | calculation | Order | subtotal..totalAmount | 金額計算順序：活動價 → 優惠券 → 點數折抵 → 加運費 → 算稅；totalAmount = (subtotal − campaignDiscount − couponDiscount − pointsDiscount) + shippingFee + taxAmount | CLR-260613-01#Q2 | SCN-CHECKOUT-001/002/003, SCN-PROMO-004, SCN-COUPON-002, SCN-POINT-002 | haAPI |
| CON-ORD-011 | state-transition | Order | status | 已付款但未出貨（P 或 C）訂單可取消（→X）；取消後回補庫存、退券、退點 | CLR-260613-01#Q3 | SCN-PAY-004 | haAPI |
| CON-ORD-007 | immutable | OrderItem | productName, skuCode, unitPrice | 訂單成立時寫入的商品快照欄位不可隨商品後續異動而改變 | SCN-CHECKOUT-001；SCN-PRODUCT-005 | SCN-CHECKOUT-001, SCN-PRODUCT-005 | haAPI |
| CON-PAY-001 | manual-recon | Payment | transferLastFive | 銀行轉帳須回報匯款後五碼，由商家對帳確認後訂單轉「已付款」 | SCN-PAY-003 | SCN-PAY-003 | manual |
| CON-PNT-001 | value-check | PointLedger | points | 折抵點數不可超過會員當前點數餘額 | SCN-POINT-003 | SCN-POINT-002, SCN-POINT-003 | haAPI |
| CON-PNT-002 | compensating | Member | pointBalance | Member.pointBalance 為反正規化快取，須與 PointLedger 累計一致（見 COMPAT-03） | SCN-POINT-001/002 | SCN-POINT-001, SCN-POINT-002 | haAPI |
| CON-PNT-003 | value-check | Order | pointsUsed | 單筆訂單點數折抵上限 = 訂單金額 50% | CLR-260613-01#Q4 | SCN-POINT-002 | haAPI |
| CON-PNT-004 | calculation | PointLedger | points | 回饋發放基準 = 折扣後實付金額（每滿 100 元 1 點） | CLR-260613-01#Q4 | SCN-POINT-001 | haAPI |
| CON-PNT-005 | expiry | PointLedger | expireAt | 獲得型點數效期 1 年（expireAt = createdAt + 1y）；到期未用失效 | CLR-260613-01#Q4 | SCN-POINT-001 | haAPI |
| CON-CMP-001 | state-transition | Campaign | status | 檔期開始時排程中(S)→生效中(A)；檔期結束時生效中(A)→已失效(E)，由系統自動觸發 | SCN-PROMO-002/003 | SCN-PROMO-001, SCN-PROMO-002, SCN-PROMO-003 | haAPI |
| CON-CPN-001 | value-check | Coupon | minSpend | 訂單金額未達券最低消費門檻不可套用 | SCN-COUPON-003 | SCN-COUPON-002, SCN-COUPON-003 | haAPI |
| CON-CPN-002 | compensating | Coupon | usedCount | 已使用張數不得超過 usageCap；達上限不可再套用（usedCount 為反正規化，見 COMPAT-04） | SCN-COUPON-005 | SCN-COUPON-005 | haAPI |
| CON-CPN-003 | eligibility | Coupon | tierLimit | 等級限定券須會員 tierCode 符合 tierLimit 才可套用 | SCN-COUPON-006 | SCN-COUPON-006 | haAPI |
| CON-CPN-004 | compensating | Coupon | usedCount | 訂單取消/退款後，已套用的優惠券退還（CouponRedemption 作廢、usedCount −1，券可再用） | CLR-260613-01#Q3 | SCN-RETURN-004 | haAPI |
| CON-MBR-001 | uniqueness | Member | email | Email 全平台唯一，重複註冊被拒 | SCN-MEMBER-003 | SCN-MEMBER-001, SCN-MEMBER-003 | haAPI |
| CON-MBR-002 | state-transition | Member | status | 待驗證(V)→生效(A) 須完成信箱驗證；未生效不可購物 | SCN-MEMBER-002 | SCN-MEMBER-001, SCN-MEMBER-002 | haAPI |
| CON-MBR-003 | tiering | Member | tierCode | 會員等級依「近 12 個月累計實付消費」分四級（T1-T4）；門檻金額待平台提案；升降級由系統定期判定 | CLR-260613-01#Q4 | SCN-COUPON-006 | haAPI |
| CON-RTN-001 | timeout | ReturnRequest | appliedAt | 退貨期限 = 到貨後 7 天（自 Shipment.deliveredAt 起算）；逾期申請不成立；排除明顯損耗品/客製品 | CLR-260613-01#Q3 | SCN-RETURN-001, SCN-RETURN-005 | haAPI |
| CON-RTN-002 | state-transition | ReturnRequest | status | 退貨狀態機：待審核(P)→已核准(A)→商品已退回(D)→已退款(R)；待審核(P)→已拒絕(J) | SCN-RETURN-001/002/003/004 | SCN-RETURN-001, SCN-RETURN-002, SCN-RETURN-003, SCN-RETURN-004 | haAPI |
| CON-SHP-001 | uniqueness | Shipment | orderId | 一張訂單僅一張出貨單（orderId unique）；不支援部分出貨 | CLR-260613-03#GAP#012 | SCN-FULFILL-003 | haAPI |
| CON-ORD-009 | authorization | Order | memberId | 消費者僅能查詢/操作自身訂單 | SCN-TRACK-003 | SCN-TRACK-003 | haARM |
| CON-ORD-010 | authorization | Order | storeId | 商家僅能查詢/操作自店訂單 | SCN-FULFILL-004 | SCN-FULFILL-004 | haARM |
| CON-MOP-001 | ref-integrity | MerchantOperator | merchantId | 每個操作者隸屬單一 Merchant；店面隔離以 operator→merchant→store 推導 | CLR-260613-03#ASM#004 | SCN-FULFILL-004 | haARM |
| CON-WSH-001 | trigger-notify | Wishlist | productId | 收藏商品任一 SKU 售價調降時，透過 NotificationLog 通知收藏會員 | CLR-260613-03#GAP#002 | — | haAPI |
| CON-AUD-001 | audit | AuditLog | action | 下列操作必寫稽核：訂單狀態變更、退款、商家停權、價格異動、庫存異動 | CLR-260613-02#GAP#013 | SCN-ONBOARD-003, SCN-RETURN-004 | haAPI |

---

## 已解決 CiC（Phase 3 Clarification，2026-06-13）

| 原 CiC | 決策 | 落實 constraint |
|---|---|---|
| GAP #006 庫存扣減時點 | 下單即預留 + 逾時釋放；付款期限 72h | CON-STK-001, CON-STK-003, CON-ORD-002 |
| GAP #007 金額順序/稅基 | 活動→券→點數→運費→稅；稅基折後不含運 | CON-ORD-006, CON-ORD-008 |
| GAP #011 退換貨 | 7 天期限、原路退款、未出貨可取消、券退還 | CON-RTN-001, CON-ORD-011, CON-CPN-004 |
| GAP #013 稽核 | 新增 AuditLog，涵蓋狀態/退款/停權/價格/庫存 | CON-AUD-001 |
| GAP #010 會員分級 | 四級依 12 月累計消費；點數效期1年/上限50% | CON-MBR-003, CON-PNT-003/004/005 |

> 各級「消費門檻金額」標 deferred-needs-decision（待平台提案），不阻擋建模。

---

## Compatibility Decisions

| item | decision | risk | compensating_rule | source |
|---|---|---|---|---|
| COMPAT-01 ProductVariant.optionDesc | 規格以單一描述字串保存（不展開 顏色/容量 為獨立規格軸表） | 無法以結構化查詢單一規格軸、難以做規格軸層級報表 | MVP 僅需顯示與下單，規格軸結構化延後；haAPI 建立時驗證 skuCode 唯一 | 04-vision-kpi-scope.md MVP 極簡原則 |
| COMPAT-02 OrderItem 快照欄位 | productName/skuCode/unitPrice 於訂單成立時冗餘快照，不即時關聯 Product/Variant | 商品改名/改價後快照與現況不一致（此為刻意正確行為） | CON-ORD-007：快照不可變；查詢顯示一律用快照，不回查 Product | SCN-CHECKOUT-001, SCN-PRODUCT-005 |
| COMPAT-03 Member.pointBalance | 點數餘額反正規化快取於 Member（避免每次彙總 PointLedger） | 快取與 PointLedger 累計可能不一致 | CON-PNT-002：每筆 PointLedger 寫入時同交易更新 balanceAfter 與 Member.pointBalance | SCN-POINT-001/002 |
| COMPAT-04 Coupon.usedCount | 已使用張數反正規化快取於 Coupon（避免每次 count CouponRedemption） | 高併發下可能超發 | CON-CPN-002：套用券時於同交易檢查並遞增 usedCount，達 usageCap 拒絕 | SCN-COUPON-005 |
