# RAPTor Session

> arguments.yml: initialized
> arguments_schema_version: 2
> initialized_at: 2026-06-12

## Phase Status

| Phase | Status | Next |
|---|---|---|
| 1. Discovery | **completed**（2026-06-12，閘門 PASS） | /rapt-behavior |
| 1.5 Behavior | **completed**（2026-06-12，閘門 9/9 PASS） | /rapt-modeling |
| 2. Modeling | **completed**（2026-06-13，閘門 11/11 PASS） | /rapt-clarify |
| 3. Clarification | **completed**（2026-06-13，閘門 6/6 PASS） | /rapt-intent |
| 4. Intent | **completed**（2026-06-13，閘門 5/5 PASS） | /rapt-verify |
| 5. Verification | **completed**（2026-06-13，PARTIAL；7/7 閘門，0 blocker） | /rapt-RAscore |
| 6. Reconcile | not-needed（0 NEED_TO_FIX） | /rapt-reconcile |
| Preview | deferred | /rapt-openapi, /rapt-lofi, /rapt-design-brief |

## RAscore 摘要（2026-06-13，advisory-only）

分數：**95.13 / 100（等級 A）**；Veto 未觸發。

維度加權：A 需求覆蓋 20.0/20、B Gherkin 16.8/18、C DBML 14.0/14、D 跨規格一致 22.0/24、E 追溯 14.0/14、F 生成準備 5.83/7、G 流程 2.5/3。

3 筆 findings（不阻擋）：
- RA-F1-001（medium）：會員等級門檻金額未定，tier 場景無法量化斷言 → rapt-clarify（待平台提案）
- RA-B5-001（low）：feature 內偶用『物流單』『SKU』同義詞 → rapt-behavior（重渲染統一）
- RA-D3-001（low）：AuditLog/Invoice/Payment/Refund 等支援實體無直接行為場景 → rapt-behavior（可選補）

輸出：docs/reports/rascore-report.md / rascore-scorecard.yml / rascore-findings.md / rascore-findings.json / rascore-precheck.json。

判讀：分數 ≥85 → 可作為 SSoT，允許進入後續推導（codegen / generate 階段）。

## Phase 1.5 增量補強（2026-06-13）

回應 verify NOTE（FIND-003/004/006）：
- 新增 `wishlist.ha.feature`（F-016，US-019，4 scenario）＋ `member-tier.ha.feature`（F-017，US-018，4 scenario）
- 清理 10 處 .feature 內聯 `# CiC` 殘留註解 → 改為決策引用（CLR-260613-*）
- story-index：US-018/019 轉 covered，feature 計數 15→17
- traceability：L1 US-018/019 covered，L2 +8 場景（SCN-WISH-001~004、SCN-TIER-001~004）

haBDD lint：17 feature 全過（0 ERROR / 0 WARN）。閘門 9/9 PASS。

保留中（合法）：member-tier ASM #015（門檻金額 deferred-needs-decision）、product-browsing 特價顯示（設計題、留 haPDL）。

> 註：verify-report NOTE FIND-003/004/006 已於本次處理；FIND-001/005（次要實體/報表 haAPI）仍待後續 rapt-intent 迭代。

## Phase 5 Verification 摘要（2026-06-13）

整體：**PARTIAL**（can_continue: true；0 blocker / 0 NEED_TO_FIX / 0 NEED_TO_CLARIFY；6 NOTE_ONLY）

四項驗證：完整性 PASS、跨 DSL 一致性 PASS（dsl-lint L1-L4 全過 0 ERROR/0 WARN）、可追蹤性 PARTIAL、覆蓋率 PASS（must-have 17/17=100%、feature→haAPI 14/15=93%）。

報告：`docs/reports/verify-report.md` + `verify-report.yml`。

NOTE_ONLY（皆後續迭代、非阻擋）：F-015 報表無 haAPI、product-browsing 讀取型由 list 承接、US-018 升降級 feature 待補、US-019 wishlist feature 待補、次要實體未產 haAPI、8 個 .feature 殘留 `# CiC` 註解。

RAscore Readiness：glossary/seeds/constraint 三項全 PASS → 具備 /rapt-RAscore 條件。

## Phase 4 Intent 摘要（2026-06-13；含次要實體增量）

產出（增量後）：
- **haAPI（22）**：核心 12（merchant, member, product, stock-item, cart, order, shipment, return-request, point-ledger, campaign, coupon, wishlist）＋ 次要 10（store, category, brand, product-variant, member-address, merchant-operator, platform-user, audit-log, notification-log, merchant-report）
- **haPDL（34）**：核心 20 ＋ 次要 14（category list/form、brand-form、product-variant-form、member-address list/form、merchant-operator list/form、platform-user list/form、audit-log-list、notification-log-list、store-form、merchant-report-dashboard）
- **traceability**：L3 Intent Mapping 共 40 列

增量回應 verify NOTE FIND-001（merchant-report haAPI，entity:Order 讀模型）+ FIND-005（次要實體 haAPI）→ 已結清。
sub-entity（OrderItem/CartItem/ProductImage/Invoice/Payment/Refund/CouponRedemption）仍折入其 aggregate operations。

dsl-lint：22 haAPI + 34 haPDL 全數 0 ERROR / 0 WARN（含 access v2 雙軌、一檔一頁、無 legacy 欄位）；全量四層 cross-DSL lint 亦 0 ERROR / 0 WARN。

跨 DSL 一致性：所有 haAPI `entity:` 對應 DBML Table（case-sensitive）；所有 haPDL `api:` 對應 haAPI id；所有 required_roles/permissions 與 permission_refs 對應現有 haARM id（**零 backfill**，無 BDY CiC）。

閘門檢查：5/5 PASS。

範圍註記（不阻擋 Phase 5）：
- 子實體（OrderItem/CartItem/ProductImage/Invoice/Payment/Refund/CouponRedemption/MemberAddress）折入其 aggregate 的 operations，未獨立產 haAPI。
- 次要/管理實體（Store/Category/Brand/PlatformUser/NotificationLog/AuditLog/MerchantOperator/ProductVariant）本輪未產獨立 haAPI，待後續迭代或 rapt-verify 評估覆蓋率。
- 單一介面實體（point-ledger/wishlist 僅 list、cart 僅 detail、member/shipment 僅 form）依性質未強制配 list+form。
- merchant_report（報表 view）未產 haAPI，讀模型待 generate 階段。

## Phase 3 Clarification 摘要（2026-06-13）

處理 13 CiC（9 GAP + 4 ASM；0 BDY/CON）→ 全數 RESOLVED。3 批 ASK session（CLR-260613-01/02/03）。

決策回寫 SSoT：
- **DBML**：+3 表（MerchantOperator、Wishlist、AuditLog → 28 表）；StockItem +reservedQuantity、PointLedger +expireAt；6 處 CiC 註解轉決策引用
- **seeds.md**：+3 值域（OperatorStatus、AuditActorType、AuditAction）；MemberTier/PlatformRole 解除 OPEN CiC
- **constraints.md**：+13 constraint（CON-STK-003、CON-ORD-002/006/008/011、CON-CPN-004、CON-RTN-001、CON-PNT-003/004/005、CON-MBR-003、CON-MOP-001、CON-WSH-001、CON-AUD-001）；移除 4 OPEN CiC
- **glossary.md**：+3 實體 +2 屬性術語（37 術語）
- **haARM**：+3 resource、+8 permission；修正 C2（member_create 移至 public）
- **traceability.md**：US-018/019 partial、US-020/021 deferred-mvp-out、新增 Decision Traceability（13 列）
- **discovery × 5 檔**：CiC 狀態同步段（RESOLVED + 決策引用）

關鍵 scope 變更（使用者決策）：願望清單入 MVP（新增 Wishlist）、一店多操作帳號（ASM#004 REJECTED → MerchantOperator）、通用稽核（AuditLog）。

閘門檢查：6/6 PASS。

殘留（不阻擋 Phase 4）：8 個 .feature 內聯 `# CiC` advisory 註解、wishlist.ha.feature、US-018 升降級 feature → 待 rapt-behavior 下輪；會員各級門檻金額 deferred-needs-decision（待平台提案）。

## Phase 2 Modeling 摘要（2026-06-13）

產出：
- `docs/ssot/dbml/schema.dbml`：25 Table、36 Ref、11 TableGroup（= Bounded Context）
- `docs/ssot/dbml/seeds.md`：17 個 ref_code 值域（PlatformRole、MemberTier 帶 OPEN CiC）
- `docs/ssot/dbml/constraints.md`：24 個 constraint（CON-*）＋ 4 個 OPEN CiC ＋ 4 個 compatibility decision（COMPAT-01~04）
- `docs/ssot/dbml/glossary.md`：33 術語＋ Canonical Mapping＋4 棄用詞
- `docs/ssot/haarm/smallBiz.haarm.yaml`：8 actor、5 role（public implicit）、26 resource、65 permission

閘門檢查：11/11 PASS；DBML / haARM 皆無 AP-01~AP-05 反模式

Bounded Context（11）：StoreMerchant、Catalog、Inventory、Shopping、Order、PaymentInvoice、Fulfillment、Returns、MembershipLoyalty、Promotion、Notification

授權落實：CON-ORD-009（消費者限自身訂單，memberId 條件）、CON-ORD-010（商家限自店訂單，storeId 條件）、CON-MER-003（店面狀態同步商家）

### Phase 2 新增 / 承接 CiC（待 rapt-clarify）

| CiC | 類型 | 位置 | 主題 |
|-----|------|------|------|
| GAP #006 | GAP | constraints.md#CON-STK-001 | 庫存扣減時點 / 預留釋放（StockItem 暫無 reservedQuantity）|
| GAP #007 | GAP | constraints.md#CON-ORD-008 | 金額計算順序 / 稅基口徑 |
| GAP #010 | GAP | seeds.md#MemberTier | 會員分級規則（四級暫定）|
| GAP #011 | GAP | constraints.md#CON-RTN-001 | 退貨期限 / 排除品項 / 退款路徑 |
| GAP #012 | GAP | schema.dbml#Shipment | 部分出貨（MVP 一單一出貨）|
| GAP #013 | GAP | constraints.md#稽核 | 稽核記錄範圍（目前無 AuditLog 表）|
| ASM #003 | ASM | seeds.md#PlatformRole | 平台 admin/marketer 角色拆分 |
| ASM #004 | ASM | schema.dbml#Merchant | 一店多操作帳號（MVP 一商家一帳號）|
| ASM #008 | ASM | constraints.md#CON-ORD-001 | 訂單狀態機觸發者（手動/自動）|
| ASM #014 | ASM | schema.dbml#ProductVariant | 原價設於 SKU 層級 |

## Phase 1.5 Behavior 摘要（2026-06-12）

產出：`docs/ssot/habdd/` 15 個 `*.ha.feature`（F-001~F-015，共 56 個 scenario）＋ `story-index.md`（21 stories＋Cross-Cutting Matrix）；`.raptor/traceability.md` L1/L2 草稿

閘門檢查：9/9 PASS；haBDD lint 15 檔全過（0 ERROR / 0 WARN）

新增 CiC：GAP #012（部分出貨）、GAP #013（稽核記錄）；高風險 scenario（涉 GAP #006/#007/#010/#011）已標 confidence: low 待 clarify

## Phase 1 Discovery 摘要（2026-06-12）

產出：`docs/discovery/00-source-inventory.md`、`01-stakeholders.md`、`02-user-journeys.md`、`03-event-timeline.md`、`04-vision-kpi-scope.md`

閘門檢查：6/6 PASS（3 份 source、8 個 stakeholder、40 個 domain events、vision、14 個 KPI、in/out/deferred 邊界）

### 未決 CiC 摘要（共 11 筆，內嵌於 discovery 文件）

| CiC | 類型 | 優先 | 主題 |
|-----|------|------|------|
| #006 | GAP | 高 | 庫存扣減時點 / 預留與釋放 / 未付款訂單逾時 |
| #007 | GAP | 高 | 折扣疊加規則與計算順序、稅基口徑 |
| #010 | GAP | 中 | 會員分級與點數細則（需平台提案） |
| #011 | GAP | 中 | 退換貨規則、已付款取消、券退還 |
| #005 | GAP | 中 | 平台管理員功能範圍 |
| #009 | GAP | 中 | 月租計費是否入 MVP |
| #002 | GAP | 低 | 願望清單是否入 MVP |
| #001/#003 | ASM | 中 | 平台端 admin/marketer 角色拆分 |
| #004 | ASM | 低 | 一店多操作帳號 |
| #008 | ASM | 中 | 訂單狀態機觸發者（手動/自動邊界） |
