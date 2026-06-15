# Seeds and Value Sets

> 規格層值域 SSoT（rapt-modeling）。未來 DB seed script 為 generated artifact，方向只能 `seeds.md -> generated`。
> 來源：docs/ssot/habdd/*.ha.feature、docs/discovery/03-event-timeline.md、04-vision-kpi-scope.md
> 每個 DBML `ref_code:` 都必須在此有對應 section，或有 OPEN CiC。

---

## MerchantStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Merchant | status | P | 待開通 | 已註冊、等待平台開通 | event #1；SCN-ONBOARD-001 | true |
| Merchant | status | A | 營運中 | 平台已開通，可上架營運 | event #2；SCN-ONBOARD-002 | true |
| Merchant | status | S | 停權 | 平台停權，店面暫停營運 | SCN-ONBOARD-003 | true |

## StoreStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Store | status | P | 待開通 | 商家已註冊、店面尚未營運 | SCN-ONBOARD-001 | true |
| Store | status | A | 營運中 | 店面可上架、可被消費者瀏覽 | SCN-ONBOARD-002 | true |
| Store | status | S | 暫停營運 | 商家被停權，前台商品不再顯示 | SCN-ONBOARD-003 | true |

## PlatformRole

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| PlatformUser | roleCode | admin | 平台管理員 | 管理商家開通/停權 | 01-stakeholders.md；CLR-260613-03#ASM#003 | true |
| PlatformUser | roleCode | marketer | 平台行銷/營運 | 代操促銷與優惠券 | 01-stakeholders.md；CLR-260613-03#ASM#003 | true |

> ✅ RESOLVED（CLR-260613-03#ASM#003）：確認平台端拆分 admin / marketer 兩角色。

## OperatorStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| MerchantOperator | status | A | 啟用 | 操作者可登入操作後台 | CLR-260613-03#ASM#004 | true |
| MerchantOperator | status | S | 停用 | 操作者帳號停用 | CLR-260613-03#ASM#004 | true |

## AuditActorType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| AuditLog | actorType | M | 商家操作者 | MerchantOperator | CLR-260613-02#GAP#013 | true |
| AuditLog | actorType | P | 平台人員 | PlatformUser | CLR-260613-02#GAP#013 | true |
| AuditLog | actorType | C | 消費者 | Member | CLR-260613-02#GAP#013 | true |
| AuditLog | actorType | S | 系統 | 自動排程/事件 | CLR-260613-02#GAP#013 | true |

## AuditAction

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| AuditLog | action | OS | 訂單狀態變更 | Order.status 變更 | CLR-260613-02#GAP#013 | true |
| AuditLog | action | RF | 退款 | Refund 執行 | CLR-260613-02#GAP#013 | true |
| AuditLog | action | MS | 商家停權 | Merchant/Store 狀態變更 | CLR-260613-02#GAP#013 | true |
| AuditLog | action | PC | 價格異動 | ProductVariant.price 變更 | CLR-260613-02#GAP#013 | true |
| AuditLog | action | SC | 庫存異動 | StockItem.quantity 變更 | CLR-260613-02#GAP#013 | true |

## ProductStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Product | status | D | 草稿 | 已建立、不在前台顯示 | SCN-PRODUCT-001 | true |
| Product | status | A | 上架 | 前台可被消費者瀏覽 | SCN-PRODUCT-004 | true |
| Product | status | X | 下架 | 前台不再顯示，不影響既有訂單 | SCN-PRODUCT-005 | true |

## OrderStatus

> 七種狀態（04-vision-kpi-scope.md In-Scope「七種狀態」）；狀態轉換見 constraints.md CON-ORD-001。

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Order | status | N | 待付款 | 訂單成立、未完成付款 | SCN-CHECKOUT-001 | true |
| Order | status | P | 已付款 | 付款成功或商家對帳確認 | SCN-PAY-001/003 | true |
| Order | status | C | 已確認 | 商家確認待出貨 | SCN-FULFILL-002 | true |
| Order | status | S | 已出貨 | 已交物流、具物流單號 | SCN-FULFILL-003 | true |
| Order | status | D | 已送達 | 物流回報送達 | SCN-TRACK-002；event #23 | true |
| Order | status | X | 已取消 | 逾時未付款或取消 | SCN-PAY-004 | true |
| Order | status | R | 已退款 | 退貨確認後完成退款 | SCN-RETURN-004 | true |

## PaymentMethod

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Payment | method | C | 信用卡 | 透過金流服務商收款 | SCN-PAY-001 | true |
| Payment | method | P | PayPal | 透過金流服務商收款 | 04-vision-kpi-scope.md#付款 | true |
| Payment | method | T | 銀行轉帳 | 匯款後回報後五碼人工對帳 | SCN-PAY-003 | true |

## PaymentStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Payment | status | P | 處理中 | 已發起、待結果或待對帳 | SCN-PAY-002 | true |
| Payment | status | S | 成功 | 付款完成 | SCN-PAY-001 | true |
| Payment | status | F | 失敗 | 付款失敗，訂單保留待付款 | SCN-PAY-002 | true |

## RefundStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Refund | status | P | 處理中 | 退款已發起 | SCN-RETURN-004 | true |
| Refund | status | S | 已退款 | 退款完成 | SCN-RETURN-004 | true |
| Refund | status | F | 失敗 | 退款失敗待重試 | 推斷（金流退款慣例） | true |

## ShipmentStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Shipment | status | S | 已出貨 | 商家標記出貨、待物流取件 | SCN-FULFILL-003 | true |
| Shipment | status | T | 配送中 | 物流運送途中 | event #23 | true |
| Shipment | status | D | 已送達 | 物流回報送達 | event #23 | true |

## ReturnStatus

> 狀態轉換見 constraints.md CON-RTN-002。

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| ReturnRequest | status | P | 待審核 | 消費者已申請、待商家審核 | SCN-RETURN-001 | true |
| ReturnRequest | status | A | 已核准 | 商家核准、安排取件 | SCN-RETURN-002 | true |
| ReturnRequest | status | J | 已拒絕 | 商家拒絕並附原因 | SCN-RETURN-003 | true |
| ReturnRequest | status | D | 商品已退回 | 物流取回、商家確認無誤 | SCN-RETURN-004；event #30 | true |
| ReturnRequest | status | R | 已退款 | 退款完成 | SCN-RETURN-004 | true |

## MemberStatus

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Member | status | V | 待驗證 | 已註冊、信箱尚未驗證 | SCN-MEMBER-001 | true |
| Member | status | A | 生效 | 信箱已驗證、可購物 | SCN-MEMBER-002 | true |

## MemberTier

> 四級暫定（04-vision-kpi-scope.md「四級會員（暫定）」）；分級依據、區間、升降級規則未決。

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Member | tierCode | T1 | 一般會員 | 註冊初始等級 | event #10；CLR-260613-01#Q4 | true |
| Member | tierCode | T2 | 銀級 | 依近12月累計消費升級 | CLR-260613-01#Q4 | true |
| Member | tierCode | T3 | 金級 | 依近12月累計消費升級 | CLR-260613-01#Q4 | true |
| Member | tierCode | T4 | 白金級 | 依近12月累計消費升級 | CLR-260613-01#Q4 | true |

> ✅ RESOLVED（CLR-260613-01#Q4）：四級會員確立，分級依「近 12 個月累計消費」（CON-MBR-003）。
> ⏳ deferred-needs-decision：各級「消費門檻金額」待平台提案後定案（不阻擋建模；升降級判斷邏輯於 haAPI 實作）。

## PointChangeType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| PointLedger | changeType | E | 獲得 | 訂單完成發放（100 元 1 點） | SCN-POINT-001 | true |
| PointLedger | changeType | U | 折抵 | 結帳折抵（1 點折 1 元） | SCN-POINT-002 | true |
| PointLedger | changeType | R | 回退 | 訂單取消/退款時點數回補 | 推斷（取消回補慣例） | true |

## CampaignType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Campaign | campaignType | P | 百分比折扣 | 商品售價乘折扣比例 | SCN-PROMO-004 | true |
| Campaign | campaignType | A | 滿額折現 | 達門檻後減固定金額 | SCN-PROMO-004 | true |
| Campaign | campaignType | B | 買X送Y | 加贈指定贈送商品 | SCN-PROMO-004 | true |

## CampaignStatus

> 狀態轉換見 constraints.md CON-CMP-001。

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Campaign | status | S | 排程中 | 已建立、檔期未開始 | SCN-PROMO-001 | true |
| Campaign | status | A | 生效中 | 檔期內、優惠前台生效 | SCN-PROMO-002 | true |
| Campaign | status | E | 已失效 | 檔期結束、恢復原售價 | SCN-PROMO-003 | true |

## CouponDiscountType

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| Coupon | discountType | P | 百分比 | 折扣比例 | SCN-COUPON-002 | true |
| Coupon | discountType | A | 固定金額 | 減固定金額 | 04-vision-kpi-scope.md#促銷 | true |

## NotificationChannel

| owner_table | owner_column | value | label | meaning | source | active |
|---|---|---|---|---|---|---|
| NotificationLog | channel | L | LINE | LINE 推播（訪談強需求） | 01-stakeholders.md | true |
| NotificationLog | channel | E | Email | Email 通知 | 01-stakeholders.md | true |
