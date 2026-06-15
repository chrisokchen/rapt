# language: zh-TW
# source: docs/discovery/00-source-inventory.md#CiC-GAP-002；CLR-260613-03#GAP#002
# stories: US-019
# feature-id: F-016
Feature: 願望清單
  In order to 延後購買想要的商品而不流失購買意願
  As a 消費者
  I want to 收藏商品並在降價時收到通知

  Background:
    Given 我已登入為消費者

  # scenario_id: SCN-WISH-001
  # entities: 願望清單, 商品
  Scenario: 將商品加入願望清單
    Given 某商品已上架
    When 消費者將該商品加入願望清單
    Then 該商品出現在消費者的願望清單

  # scenario_id: SCN-WISH-002
  # entities: 願望清單, 通知
  Scenario: 收藏商品降價時收到通知
    Given 消費者已將某商品加入願望清單
    When 該商品的售價調降
    Then 消費者收到該商品降價的通知

  # scenario_id: SCN-WISH-003
  # entities: 願望清單
  Scenario: 從願望清單移除商品
    Given 消費者的願望清單中有某商品
    When 消費者將該商品從願望清單移除
    Then 該商品不再出現在消費者的願望清單

  # scenario_id: SCN-WISH-004
  # entities: 願望清單, 商品
  Scenario: 重複收藏同一商品不重複建立
    Given 消費者的願望清單中已有某商品
    When 消費者再次將該商品加入願望清單
    Then 願望清單中該商品仍只有一筆
