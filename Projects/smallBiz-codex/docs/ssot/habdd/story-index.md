# User Story Index

> 最後更新：2026-06-12
> 總計：18 個故事（must-have: 15, should-have: 3, nice-to-have: 0, out-of-scope: 2）

## Must-Have

| 故事 ID | Actor | 目標 | 業務價值 | Feature 連結 |
|---|---|---|---|---|
| US-001 | merchant-owner | 建立商品、SKU 與分類 | 讓實體商品能轉為可販售的線上商品 | product-catalog.ha.feature |
| US-002 | merchant-owner | 管理商品上下架狀態 | 避免未完成或不可販售商品被購買 | product-catalog.ha.feature |
| US-003 | consumer | 瀏覽並理解商品資訊與價格 | 快速找到商品並判斷折扣是否可信 | product-discovery.ha.feature |
| US-004 | consumer | 收藏商品與保留購物車 | 讓未立即購買的商品可被日後找回 | product-discovery.ha.feature |
| US-005 | merchant-owner | 維護 SKU 庫存與低庫存水位 | 避免超賣並支援補貨決策 | inventory-control.ha.feature |
| US-006 | smallbiz-platform | 依訂單規則扣減庫存 | 維持庫存準確度與訂單一致性 | inventory-control.ha.feature |
| US-007 | consumer | 以最少必要資訊提交訂單 | 降低結帳流失並完成購買 | checkout-payment.ha.feature |
| US-008 | consumer | 使用支援的付款方式完成付款 | 讓訂單進入可履約狀態 | checkout-payment.ha.feature |
| US-009 | smallbiz-platform | 計算訂單金額、運費、稅金與優惠 | 讓消費者與商家看到一致金額 | checkout-payment.ha.feature |
| US-010 | merchant-owner | 查看並處理訂單狀態 | 減少漏單與重複出貨 | order-fulfillment.ha.feature |
| US-011 | consumer | 追蹤訂單與物流狀態 | 降低付款後資訊不透明的焦慮 | order-fulfillment.ha.feature |
| US-012 | consumer | 註冊會員並使用點數 | 累積忠誠關係並提升回購 | membership-loyalty.ha.feature |
| US-013 | platform-marketer | 定義會員等級與專屬資格 | 支援分級行銷與 VIP 權益 | membership-loyalty.ha.feature |
| US-014 | merchant-owner | 建立促銷活動與優惠券 | 推動銷售並控制優惠風險 | promotion-coupon.ha.feature |
| US-015 | consumer | 線上申請退貨並取得退款進度 | 讓售後流程簡單且可追蹤 | return-refund.ha.feature |

## Should-Have

| 故事 ID | Actor | 目標 | 業務價值 | Feature 連結 |
|---|---|---|---|---|
| US-016 | merchant-owner | 查看銷售與商品報表 | 用資料支援補貨與營運判斷 | merchant-reporting.ha.feature |
| US-017 | platform-admin | 維護商家、消費者與平台權限邊界 | 保護商家資料與消費者訂單隱私 | access-boundary.ha.feature |
| US-018 | smallbiz-platform | 發送訂單狀態通知 | 讓狀態變更能被消費者掌握 | order-fulfillment.ha.feature |

## Out-of-Scope

| 故事 ID | Actor | 目標 | 原因 | Feature 連結 |
|---|---|---|---|---|
| OOS-001 | merchant-owner | 專案型客製建站 | discovery 已明確排除，SmallBiz 採月租制 SaaS | out-of-scope |
| OOS-002 | platform-admin | 保存敏感付款資訊 | discovery 已明確排除，支付資訊由金流服務商處理 | out-of-scope |

## Deferred

| 項目 | 狀態 | 來源 | 備註 |
|---|---|---|---|
| 多倉庫 / 多門市出貨 | deferred | docs/discovery/04-vision-kpi-scope.md#Deferred | 後續版本再釐清是否預留資料模型。 |
| 願望清單降價通知 | deferred | docs/discovery/04-vision-kpi-scope.md#Deferred | MVP 未納入自動降價通知。 |
| 部分出貨能力 | deferred | docs/discovery/04-vision-kpi-scope.md#Deferred | 訂單缺貨時是否允許部分出貨延後到後續版本裁決。 |
| PayPal 以外的其他電子支付 | deferred | docs/discovery/04-vision-kpi-scope.md#Deferred | 第一版付款方式已列信用卡、PayPal、銀行轉帳。 |

## Cross-Cutting Capability Matrix

| module | capability | handling | feature/scenario | decision_ref | notes |
|---|---|---|---|---|---|
| 訂單管理 | 篩選 | scenario | order-fulfillment.ha.feature#SCN-ORDER-001 |  | 商家需依訂單狀態判斷待處理訂單。 |
| 商家報表 | 篩選 | scenario | merchant-reporting.ha.feature#SCN-REPORT-001 |  | 報表以期間呈現訂單數、營業額與客單價。 |
| 商品管理 | 授權不足 | scenario | access-boundary.ha.feature#SCN-AUTH-001 |  | 商家只能管理自己的商店資料。 |
| 訂單查詢 | 授權不足 | scenario | access-boundary.ha.feature#SCN-AUTH-002 |  | 消費者只能查看自己的訂單。 |
| 購物車 | 清理 / 保留政策 | scenario | product-discovery.ha.feature#SCN-DISC-003 |  | 購物車跨裝置保留是 scope 明列能力。 |
| 付款 | 稽核記錄 | common-dsl | checkout-payment.ha.feature#SCN-CHECKOUT-003 |  | 僅以業務結果記錄金額來源；精確稽核欄位留待 modeling。 |
| 退貨退款 | 稽核記錄 | common-dsl | return-refund.ha.feature#SCN-RETURN-002 |  | 審核與退款進度需可追蹤；精確欄位留待 modeling。 |
| 商品管理 | 匯入 | out-of-scope |  | docs/discovery/04-vision-kpi-scope.md#範圍邊界 | discovery 未列商品匯入能力。 |
| 商品管理 | 匯出 | out-of-scope |  | docs/discovery/04-vision-kpi-scope.md#範圍邊界 | discovery 未列商品匯出能力。 |
| 訂單管理 | 批次處理 | out-of-scope |  | docs/discovery/04-vision-kpi-scope.md#範圍邊界 | discovery 未列批次處理能力。 |
| 訂單管理 | 部分成功 / 部分失敗 | deferred |  | docs/discovery/04-vision-kpi-scope.md#Deferred | 部分出貨延後；取消退款規則已由 DEC-CLR-004 裁決。 |

## Feature Summary

| Feature | Stories | Source Evidence |
|---|---|---|
| product-catalog.ha.feature | US-001, US-002 | docs/discovery/02-user-journeys.md#中小零售店老闆--商家的主要旅程建立並營運線上商店 |
| product-discovery.ha.feature | US-003, US-004 | docs/discovery/02-user-journeys.md#一般網購消費者的主要旅程從瀏覽到售後 |
| inventory-control.ha.feature | US-005, US-006 | docs/discovery/03-event-timeline.md#庫存 |
| checkout-payment.ha.feature | US-007, US-008, US-009 | docs/discovery/02-user-journeys.md#一般網購消費者的主要旅程從瀏覽到售後 |
| order-fulfillment.ha.feature | US-010, US-011, US-018 | docs/discovery/03-event-timeline.md#訂單與履約 |
| membership-loyalty.ha.feature | US-012, US-013 | docs/discovery/04-vision-kpi-scope.md#範圍邊界 |
| promotion-coupon.ha.feature | US-014 | docs/discovery/02-user-journeys.md#平台營運--行銷人員的主要旅程協助商家做促銷 |
| return-refund.ha.feature | US-015 | docs/discovery/02-user-journeys.md#一般網購消費者的主要旅程從瀏覽到售後 |
| merchant-reporting.ha.feature | US-016 | docs/discovery/02-user-journeys.md#中小零售店老闆--商家的主要旅程建立並營運線上商店 |
| access-boundary.ha.feature | US-017 | docs/discovery/04-vision-kpi-scope.md#範圍邊界 |
