# Clarify Backlog

> 最後掃描：2026-06-13
> 初始 OPEN：13（9 GAP + 4 ASM）；BDY 0；CON 0
> 處理後 OPEN：0（全數 RESOLVED；3 項 deferred 已標明確狀態）

## GAP（資訊缺失，需人工回答）

| ID | 位置 | 描述 | 決策 | status |
|----|------|------|------|--------|
| GAP #006 | constraints.md#CON-STK-001 | 庫存扣減時點/預留釋放/付款期限 | 下單即預留+逾時釋放；72h（CLR-260613-01#Q1） | RESOLVED |
| GAP #007 | constraints.md#CON-ORD-008 | 金額計算順序/稅基口徑 | 活動→券→點數→運費→稅；稅基折後不含運（#Q2） | RESOLVED |
| GAP #011 | constraints.md#CON-RTN-001 | 退貨期限/退款路徑/取消/券退還 | 7天/原路/未出貨可取消/券退還（#Q3） | RESOLVED |
| GAP #010 | seeds.md#MemberTier | 會員分級+點數細則 | 四級依12月累計；效期1年/上限50%（#Q4） | RESOLVED |
| GAP #005 | 02-user-journeys.md | 平台管理員功能範圍 | 僅開通/停權+清單（CLR-260613-02#Q1） | RESOLVED |
| GAP #013 | constraints.md#CON-AUD-001 | 稽核記錄範圍 | 加 AuditLog（#Q3） | RESOLVED |
| GAP #009 | 04-vision-kpi-scope.md | 月租計費入 MVP | 不入 MVP（#Q2）→ deferred-mvp-out | RESOLVED |
| GAP #012 | schema.dbml#Shipment | 部分出貨 | 不支援（CLR-260613-03）→ deferred-mvp-out | RESOLVED |
| GAP #002 | story-index.md US-019 | 願望清單入 MVP | 入 MVP，新增 Wishlist（CLR-260613-03） | RESOLVED |

## ASM（假設，需確認）

| ID | 位置 | 假設內容 | 結果 | status |
|----|------|---------|------|--------|
| ASM #003 | seeds.md#PlatformRole | 平台拆 admin/marketer | CONFIRMED | RESOLVED |
| ASM #004 | schema.dbml#Merchant | 一商家一帳號 | REJECTED → 新增 MerchantOperator | RESOLVED |
| ASM #008 | constraints.md#CON-ORD-001 | 訂單狀態機觸發者 | CONFIRMED | RESOLVED |
| ASM #014 | schema.dbml#ProductVariant | 原價設於 SKU 層級 | CONFIRMED | RESOLVED |

## BDY（超界）／ CON（衝突）

（無）

## deferred 項目狀態（Phase 3 閘門要求）

| 項目 | 狀態 |
|------|------|
| 月租計費（GAP #009） | deferred-mvp-out |
| 部分出貨（GAP #012） | deferred-mvp-out |
| 多倉庫（US-020） | deferred-mvp-out |
| 會員各級門檻金額（GAP #010 子項） | deferred-needs-decision（待平台提案，不阻擋建模） |
| US-018 會員升降級 feature、US-019 wishlist feature | accepted-risk（實體已建模，feature 待 rapt-behavior 補） |

## 結構掃描發現（A1-A6 / B1-B5 / C1-C4）

| 規則 | 位置 | 問題 | 嚴重度 | 處理 |
|------|------|------|-------|------|
| A1-A6 | schema.dbml | 全數齊備 | — | 無 |
| B1-B5 | docs/ssot/habdd/** | 沿用 Phase 1.5 9/9 | — | 無 |
| C1 | merchant_report | view 無對應 Table（報表讀模型） | INFO | 刻意設計 |
| C2 | member_create | 原置於 consumer role scope:all | LOW | 已於 04 移至 public role |
| C3 | 01-stakeholders.md | user actor 皆有 role | — | 無 |
