# language: zh-TW
# source: docs/discovery/02-user-journeys.md#consumer的主要旅程1
# stories: US-003
# feature-id: F-003
Feature: 購物車
  In order to 彙整想買的商品並隨時湊單
  As a 消費者
  I want to 將商品加入購物車並管理內容

  Background:
    Given 我已登入為消費者

  # scenario_id: SCN-CART-001
  # entities: 購物車, 商品
  Scenario: 將上架商品加入購物車
    Given 某商品已上架且有庫存
    When 消費者將該商品加入購物車
    Then 購物車包含該商品

  # scenario_id: SCN-CART-002
  # entities: 購物車
  Scenario: 調整購物車內商品數量
    Given 購物車中已有某商品 1 件
    When 消費者將該商品數量調整為 3 件
    Then 購物車顯示該商品數量為 3 件

  # scenario_id: SCN-CART-003
  # entities: 購物車
  Scenario: 購物車跨裝置保留
    Given 消費者已在手機上將商品加入購物車
    When 消費者在電腦上登入並開啟購物車
    Then 購物車內容與手機上的內容一致

  # scenario_id: SCN-CART-004
  # entities: 購物車, 商品
  Scenario: 已下架商品無法加入購物車
    Given 某商品已被商家下架
    When 消費者將該商品加入購物車
    Then 加入不成立
    And 消費者收到商品已下架的提示
