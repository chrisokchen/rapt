# 統一語言詞彙表（Ubiquitous Language Glossary）

> 最後更新：2026-06-13（Phase 3 Clarification 後）
> 術語數量：37（業務實體 29 + 屬性/概念 8）
> 來源：docs/discovery/01-stakeholders.md、03-event-timeline.md、docs/ssot/habdd/*.ha.feature、docs/ssot/dbml/schema.dbml

## 業務實體術語

| 術語（繁中）| 英文 | 定義 | 使用位置 |
|-----------|------|------|---------|
| 商家 | Merchant | 以月租方式租用平台開店的店家主體 | Feature / DBML / haARM |
| 商家操作者 | MerchantOperator | 隸屬商家的登入操作帳號（店主或店員） | DBML / haARM |
| 店面 | Store | 商家經營的線上商店，商品/訂單歸屬單位 | Feature / DBML / haARM |
| 平台人員 | PlatformUser | 平台側管理商家與促銷的內部帳號 | DBML / haARM |
| 商品分類 | Category | 多層樹狀的商品歸類 | Feature / DBML |
| 品牌 | Brand | 商品的品牌標記 | DBML |
| 商品 | Product | 商家上架販售的商品主體 | Feature / DBML / haAPI |
| 商品圖片 | ProductImage | 商品的展示圖片 | DBML |
| 商品規格 / SKU | ProductVariant | 商品規格組合，最小可售與計價單位 | Feature / DBML / haAPI |
| 庫存 | StockItem | 以 SKU 為單位的即時可售數量 | Feature / DBML |
| 購物車 | Cart | 會員彙整待購商品的容器（每會員一車） | Feature / DBML |
| 購物車品項 | CartItem | 購物車內的單一 SKU 與數量 | DBML |
| 訂單 | Order | 消費者確認的購買請求，含金額與收件資訊 | Feature / DBML / haAPI |
| 訂單明細 | OrderItem | 訂單內單一 SKU 的商品快照與數量 | Feature / DBML |
| 付款 | Payment | 一筆訂單的收款紀錄 | Feature / DBML |
| 發票 | Invoice | 付款後開立的電子發票（含 5% 稅） | Feature / DBML |
| 退款 | Refund | 退貨確認後的退款紀錄 | Feature / DBML |
| 出貨單 | Shipment | 商家標記出貨後的物流配送紀錄 | Feature / DBML |
| 退貨申請 | ReturnRequest | 消費者線上提出的退貨請求 | Feature / DBML |
| 會員 | Member | 經 Email 註冊驗證的消費者帳號 | Feature / DBML / haARM |
| 收件地址 | MemberAddress | 會員儲存的常用收件地址 | Feature / DBML |
| 點數異動帳 | PointLedger | 會員點數增減的逐筆帳 | Feature / DBML |
| 促銷活動 | Campaign | 有檔期、自動上下架的優惠活動 | Feature / DBML |
| 優惠券 | Coupon | 有門檻/張數上限/效期的折扣券 | Feature / DBML |
| 優惠券使用紀錄 | CouponRedemption | 優惠券於訂單套用的紀錄（落實一單一券） | DBML |
| 通知 | NotificationLog | 推送給會員的 LINE/Email 訊息紀錄 | Feature / DBML |
| 願望清單 | Wishlist | 會員收藏商品、降價時收通知 | Feature / DBML |
| 稽核紀錄 | AuditLog | 高風險操作的軌跡（狀態/退款/停權/價格/庫存） | DBML / haARM |
| 平台管理員 | platform-admin | 管理商家開通/停權的平台角色（actor） | Feature / haARM |

## Canonical Mapping

| term | canonical_english | dbml_table | dbml_columns | gherkin_synonyms | legacy_aliases | notes |
|---|---|---|---|---|---|---|
| 商家 | Merchant | Merchant | merchantId,status | 店主 | | 店家主體 |
| 商家操作者 | MerchantOperator | MerchantOperator | operatorId,merchantId,isOwner | 店員,操作帳號 | | 一店多帳號（CLR-260613-03） |
| 店面 | Store | Store | storeId,status | 商店,店鋪 | | 商家 1:1 店面（MVP） |
| 平台人員 | PlatformUser | PlatformUser | platformUserId,roleCode | | | admin/marketer ASM #003 |
| 商品分類 | Category | Category | categoryId,parentCategoryId | 分類 | | 多層樹狀 |
| 品牌 | Brand | Brand | brandId | | | |
| 商品 | Product | Product | productId,status | | | |
| 商品圖片 | ProductImage | ProductImage | imageId | | | |
| 商品規格 | ProductVariant | ProductVariant | variantId,skuCode,price | SKU,規格組合 | | SKU 即 ProductVariant |
| 庫存 | StockItem | StockItem | variantId,quantity | 可售庫存 | | 與 SKU 1:1 |
| 購物車 | Cart | Cart | cartId,memberId | | | |
| 購物車品項 | CartItem | CartItem | cartItemId,quantity | | | |
| 訂單 | Order | Order | orderId,status,totalAmount | 購買請求 | | |
| 訂單明細 | OrderItem | OrderItem | orderItemId,unitPrice | 商品快照 | | 含快照欄位 |
| 付款 | Payment | Payment | paymentId,method,status | | | |
| 發票 | Invoice | Invoice | invoiceId,invoiceNo,taxAmount | 電子發票 | | |
| 退款 | Refund | Refund | refundId,amount,status | | | |
| 出貨單 | Shipment | Shipment | shipmentId,trackingNo | 物流單 | | 一單一出貨（MVP） |
| 退貨申請 | ReturnRequest | ReturnRequest | returnRequestId,status | 退貨 | | |
| 會員 | Member | Member | memberId,email,tierCode,pointBalance | 消費者,用戶 | | 「消費者」為 actor、「會員」為帳號實體 |
| 收件地址 | MemberAddress | MemberAddress | addressId,address | 常用地址 | | |
| 點數異動帳 | PointLedger | PointLedger | ledgerId,points,balanceAfter | 點數 | | |
| 促銷活動 | Campaign | Campaign | campaignId,campaignType,status | 活動 | | |
| 優惠券 | Coupon | Coupon | couponId,code,minSpend | 券 | | |
| 優惠券使用紀錄 | CouponRedemption | CouponRedemption | redemptionId,orderId | | | orderId unique |
| 通知 | NotificationLog | NotificationLog | notificationId,channel | | | |
| 願望清單 | Wishlist | Wishlist | wishlistId,memberId,productId | 收藏 | | 降價通知 |
| 稽核紀錄 | AuditLog | AuditLog | auditId,action,targetEntity | 操作軌跡 | | actorId/targetId 多型，無 FK Ref |

## 欄位/屬性術語

| 術語 | 英文 | 定義 |
|------|------|------|
| 會員等級 | tierCode / MemberTier | 會員忠誠分級（四級暫定，規則 GAP #010） |
| 點數餘額 | pointBalance | 會員可用於折抵的點數（1 點折 1 元） |
| 商品快照 | snapshot | 訂單成立當下凍結的商品名稱/SKU/單價 |
| 原價（划線價）| originalPrice | SKU 的對照原價，前台以划線顯示 |
| 補貨水位 | restockThreshold | 觸發補貨通知的庫存下限 |
| 免運門檻 | shippingFee threshold | 商品小計達門檻免運（暫定滿 1,000） |
| 後五碼 | transferLastFive | 銀行轉帳匯款帳號後五碼，供人工對帳 |
| 點數效期 | expireAt | 獲得型點數的失效日（createdAt + 1 年） |
| 預留量 | reservedQuantity | 已下單未付款而暫留的庫存，付款轉扣、逾時釋放 |

## 已棄用術語

| 棄用詞 | 替換為 | 原因 |
|--------|-------|------|
| 用戶 | 會員（Member）| 統一消費者帳號實體稱「會員」，避免與「平台人員/商家」混淆 |
| 客戶 | 會員（Member）| 同上，B2C 前台一律稱會員 |
| 變體 | 商品規格 / SKU（ProductVariant）| 統一以「SKU / 商品規格」稱呼，避免「變體」「規格組合」混用 |
| 物流單 | 出貨單（Shipment）| Gherkin 中「物流單」「物流單號」統一對應 Shipment.trackingNo |

---

## 術語一致性備註

- **消費者（consumer）** 是 haARM actor（操作系統的人）；**會員（Member）** 是 DBML 實體（帳號資料）。L2 traceability 的 entities「會員」對應 Member、「商品」對應 Product、「庫存」對應 StockItem、「點數」對應 PointLedger、「物流單」對應 Shipment、「商品快照」對應 OrderItem。
- 高階 Gherkin 使用中文術語，須與本表 term 欄一致；混用同義詞為 AP-G08，由 rapt-verify 警告。
