# language: zh-TW
# source: docs/discovery/02-user-journeys.md#consumer的主要旅程1
# stories: US-002
# feature-id: F-002
Feature: 商品瀏覽與搜尋
  In order to 快速找到想買的商品
  As a 消費者
  I want to 瀏覽分類、搜尋商品並查看商品資訊

  Scenario: 瀏覽多層分類下的商品
    Given 商家已將商品上架於「3C → 手機 → 配件」的多層分類
    When 消費者瀏覽「手機」分類
    Then 顯示該分類與其子分類下的所有上架商品

  Scenario: 以關鍵字搜尋商品
    Given 店內有名稱含「保溫杯」的上架商品
    When 消費者以「保溫杯」搜尋
    Then 顯示名稱或描述相符的上架商品

  # CiC GAP（低）：特價顯示規則細節未決（PRD 1.5），呈現方式留待 haPDL 設計；原價/特價並列為已確認需求（訪談 2）
  Scenario: 商品頁顯示價格與庫存狀態
    Given 商品設有原價與特價且尚有庫存
    When 消費者查看該商品頁
    Then 同時顯示原價與目前售價
    And 顯示商品的庫存狀態
