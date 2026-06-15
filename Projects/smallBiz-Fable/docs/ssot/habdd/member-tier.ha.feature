# language: zh-TW
# source: docs/discovery/04-vision-kpi-scope.md#CiC-GAP-010；CLR-260613-01#Q4
# stories: US-018
# feature-id: F-017
Feature: 會員等級
  In order to 讓回購多的會員獲得對應的等級權益
  As a 消費者
  I want to 依累計消費自動升降等級並享有等級權益

  Background:
    Given 我已登入為消費者

  # scenario_id: SCN-TIER-001
  # entities: 會員, 會員等級
  # CiC ASM #015：各等級的「累計消費門檻金額」待平台提案（GAP #010 deferred-needs-decision）；本 feature 以「次一等級門檻」為規則層變數，不寫死金額
  Scenario: 近一年累計消費達門檻時升級
    Given 會員目前等級為一般會員
    And 會員近 12 個月累計消費達到次一等級的門檻
    When 系統執行會員等級評定
    Then 會員等級升為次一等級

  # scenario_id: SCN-TIER-002
  # entities: 會員, 會員等級
  Scenario: 累計消費未達門檻時維持原等級
    Given 會員目前等級為一般會員
    And 會員近 12 個月累計消費未達次一等級的門檻
    When 系統執行會員等級評定
    Then 會員等級維持不變

  # scenario_id: SCN-TIER-003
  # entities: 會員, 會員等級
  Scenario: 累計消費下滑時降級
    Given 會員目前等級為金級會員
    And 會員近 12 個月累計消費已低於金級的維持門檻
    When 系統執行會員等級評定
    Then 會員等級降為符合其累計消費的等級

  # scenario_id: SCN-TIER-004
  # entities: 會員, 會員等級, 優惠券
  Scenario: 升級後可使用等級限定優惠券
    Given 存在一張限定金級會員使用的優惠券
    And 會員已升級為金級會員
    When 會員於結帳時套用該優惠券
    Then 系統接受該優惠券的使用資格
