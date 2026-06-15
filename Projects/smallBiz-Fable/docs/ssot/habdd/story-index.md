# User Story Index

> 最後更新：2026-06-13（Phase 1.5 增量：補 F-016 願望清單、F-017 會員等級）
> 總計：21 個故事（must-have: 17, should-have: 1, nice-to-have: 1, deferred: 2）
> 來源：docs/discovery/02-user-journeys.md、03-event-timeline.md、04-vision-kpi-scope.md
> Feature 檔案：17 個（F-001 ~ F-017，haBDD lint 0 ERROR / 0 WARN）

## Must-Have

| 故事 ID | Actor | 目標 | 業務價值 | source_evidence | Feature 連結 |
|--------|-------|------|---------|----------------|------------|
| US-001 | consumer | 以 Email 註冊會員並驗證信箱 | 取得會員身分以購物、累點 | 02-user-journeys.md#consumer旅程1；events #9-#11 | member-account.ha.feature（F-001） |
| US-002 | consumer | 瀏覽多層分類並搜尋商品 | 快速找到想買的商品 | 02-user-journeys.md#consumer旅程1步驟1 | product-browsing.ha.feature（F-002） |
| US-003 | consumer | 管理跨裝置保留的購物車 | 隨時湊單、不流失購買意願 | 02-user-journeys.md#consumer旅程1步驟2 | shopping-cart.ha.feature（F-003） |
| US-004 | consumer | 以極簡流程結帳並提交訂單 | 順利完成購買、金額自動算對 | 02-user-journeys.md#consumer旅程1步驟3；events #16-#17 | checkout-order.ha.feature（F-004） |
| US-005 | consumer | 以慣用方式完成付款 | 安全付款、確定買到 | 02-user-journeys.md#consumer旅程1步驟4；events #18-#19 | payment-invoice.ha.feature（F-005） |
| US-006 | consumer | 追蹤訂單狀態並收到通知 | 全程進度可見、不需電話詢問 | 02-user-journeys.md#consumer旅程1步驟5；event #24 | order-tracking.ha.feature（F-006） |
| US-007 | consumer | 獲得並折抵消費點數 | 回購誘因、累積忠誠 | 02-user-journeys.md#consumer旅程1步驟6；events #15 #32 | loyalty-points.ha.feature（F-012） |
| US-008 | consumer | 線上申請退貨免紙本 | 簡單退貨、不被流程刁難 | 02-user-journeys.md#consumer旅程2；events #27-#31 | returns.ha.feature（F-011） |
| US-009 | merchant | 註冊開店、當天開始營運 | 開箱即用、不需技術知識 | 02-user-journeys.md#merchant旅程1步驟1；event #1 | merchant-onboarding.ha.feature（F-007） |
| US-010 | merchant | 建立商品、規格組合與 SKU 並上下架 | 商品搬上線、自主管理 | 02-user-journeys.md#merchant旅程1步驟2；events #3-#5 #8 | product-management.ha.feature（F-008） |
| US-011 | merchant | 管理 SKU 庫存與低水位提醒 | 賣一個扣一個、不再超賣 | 02-user-journeys.md#merchant旅程1步驟3；events #6 #7 #38 #39 | inventory-management.ha.feature（F-009） |
| US-012 | merchant | 在訂單看板篩選、確認、出貨 | 不漏單、不重複出貨 | 02-user-journeys.md#merchant旅程2步驟1-2；events #21 #22 | order-fulfillment.ha.feature（F-010） |
| US-013 | merchant | 審核退貨並執行退款 | 有規則可循、不被濫退 | 02-user-journeys.md#merchant旅程2步驟3；events #28 #30 #31 | returns.ha.feature（F-011） |
| US-014 | merchant | 查看極簡銷售報表 | 進貨有依據 | 02-user-journeys.md#merchant旅程2步驟4；event #40 | merchant-reporting.ha.feature（F-015） |
| US-015 | merchant, platform-marketer | 建立有檔期的促銷活動 | 自動上下架、不靠人工切 | 02-user-journeys.md#促銷旅程步驟1；events #34-#36 | promotion-campaign.ha.feature（F-013） |
| US-016 | merchant, platform-marketer | 發行防濫用的優惠券 | 行銷拉新不被薅羊毛 | 02-user-journeys.md#促銷旅程步驟2；event #37 | coupon.ha.feature（F-014） |
| US-017 | platform-admin | 開通與停權商家帳號 | 平台營運健康 | 02-user-journeys.md#platform-admin旅程；events #1 #2 | merchant-onboarding.ha.feature（F-007） |

## Should-Have

| 故事 ID | Actor | 目標 | 業務價值 | source_evidence | Feature 連結 |
|--------|-------|------|---------|----------------|------------|
| US-018 | consumer | 依會員等級享折扣與專屬權益 | 高等級回購誘因 | PRD 5.2；event #33 | covered（member-tier.ha.feature F-017，4 scenario；門檻金額 deferred-needs-decision 以規則層變數承接） |

## Nice-to-Have

| 故事 ID | Actor | 目標 | 業務價值 | source_evidence | Feature 連結 |
|--------|-------|------|---------|----------------|------------|
| US-019 | consumer | 願望清單與降價通知 | 延後購買不流失 | 訪談 2；CLR-260613-03#GAP#002 | covered（wishlist.ha.feature F-016，4 scenario；入 MVP，CON-WSH-001） |

## Deferred / Open

| 故事 ID | Actor | 目標 | 狀態 | source_evidence |
|--------|-------|------|------|----------------|
| US-020 | merchant | 多倉庫 / 多門市出貨 | deferred（04-vision-kpi-scope.md#Deferred） | 構想書 §6、PRD 2.4 |
| US-021 | platform-admin | 月租方案計費管理 | open-cic（GAP #009：是否入 MVP 未定） | 商業模式隱含 |

## Cross-Cutting Capability Matrix

| module | capability | handling | feature/scenario | decision_ref | notes |
|---|---|---|---|---|---|
| 訂單管理（商家） | 篩選 | scenario | order-fulfillment.ha.feature#SCN-FULFILL-001 | | PRD 4.3 明列依狀態篩選 |
| 訂單資料（消費者） | 授權不足 | scenario | order-tracking.ha.feature#SCN-TRACK-003 | | PRD §0：消費者限自身訂單 |
| 訂單資料（商家） | 授權不足 | scenario | order-fulfillment.ha.feature#SCN-FULFILL-004 | | PRD §0：商家限自店 |
| 訂單出貨 | 部分成功（部分出貨） | deferred-mvp-out | | GAP #012 RESOLVED | 不支援部分出貨，一單整單出貨 CON-SHP-001 |
| 折扣計算 | 疊加順序 / 部分套用 | resolved | | GAP #007 RESOLVED | 活動→券→點數→運費→稅，稅基折後不含運 CON-ORD-006/008 |
| 會員等級 | 升降級規則 | scenario | member-tier.ha.feature#SCN-TIER-001~003 | GAP #010 RESOLVED | 四級依12月累計消費 CON-MBR-003；門檻金額 deferred-needs-decision |
| 報表 | 匯出 / 匯入 / 批次 | out-of-scope | | | 三份 source 皆未提及，MVP 報表僅線上檢視 |
| 全模組 | 稽核記錄 | resolved | | GAP #013 RESOLVED | 新增 AuditLog 通用稽核 CON-AUD-001 |

## CiC 便條

<!-- CiC GAP #012 — RESOLVED（CLR-260613-03，2026-06-13）-->
**類型**：GAP
**狀態**：RESOLVED — 決策：不支援部分出貨，一單整單出貨（Shipment.orderId unique，CON-SHP-001）；deferred-mvp-out。
**位置**：docs/ssot/habdd/story-index.md#Cross-CuttingCapabilityMatrix
**描述**：一張訂單部分商品缺貨時可否部分出貨（PRD 4.6）未決，無法寫出可驗證的出貨 scenario 變體。
**影響**：order-fulfillment feature、Order/Shipment 模型
<!-- /CiC -->

<!-- CiC GAP #013 — RESOLVED（CLR-260613-02，2026-06-13）-->
**類型**：GAP
**狀態**：RESOLVED — 決策：新增通用 AuditLog，涵蓋訂單狀態變更、退款、商家停權、價格/庫存異動（CON-AUD-001）。
**位置**：docs/ssot/habdd/story-index.md#Cross-CuttingCapabilityMatrix
**描述**：稽核記錄（誰在何時改了價格/庫存/訂單狀態）在 source 中未被提及，但退款、對帳、停權等高風險操作慣例上需要操作軌跡。
**影響**：DBML 稽核欄位、haARM、haAPI
<!-- /CiC -->
