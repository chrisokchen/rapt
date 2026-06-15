# Stakeholders

> 來源：00-source-inventory.md（構想書 §4 目標使用者、訪談記錄 1-3、PRD §0 範圍說明）

## 角色列表

| id | 名稱 | 類型 | 系統中的角色 |
|----|------|------|------------|
| consumer | 消費者 | user | 在商家前台店面瀏覽、購買、追蹤訂單、累點與退貨 |
| merchant | 商家（店主） | user | 經營自己的線上商店：商品、庫存、訂單、促銷、報表 |
| platform-admin | 平台管理員 | user | 管理全平台商家帳號與營運狀態 |
| platform-marketer | 平台行銷/營運人員 | user | 幫商家代操或指導促銷活動、優惠券設定 |
| payment-gateway | 金流服務商 | external | 處理信用卡 / PayPal 支付，支付資訊不落地 |
| logistics-provider | 物流業者（貨運行） | external | 收件、配送、提供物流追蹤狀態 |
| einvoice-service | 電子發票加值服務 | external | 開立發票、5% 營業稅申報資料 |
| notification-channel | 通知通道（LINE / Email） | external | 推送訂單狀態與行銷通知給消費者 |

## 各角色詳細描述

### consumer — 消費者
- **類型**：user
- **系統角色**：在商家店面前台選購商品、結帳付款、查訂單與物流進度、使用優惠與點數、線上申請退貨。
- **輪廓**（構想書 §4 角色 B + 訪談 2）：25-40 歲上班族，9 成用手機，對購物體驗很挑。
- **主要關切**：網站快（>2-3 秒就離開）、找東西方便、付款安全、訂單進度可見、退貨簡單。
- **痛點**：付款後才被通知缺貨（最強烈負面情緒點）、結帳必填欄位過多、優惠併用規則藏小字、紙本退貨流程冗長。

### merchant — 商家（店主）
- **類型**：user
- **系統角色**：租用平台開店；管理商品上下架、庫存、訂單出貨、促銷設定、查看報表。
- **輪廓**（構想書 §4 角色 A + 訪談 1）：35-50 歲實體店主，技術程度低（「聽到架站、金流串接就頭痛」），目前 Excel 記庫存＋LINE/Email 接單。
- **主要關切**（依張老闆自述優先序）：① 庫存即時同步 ② 折扣自動算對 ③ 訂單狀態一畫面看完 ④ 看得懂的簡單報表。
- **痛點**：庫存對不上導致超賣道歉、人工算折扣常錯、漏單與重複出貨、發票稅金不會算。
- **附帶約束**：「不要讓我動腦」→ 後台 UX 必須極簡；月費可接受 2-3 千元。

### platform-admin — 平台管理員
- **類型**：user
- **系統角色**：平台側管理商家（開通、停權）、確保權限區隔（商家只能管自己的店、消費者只能看自己的訂單，PRD §0）。
- **主要關切**：商家活躍度與留存（構想書 KPI）、平台整體營運健康。
- **痛點**：source 中著墨少，職能細節待補。

### platform-marketer — 平台行銷/營運人員
- **類型**：user
- **系統角色**：幫商家代操或教學促銷活動與優惠券（構想書角色 C＋訪談 3 林經理）。
- **主要關切**：三種促銷工具齊備且可設檔期自動上下架、優惠券防濫用（最低門檻、張數上限）、分級行銷（券限會員等級）。
- **痛點**：折扣疊加規則不明會導致商家虧錢回頭怪平台；無門檻券外流被薅羊毛（前公司事故）。

### 外部系統（external）

| id | 互動方式 |
|----|---------|
| payment-gateway | 結帳時請求付款（信用卡/PayPal）、回傳付款結果；轉帳採「匯款後五碼」人工對帳模式 |
| logistics-provider | 商家標記出貨後取得物流單號；消費者可查配送進度；退貨時上門取件 |
| einvoice-service | 訂單成立後自動計算 5% 營業稅並開立發票 |
| notification-channel | 訂單狀態變更時推送 LINE / Email 通知 |

## CiC 便條

<!-- CiC ASM #003 -->
**類型**：ASM
**位置**：docs/discovery/01-stakeholders.md#角色列表
**描述**：假設 platform-marketer 與 platform-admin 為平台端兩個不同角色（PRD 僅列「平台管理員」一類）。承接 00-source-inventory.md CiC ASM #001。
**影響**：haARM roles、後台權限設計
**推薦**：clarify 確認平台端是否需要 admin / marketer 權限分離
<!-- /CiC -->

<!-- CiC ASM #004 -->
**類型**：ASM
**位置**：docs/discovery/01-stakeholders.md#merchant
**描述**：訪談 1 顯示同一家店由老闆與老闆娘兩人共同操作（曾因資訊不同步重複出貨），假設一個商家帳號之下需要多個操作者（店主＋店員），但 source 未明文要求。
**影響**：DBML 商家/使用者模型、haARM merchant 角色細分
**推薦**：clarify 確認 MVP 是否支援一店多操作帳號
<!-- /CiC -->

## CiC 狀態同步（Phase 3 Clarification，2026-06-13）

- **ASM #003 → RESOLVED / CONFIRMED**（CLR-260613-03#ASM#003）：平台端拆分 platform-admin 與 platform-marketer 兩角色。
- **ASM #004 → RESOLVED / REJECTED**（CLR-260613-03#ASM#004）：使用者要求**支援一店多操作帳號**，已新增 MerchantOperator 實體（CON-MOP-001）。
