# 統一語言詞彙表（Ubiquitous Language Glossary）

> 最後更新：2026-06-12
> 術語數量：24

## 業務實體術語

| 術語（繁中） | 英文 | 定義 | 使用位置 |
|---|---|---|---|
| 帳號 | Account | 可登入平台並對應商家、消費者或平台管理角色的識別。 | DBML / haARM |
| 商家 | Merchant | 使用 SmallBiz 開設線上商店並管理商品、訂單與促銷的付費客戶。 | Discovery / haBDD / DBML |
| 消費者 | ConsumerProfile | 在商店前台購買商品、追蹤訂單與申請退貨的會員。 | Discovery / haBDD / DBML |
| 地址 | Address | 消費者保存的常用收件資料。 | DBML |
| 分類 | Category | 商家用來組織商品的多層目錄節點。 | haBDD / DBML |
| 商品 | Product | 商家上架銷售的商品主體。 | haBDD / DBML |
| SKU | ProductSku | 商品下可獨立售價與庫存的銷售單位。 | haBDD / DBML |
| 庫存 | InventoryItem | SKU 的帳面與可販售數量。 | haBDD / DBML |
| 庫存異動 | InventoryMovement | 銷售扣減、人工調整或退貨回補造成的庫存變化紀錄。 | haBDD / DBML |
| 購物車 | Cart | 消費者結帳前暫存購買意向的容器。 | haBDD / DBML |
| 購物車項目 | CartItem | 購物車中的 SKU 與數量。 | DBML |
| 願望清單 | WishlistItem | 消費者收藏但尚未購買的商品。 | haBDD / DBML |
| 訂單 | SalesOrder | 消費者提交並由商家履約的購買請求。 | haBDD / DBML |
| 訂單項目 | OrderItem | 訂單中的商品快照、數量與金額。 | DBML |
| 付款 | Payment | 訂單付款方式、狀態與金額紀錄。 | haBDD / DBML |
| 物流 | Shipment | 訂單出貨與配送狀態紀錄。 | haBDD / DBML |
| 會員等級 | MemberLevel | 會員分級與權益的資料主體。 | haBDD / DBML |
| 點數流水 | PointLedger | 點數獲得、使用或到期的變化紀錄。 | haBDD / DBML |
| 促銷活動 | Promotion | 商家設定的期間性折扣活動。 | haBDD / DBML |
| 優惠券 | Coupon | 具有代碼、門檻、上限與資格限制的優惠工具。 | haBDD / DBML |
| 優惠券使用紀錄 | CouponRedemption | 優惠券被套用到訂單的紀錄。 | DBML |
| 退貨申請 | ReturnRequest | 消費者針對已送達訂單提出的退貨流程。 | haBDD / DBML |
| 退款 | Refund | 退貨或取消後的退款紀錄。 | haBDD / DBML |
| 通知 | Notification | 訂單、退貨或退款狀態變更的 LINE / Email 通知紀錄。 | haBDD / DBML |

## Canonical Mapping

| term | canonical_english | dbml_table | dbml_columns | gherkin_synonyms | legacy_aliases | notes |
|---|---|---|---|---|---|---|
| 帳號 | Account | Account | accountId,email,accountType,accountStatus | 使用者帳號 |  |  |
| 商家 | Merchant | Merchant | merchantId,merchantName,planStatus | 中小零售店老闆, 店主 |  | Gherkin actor 使用「中小零售店老闆 / 商家」。 |
| 消費者 | ConsumerProfile | ConsumerProfile | consumerId,accountId,memberLevelId | 客戶, 會員 |  | 統一使用「消費者」，會員表示已註冊狀態。 |
| 地址 | Address | Address | addressId,recipientName,phone,line1 | 收件資訊 |  |  |
| 分類 | Category | Category | categoryId,parentCategoryId,categoryName | 商品分類 |  |  |
| 商品 | Product | Product | productId,productName,productStatus | 品項 |  |  |
| SKU | ProductSku | ProductSku | skuId,skuCode,salePrice | 規格組合, 銷售單位 |  |  |
| 庫存 | InventoryItem | InventoryItem | inventoryItemId,onHandQty,availableQty | SKU 庫存 |  |  |
| 庫存異動 | InventoryMovement | InventoryMovement | movementId,movementType,quantity | 庫存流水 |  |  |
| 購物車 | Cart | Cart | cartId,cartStatus |  |  |  |
| 購物車項目 | CartItem | CartItem | cartItemId,skuId,quantity |  |  |  |
| 願望清單 | WishlistItem | WishlistItem | wishlistItemId,productId | 收藏商品 |  |  |
| 訂單 | SalesOrder | SalesOrder | orderId,orderStatus,totalAmount | 購買請求 |  | DBML table 使用 SalesOrder 避免通用字 Order。 |
| 訂單項目 | OrderItem | OrderItem | orderItemId,skuId,quantity,lineAmount | 訂單明細 |  |  |
| 付款 | Payment | Payment | paymentId,paymentMethod,paymentStatus,amount | 金流 |  | 金流服務商是外部依賴。 |
| 物流 | Shipment | Shipment | shipmentId,trackingNo,shipmentStatus | 出貨, 配送 |  |  |
| 會員等級 | MemberLevel | MemberLevel | memberLevelId,levelName,discountRate | VIP 等級 |  |  |
| 點數流水 | PointLedger | PointLedger | pointLedgerId,pointType,points | 點數帳本 |  |  |
| 促銷活動 | Promotion | Promotion | promotionId,promotionType,promotionStatus | 活動價 |  |  |
| 優惠券 | Coupon | Coupon | couponId,couponCode,discountType | 券 |  |  |
| 優惠券使用紀錄 | CouponRedemption | CouponRedemption | redemptionId,couponId,orderId |  |  |  |
| 退貨申請 | ReturnRequest | ReturnRequest | returnRequestId,returnStatus,reason | 退換貨 |  | MVP 先建退貨申請。 |
| 退款 | Refund | Refund | refundId,refundStatus,refundAmount |  |  |  |
| 通知 | Notification | Notification | notificationId,notificationType,channel | LINE 通知, Email 通知 |  |  |

## 欄位/屬性術語

| 術語 | 英文 | 定義 |
|---|---|---|
| 狀態 | status | 業務物件的生命週期位置，值域由 `seeds.md` 管理。 |
| 可販售庫存 | availableQty | 可接受新購買的 SKU 數量。 |
| 帳面庫存 | onHandQty | 商家記錄的 SKU 實際庫存數量。 |
| 商品快照 | snapshot | 訂單成立時保存的商品名稱、SKU 代碼與單價。 |
| 應付總額 | totalAmount | 訂單商品、優惠、運費與稅金計算後的消費者應付金額。 |
| 稅金 | taxAmount | 訂單營業稅金額，稅基仍待釐清。 |
| 低庫存水位 | lowStockThreshold | 商家設定的補貨提醒門檻。 |

## 已棄用術語

| 棄用詞 | 替換為 | 原因 |
|---|---|---|
| 用戶 | 消費者 / 帳號 | 用戶語意過寬，需區分購物角色與登入識別。 |
| 客戶 | 消費者 | 本專案以前台購物者統一稱為消費者。 |
| 品項 | 商品 / SKU | 商品是主體，SKU 是銷售單位，需避免混用。 |
## Clarification Glossary Updates

| term | canonical_name | definition | source |
|---|---|---|---|
| 庫存預留 | inventoryReservation | 下單成立時鎖定商品庫存，付款完成時正式扣減；訂單逾時取消時釋放。 | `.clarify/decisions/batch-CLR-260613-001.md#q1-cic-gap-001庫存扣減與預留策略` |
| 折扣疊加 | discountStacking | 活動價可與優惠券或會員折扣擇一疊加，優惠券與會員折扣互斥，點數折抵最後計算。 | `.clarify/decisions/batch-CLR-260613-001.md#q2-cic-gap-002折扣疊加與計算順序` |
| 稅基 | taxBase | 5% 營業稅以商品小計扣除活動、優惠券、會員折扣與點數折抵後的商品金額為稅基，不含運費。 | `.clarify/decisions/batch-CLR-260613-001.md#q5-cic-gap-0055-營業稅稅基` |
| 退貨期限 | returnWindow | 到貨後 7 天內可申請退貨；已拆封、個人化商品與耗材不可退。 | `.clarify/decisions/batch-CLR-260613-002.md#q6-cic-gap-006退貨期限不可退範圍與退款路徑` |
