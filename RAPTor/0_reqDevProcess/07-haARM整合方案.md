# haARM 需求發掘技術整合方案

> 本文件說明如何將 haARM v2（Actor-Role Modeling Language）整合到 0_reqDevProcess 目錄的七階段需求發掘與分析流程中

## 整合背景與目標

### 背景

WA-RAPTor 的需求發掘流程原有七個規格檔案，涵蓋從領域模型到測試規格的完整管線。然而，角色/權限/存取控制的定義散布在多處：
- haPDL 的 `auth.roles` 控制 UI 可見性
- haAPI 的端點定義中隱含存取控制
- Gherkin 的 `Given` 步驟假設角色
- 實作時習慣以 DB table（`urgp`、`ap`）直接管理權限

這導致權限定義缺乏規格層的集中管理，容易產生各 DSL 之間的不一致。

**概念起源**：參見 `0329-Actor-UserStory-AP_mapping.md`，該文件首次提出需要一種規格語言來建模 Actor-Role-Permission 的多對多映射關係。

### 整合目標

1. 將 haARM 作為**橫切面規格**整合進七階段流程，使角色/權限定義成為規格體系的一等公民
2. 建立 haARM 與其他 DSL（haPDL、haAPI、Gherkin、DBML）之間明確的引用規範
3. 在 Phase 5 驗證階段提供跨 DSL 的權限一致性檢查機制

---

## haARM 與原有流程的關係

### 定位差異

| 項目 | haPDL（參考 06-haPDL整合方案.md） | haARM |
|------|-------------------------------|-------|
| 定位 | 管線內的一站（Intent Layer #4） | **橫切面規格**，被多個 Phase 引用 |
| 管線位置 | Phase 4 規格制定的產出之一 | Phase 2 領域建模的產出，橫跨 Phase 2-7 |
| 引用方向 | 向下生成 PDL、Low-level Gherkin | 被 haPDL、haAPI、Gherkin 向上引用 |
| 類比 | 類似 haAPI（意圖層的一站） | 類似 DBML（橫切面的共用模型） |

### 在七規格體系中的位置

```
Intent Layer（意圖層）          Implementation Layer（實作層）
─────────────────────          ──────────────────────────────
1. DBML（領域模型）              5. TypeSpec/OpenAPI
2. High-level Gherkin            6. PDL（頁面實作規格）
3. haAPI（高階 API）             7. Low-level Gherkin
4. haPDL（高階頁面）

        ╔══════════════════════════════════════╗
        ║  haARM（橫切面：角色/權限/存取控制）      ║
        ║  被 #2, #3, #4, #6, #7 引用              ║
        ╚══════════════════════════════════════╝
```

haARM 不是第 8 號管線站，而是橫跨兩層的**共用定義**——角色與權限的 Single Source of Truth。

---

## 流程銜接點

### Phase 1 → Phase 2 銜接（角色候選萃取）

Phase 1 的 Event Storming 和 User Journey 產出中已包含角色相關資訊，在 Phase 2 轉化為 haARM 定義：

```
Phase 1 產出                      Phase 2 轉化
─────────────                    ─────────────
Event Storming 「相關角色」欄位 ──→ haARM actors（提取、去重、分類 type）
Event Storming 「命令」欄位 ──────→ haARM permissions 的 action 候選
User Journey Persona ────────────→ haARM actors 的 properties（補充屬性）
DBML entity ─────────────────────→ haARM resources（1:1 映射）
```

> **注意**：Phase 1 模板不做修改。角色到 haARM 的結構化轉化發生在 Phase 2，避免在業務探索階段過早引入 DSL 結構。

### Phase 2：建立 haARM（核心銜接點）

Phase 2 是建構 haARM 的最佳時機，因為此階段同時產出 DBML（與 haARM resource 1:1 映射）和通用語言詞彙表（角色名稱應納入）。

**新增產出物**：`<project>.haarm.yaml`

**關鍵活動**：
- 從 Phase 1 的 Event Storming 萃取 Actor 候選清單
- 識別角色層級關係與權限需求
- 建立 `.haarm.yaml` 定義 actors、roles、resources、permissions、access_control
- 確認 haARM resource 與 DBML entity 的對應關係
- 識別治理約束（互斥、依賴），填入 constraints（選填）

### Phase 4：引用 haARM

Phase 4 規格制定時，各 DSL 引用 haARM 中定義的角色與權限：

- **BDD Feature** 的 Background 角色欄位 → 引用 `haARM role.id`
- **haAPI / TypeSpec** 的 `@useAuth()` → 引用 `haARM permission.id`
- **haPDL** 的 `auth.roles[]` → 引用 `haARM role.id`

### Phase 5：驗證一致性

Phase 5 驗證階段新增 haARM 相關的檢查項目：

- **引用完整性**：haPDL、haAPI、Gherkin 中引用的角色/權限是否都在 haARM 中定義
- **孤兒檢測**：haARM 中定義但無任何 DSL 引用的權限
- **缺防護檢測**：haAPI 中有端點但未標註 @useAuth 的

---

## 跨 DSL 引用規範

### 引用對照表

| haARM 元素 | 引用方 | 對應欄位 | 範例 |
|-----------|--------|---------|------|
| `role.id` | haPDL | `auth.roles[]` | `auth.roles: [admin, merchant]` |
| `permission.id` | haAPI / TypeSpec | `@useAuth()` | `@useAuth("order_read")` |
| `actor.id` + `role.id` | Gherkin | `Given` 步驟 | `Given 我以 "john" (角色: customer_role) 登入` |
| `resource.id` | DBML | Table 名稱 | `resource.id: orders` ↔ `Table orders` |
| `constraint` | Gherkin | Scenario | 互斥約束對應 Negative BDD 場景 |

### 引用驗證規則

1. **所有引用必須可解析**：haPDL 的 `auth.roles[]` 中每個值都必須是 haARM 中已定義的 `role.id`
2. **Resource 與 DBML 對齊**：haARM 的 `resource.id` 應與 DBML 的 Table 名稱一致（允許 haARM 有額外的 action/view 類型 resource）
3. **權限無孤兒**：每個 haARM permission 至少被一個 haAPI 端點或 haPDL 頁面引用（否則發出 warning）
4. **端點無裸奔**：每個 haAPI 端點至少有一個 `@useAuth` 標註（除非明確標註為 public）

---

## 與 06-haPDL整合方案 的異同

### 共同點

- 都強調規格即 SSOT
- 都採用漸進式整合策略
- 都需要跨 DSL 的引用一致性驗證
- 都在 Phase 4 產出規格

### 差異點

| 面向 | haPDL 整合 | haARM 整合 |
|------|-----------|-----------|
| 進入流程的時機 | Phase 4（規格制定） | Phase 2（領域建模） |
| 在管線中的角色 | 產出者（向下生成 PDL、Low-level Gherkin） | 被引用者（被 haPDL、haAPI、Gherkin 引用） |
| 新增模板 | Phase 4 相關 | Phase 2（`phase2-access-control.haarm.yaml`） |
| 影響的驗證項目 | haPDL ↔ PDL 一致性 | haARM ↔ haPDL、haARM ↔ haAPI、haARM ↔ Gherkin、haARM ↔ DBML |

---

## 受影響的模板與文件

### 新增

| 檔案 | 說明 |
|------|------|
| `templates/phase2-access-control.haarm.yaml` | haARM v2 標準模板 |

### 修改（主要）

| 檔案 | 修改內容 |
|------|---------|
| `CLAUDE.md` | 規格體系、技術堆疊、文件導覽 |
| `README.md` | Phase 2 產出物、規格語言、三層域架構 |
| `templates/README.md` | 新增模板索引條目 |
| `templates/phase4-bdd-feature.feature` | Background 角色引用 haARM、新增權限 Scenario 範例 |
| `templates/phase4-api-spec.tsp` | 新增 @useAuth 裝飾器範例 |
| `templates/phase5-validation-checklist.md` | 新增 haARM 檢查項目 |
| `templates/phase5-consistency-matrix.md` | 新增 haARM ↔ 各 DSL 一致性區塊 |

### 修改（次要）

| 檔案 | 修改內容 |
|------|---------|
| `01-整體流程架構.md` | Phase 2 Mermaid 圖、品質閘門 |
| `02-階段詳解wAI.md` | AI 輔助 haARM 建模指引 |
| `03-技術與工具.md` | 技術堆疊新增 haARM |
| `05-範例-電商系統.md` | 電商 haARM 範例 |
| `templates/phase2-ubiquitous-language.md` | 使用場景新增 haARM |
| `templates/phase3-clarification-questions.md` | 新增權限澄清類別 |
| `templates/phase3-business-rules.md` | 新增存取控制規則範例 |
| `templates/phase4-page-spec.rui.yaml` | auth 區塊加引用提示 |
| `templates/phase5-traceability-matrix.md` | 新增 haARM 追溯矩陣 |

---

## 實施建議

### 優先順序

1. **立即**：建立本整合方案文件 + haARM 模板 + CLAUDE.md 更新
2. **短期**：Phase 4-5 模板更新（BDD、API、validation checklist、consistency matrix）
3. **視需要**：其餘流程文件與模板

### 注意事項

- haARM 模板為 Phase 2 的**選填**產出，不強制所有專案都必須產出
- 小型專案可僅填寫 actors + roles + permissions，省略 resources 和 constraints
- 與 DBML 的 resource 對應可在後續迭代中逐步完善

---

## 效益評估

| 面向 | 整合前 | 整合後 |
|------|-------|-------|
| 權限定義位置 | 散布在 haPDL、haAPI、Gherkin、DB table | haARM 集中定義，各 DSL 引用 |
| 一致性保證 | 人工核對，容易遺漏 | Phase 5 結構化驗證 |
| 角色建模時機 | 實作階段才建 DB table | Phase 2 領域建模階段前置 |
| 治理約束 | 無規格層機制 | haARM constraints 提供結構化定義 |
| 新人上手 | 需要理解散落各處的權限定義 | 一個 `.haarm.yaml` 檔案即可瞭解全貌 |

---

**版權聲明**：本文件屬於 WA-RAPTor 專案。
