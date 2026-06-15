# 需求發掘與分析流程 - 模板目錄

> 本目錄包含七階段需求發掘與分析流程的所有模板檔案

## 📁 模板索引

### Phase 1: 業務探索
- **[phase1-stakeholder-interview.md](phase1-stakeholder-interview.md)** - 利害關係人訪談模板
- **[phase1-user-journey-map.md](phase1-user-journey-map.md)** - User Journey Mapping 模板
- **[phase1-event-storming.md](phase1-event-storming.md)** - Event Storming 工作坊模板
- **[phase1-business-vision.md](phase1-business-vision.md)** - 業務願景文件模板

### Phase 2: 領域建模
- **[phase2-domain-model.dbml](phase2-domain-model.dbml)** - 領域實體模型模板 (DBML)
- **[phase2-ubiquitous-language.md](phase2-ubiquitous-language.md)** - 通用語言詞彙表模板
- **[phase2-bounded-contexts.md](phase2-bounded-contexts.md)** - 限界上下文模板
- **[phase2-aggregate-design.md](phase2-aggregate-design.md)** - 聚合設計模板
- **[phase2-access-control.haarm.yaml](phase2-access-control.haarm.yaml)** - 角色/權限/存取控制模型模板 (haARM v2)

### Phase 3: 需求澄清
- **[phase3-clarification-questions.md](phase3-clarification-questions.md)** - 澄清問題列表模板
- **[phase3-qna-session.md](phase3-qna-session.md)** - 問答會議記錄模板
- **[phase3-business-rules.md](phase3-business-rules.md)** - 業務規則清單模板

### Phase 4: 規格制定
- **[phase4-bdd-feature.feature](phase4-bdd-feature.feature)** - BDD Feature 文件模板 (Gherkin)
- **[phase4-api-spec.tsp](phase4-api-spec.tsp)** - API 規格模板 (TypeSpec)
- **[phase4-page-spec.rui.yaml](phase4-page-spec.rui.yaml)** - UI 頁面規格模板 (DSL)
- **[phase4-data-schema.dbml](phase4-data-schema.dbml)** - 資料模型規格模板 (DBML)

### Phase 5: 驗證確認
- **[phase5-validation-checklist.md](phase5-validation-checklist.md)** - 驗證檢查清單模板
- **[phase5-consistency-matrix.md](phase5-consistency-matrix.md)** - 一致性驗證矩陣模板
- **[phase5-traceability-matrix.md](phase5-traceability-matrix.md)** - 可追溯性矩陣模板
- **[phase5-coverage-report.md](phase5-coverage-report.md)** - 涵蓋率報告模板

### Phase 6: 原型生成
- **[phase6-prototype-plan.md](phase6-prototype-plan.md)** - 原型生成計畫模板
- **[phase6-codegen-config.yaml](phase6-codegen-config.yaml)** - 程式碼生成配置模板

### Phase 7: 迭代精煉
- **[phase7-user-testing-plan.md](phase7-user-testing-plan.md)** - 使用者測試計畫模板
- **[phase7-feedback-log.md](phase7-feedback-log.md)** - 反饋記錄模板
- **[phase7-iteration-plan.md](phase7-iteration-plan.md)** - 迭代計畫模板

## 🎯 使用指南

### 快速開始

1. **選擇適合的模板**: 根據當前所處階段選擇對應的模板
2. **複製模板**: 將模板複製到專案目錄中
3. **填寫內容**: 根據模板指引填寫專案實際內容
4. **與團隊協作**: 與團隊成員共同完善文件
5. **持續更新**: 隨著專案進展持續更新文件

### 模板使用原則

- ✅ **適應性調整**: 模板僅供參考,可根據專案特性調整
- ✅ **簡化優先**: 小型專案可簡化部分章節
- ✅ **持續演進**: 模板應隨著團隊實踐持續改進
- ✅ **工具整合**: 可結合 AI 工具輔助填寫模板

### 各階段模板選擇建議

| 專案規模 | 小型專案 (1-3人月) | 中型專案 (3-12人月) | 大型專案 (12+人月) |
|---------|-------------------|--------------------|--------------------|
| Phase 1 | 訪談模板 + 願景文件 | 全部 Phase 1 模板 | 全部 Phase 1 模板 + 詳細分析 |
| Phase 2 | 實體模型 + 詞彙表 | 全部 Phase 2 模板 | 全部 Phase 2 模板 + 多層次建模 |
| Phase 3 | 問答記錄 + 規則清單 | 全部 Phase 3 模板 | 全部 Phase 3 模板 + 多輪澄清 |
| Phase 4 | Feature + API 規格 | 全部 Phase 4 模板 | 全部 Phase 4 模板 + 完整覆蓋 |
| Phase 5 | 基礎檢查清單 | 檢查清單 + 矩陣 | 全部 Phase 5 模板 + 自動化驗證 |
| Phase 6 | Mock Server | Mock + UI 原型 | 全部 Phase 6 + 完整測試 |
| Phase 7 | 反饋記錄 | 測試計畫 + 反饋 | 全部 Phase 7 + 多輪迭代 |

## 🔗 相關資源

- **[05-範例：電商系統.md](../05-範例：電商系統.md)** - 完整的電商系統範例展示如何使用這些模板
- **[02-階段詳解wAI.md](../02-階段詳解wAI.md)** - 各階段詳細說明與實踐指南
- **[04-最佳實踐.md](../04-最佳實踐.md)** - 使用模板的最佳實踐

## 📝 貢獻模板

歡迎貢獻新的模板或改進現有模板：

1. 基於實際專案實踐提煉模板
2. 確保模板的通用性與適應性
3. 提供清晰的填寫指引與範例
4. 提交 Pull Request

---

**最後更新**: 2025-01-07
