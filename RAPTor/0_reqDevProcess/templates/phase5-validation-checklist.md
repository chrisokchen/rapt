# 驗證檢查清單模板

> **階段**: Phase 5 - 驗證確認
> **目的**: 系統化檢查規格的完整性與正確性

---

## 完整性檢查

### 需求涵蓋度
- [ ] 所有使用者故事都有對應的 BDD Scenario
- [ ] 所有 BDD Scenario 都有對應的 API 端點
- [ ] 所有 API 都有對應的 UI 頁面或系統流程
- [ ] 所有角色都有對應的 haARM role 定義
- [ ] 所有受保護的資源都有對應的 haARM resource 和 permission 定義
- [ ] 所有 haARM permission 都有至少一個 access_control 規則引用

### 場景完整性
- [ ] 正常流程場景 (Happy Path)
- [ ] 異常流程場景 (Error Handling)
- [ ] 邊界條件場景 (Edge Cases)

---

## 一致性檢查

### BDD ↔ API 一致性
- [ ] BDD 步驟對應正確的 API 端點
- [ ] API 回應格式符合 BDD 預期

### API ↔ UI 一致性
- [ ] UI 頁面使用正確的 API 端點
- [ ] 資料綁定正確

### haARM ↔ 各 DSL 一致性
- [ ] haPDL 的 auth.roles[] 中所有角色都在 haARM roles 中定義
- [ ] haAPI 的 @useAuth() 中所有權限都在 haARM permissions 中定義
- [ ] BDD Background 的 role 欄位都對應 haARM role.id
- [ ] haARM resource.id 與 DBML Table 名稱一致
- [ ] 無孤兒權限（haARM 中定義但無任何 DSL 引用的 permission）
- [ ] 無缺防護端點（haAPI 中有端點但未標註 @useAuth 的）

---

## 品質檢查

- [ ] 所有必要驗證規則已定義
- [ ] 錯誤訊息清晰易懂
- [ ] 權限控制完整（已與 haARM 交叉驗證）
- [ ] haARM constraints 已覆蓋所有業務規則中的互斥/依賴需求
- [ ] 效能需求已考慮
