# haARM 新手教學指南

**ha Actor-Role Modeling Language — Beginner's Guide**

**版本**: v1.0  
**日期**: 2026-06-24  
**適合對象**: 需求分析師、產品經理、系統設計師  
**前置知識**: 了解基本的使用者故事（User Story）、角色（Role）概念即可

---

## 目錄

1. [為什麼需要 haARM？](#為什麼需要-haarm)
2. [haARM 核心概念 5 分鐘速成](#haarm-核心概念-5-分鐘速成)
3. [最簡單的範例開始](#最簡單的範例開始)
4. [進階：逐步建立複雜規格](#進階逐步建立複雜規格)
5. [haARM 結構完整指南](#haarm-結構完整指南)
6. [實踐技巧與常見錯誤](#實踐技巧與常見錯誤)
7. [與 WA-RAPTor 的連接](#與-wraptor-的連接)
8. [常見問題 FAQ](#常見問題-faq)

---

## 為什麼需要 haARM？

想像你在設計一個「線上購物系統」。你可能會寫出這些使用者故事：

- **US-101**: 使用者可以查看商品清單
- **US-102**: 使用者可以將商品加入購物車
- **US-201**: 管理員可以上架新商品
- **US-202**: 管理員可以檢視銷售報表

**問題來了**：
- 「使用者」和「管理員」可以做什麼？
- 「查看商品」需要什麼權限？
- 一個人能同時是「收貨員」和「稽核員」嗎？
- 如何確保權限配置沒有漏洞或衝突？

**haARM 的用途**：用一份清晰的規格檔定義「誰」（角色）可以做「什麼」（權限），並自動檢查配置是否合理。

---

## haARM 核心概念 5 分鐘速成

### 1. **角色（Actor）**
- 系統中的使用者類型
- 例如：顧客、收貨員、管理員、稽核員

### 2. **權限（Permission）**
- 角色可以執行的動作
- 例如：查看清單、建立商品、刪除訂單

### 3. **使用者故事引用（Story Reference）**
- 權限與你的 User Story 綁定
- 讓權限具有業務背景

### 4. **約束規則（Constraints）**
- 定義哪些角色配置是「不允許」的
- 例如：同一人不能同時是收款員和稽核員

### 5. **驗證（Validation）**
- haARM 會自動檢查規格是否違反約束

---

## 最簡單的範例開始

### 範例 1：極簡線上購物系統

假設你的系統只有兩個角色和一個故事。

```yaml
metadata:
  version: "1.0"
  name: "Simple E-Commerce RBAC"
  description: "最簡單的購物系統角色權限模型"
  created: "2026-06-24"
  owner: "產品經理 - 王小明"

actors:
  - id: A01
    name: "顧客"
    description: "已登入的系統使用者"
    
  - id: A02
    name: "管理員"
    description: "系統管理員，具有全部權限"

roles:
  - id: R01
    name: "customer-user"
    actor: A01
    description: "購物顧客角色"
    
  - id: R02
    name: "system-admin"
    actor: A02
    description: "系統管理員角色"

permissions:
  - id: P01
    name: "browse-products"
    description: "瀏覽商品清單"
    operation: "Read"
    resource: "Product"
    
  - id: P02
    name: "manage-products"
    description: "上架、編輯、下架商品"
    operation: "Write"
    resource: "Product"

participation-matrix:
  - story: "US-101"
    role: R01
    permissions: [P01]
    rationale: "顧客需要瀏覽可購買的商品"
    
  - story: "US-201"
    role: R02
    permissions: [P01, P02]
    rationale: "管理員需要管理所有商品"
```

**這個範例告訴系統**：
- 有 2 個角色（顧客、管理員）
- 顧客只能瀏覽商品（P01）
- 管理員可以瀏覽和管理商品（P01 + P02）

### 怎麼驗證這份規格？

目前這份規格很簡單，沒有衝突。但當你加入約束規則時，驗證就變得重要了。

---

## 進階：逐步建立複雜規格

### 範例 2：加入更多角色和權限

現在加入「收貨員」和「稽核員」角色。

```yaml
metadata:
  version: "1.1"
  name: "E-Commerce with Operations"
  description: "包含訂單和金流處理的角色模型"
  created: "2026-06-24"

actors:
  - id: A01
    name: "顧客"
    description: "購物使用者"
    
  - id: A02
    name: "管理員"
    description: "系統管理員"
    
  - id: A03
    name: "收貨員"
    description: "負責接收和記錄訂單"
    
  - id: A04
    name: "稽核員"
    description: "負責稽核金流和訂單合規"

roles:
  - id: R01
    name: "customer"
    actor: A01
    
  - id: R02
    name: "admin"
    actor: A02
    
  - id: R03
    name: "receiving-clerk"
    actor: A03
    
  - id: R04
    name: "auditor"
    actor: A04

permissions:
  # 顧客權限
  - id: P01
    name: "browse-products"
    operation: "Read"
    resource: "Product"
    
  - id: P02
    name: "create-order"
    operation: "Write"
    resource: "Order"
    
  - id: P03
    name: "view-own-order"
    operation: "Read"
    resource: "Order"
    constraint: "owner-only"  # 只能看自己的訂單
  
  # 收貨員權限
  - id: P04
    name: "view-all-orders"
    operation: "Read"
    resource: "Order"
    
  - id: P05
    name: "mark-order-received"
    operation: "Write"
    resource: "Order"
    
  # 稽核員權限
  - id: P06
    name: "view-financial-reports"
    operation: "Read"
    resource: "FinancialReport"
    
  - id: P07
    name: "approve-large-payment"
    operation: "Approve"
    resource: "Payment"
    threshold: 100000  # 10 萬以上的付款需要稽核
    
  # 管理員權限
  - id: P08
    name: "manage-roles"
    operation: "Write"
    resource: "Role"

participation-matrix:
  - story: "US-101"
    role: R01
    permissions: [P01]
    rationale: "顧客瀏覽商品"
    
  - story: "US-102"
    role: R01
    permissions: [P02, P03]
    rationale: "顧客建立訂單並查看"
    
  - story: "US-301"
    role: R03
    permissions: [P04, P05]
    rationale: "收貨員接收訂單"
    
  - story: "US-401"
    role: R04
    permissions: [P06, P07]
    rationale: "稽核員檢查財務和大額支付"
    
  - story: "US-501"
    role: R02
    permissions: [P01, P02, P03, P04, P05, P06, P07, P08]
    rationale: "管理員有所有權限"

constraints:
  separation-of-duty:
    - name: "收貨與稽核分離"
      rule: "NOT (R03.has_permission(P05) AND R04.has_permission(P07))"
      rationale: "同一人不應同時接收訂單和稽核付款，避免舞弊"
      severity: "high"
      
  mutual-exclusion:
    - name: "稽核員不能是收貨員"
      rule: "EXCLUSIVE(R03, R04)"
      rationale: "職責分離原則"
      severity: "critical"

  mandatory-assignment:
    - name: "每個故事必須有至少一個角色"
      rule: "FORALL story IN participation-matrix: COUNT(assigned_roles) >= 1"
      rationale: "故事必須有負責人"
      severity: "high"
```

**新增內容說明**：

1. **更多角色**：增加收貨員、稽核員
2. **更多權限**：區分讀取、寫入、核准操作
3. **約束規則**：定義哪些角色配置不允許
   - `separation-of-duty`：職責分離
   - `mutual-exclusion`：相互排斥
   - `mandatory-assignment`：強制分配

### 這份規格的好處

✅ 清楚看到每個角色的權限  
✅ 約束規則明確定義了組織政策  
✅ 可以自動化驗證是否有漏洞  
✅ 新團隊成員一眼看懂權限結構

---

## haARM 結構完整指南

### 結構 1：元資料（Metadata）

```yaml
metadata:
  version: "1.0"                    # haARM 版本（遵循 SemVer）
  name: "系統名稱"                  # 易讀的系統名字
  description: "簡短說明"            # 這個角色模型的用途
  created: "2026-06-24"             # 建立日期
  updated: "2026-06-25"             # 最後更新日期（可選）
  owner: "負責人名字"                # 誰維護這份規格
  namespace: "com.company.system"   # 命名空間（可選，用於跨系統引用）
```

### 結構 2：角色（Actors）

```yaml
actors:
  - id: A01
    name: "customer"
    display_name: "顧客"             # 友善的中文名稱
    description: "購物系統的使用者"
    type: "human"                    # "human" 或 "system"
    scope: "external"                # "external"（外部）或 "internal"（內部）
```

**角色（Actor）** vs **角色類型（Role）** 的區別：
- **Actor** = 實際的人或系統（「顧客」「員工」「外部API」）
- **Role** = 系統中的職位名稱（「customer-user」「warehouse-manager」）

一個 Actor 可能扮演多個 Role。

### 結構 3：角色類型（Roles）

```yaml
roles:
  - id: R01
    name: "customer-user"           # 程式化名稱（kebab-case）
    display_name: "購物顧客"
    actor: A01                       # 參考到哪個 Actor
    description: "在線購物的註冊用戶"
    priority: 10                     # 可選：優先順序（用於報表）
```

### 結構 4：權限（Permissions）

```yaml
permissions:
  - id: P01
    name: "read-order"
    description: "查看訂單詳情"
    operation: "Read"                # CRUD 操作類型
    resource: "Order"                # 資源名稱
    
    # 可選的進階欄位
    scope: "own"                     # "own"（只限自己）或 "all"（全部）
    condition: "status == 'active'"  # 加入條件判斷
    rationale: "支援查單功能"
    ref-story: ["US-102"]            # 相關的 User Story ID
```

**Operation 的標準值**：
- `Read` – 查看資訊
- `Write` – 建立或編輯
- `Delete` – 刪除
- `Approve` – 核准
- `Execute` – 執行指令

### 結構 5：參與矩陣（Participation Matrix）

這是 haARM 最重要的部分，連接故事、角色、權限。

```yaml
participation-matrix:
  - id: PM-001                      # 可選：唯一識別符
    story: "US-102"                 # 參考的 User Story ID
    role: R01                        # 這個故事需要的角色
    permissions: [P01, P02]          # 這個角色在故事中需要的權限
    priority: "high"                 # 可選：優先順序
    status: "active"                 # "active"、"pending"、"deprecated"
    rationale: "顧客需要查看和建立訂單"
    
    # 進階欄位
    constraints: []                  # 特定於此參與的額外約束
    dependencies: ["US-101"]         # 前置故事
```

### 結構 6：約束規則（Constraints）

約束規則定義「什麼配置是不允許的」。

#### 6.1 職責分離（Separation of Duty）

```yaml
constraints:
  separation-of-duty:
    - id: SOD-001
      name: "請款與稽核分離"
      rule: "NOT (R03.has_perm(P05) AND R04.has_perm(P07))"
      description: "同一人不能既請款又稽核"
      rationale: "避免舞弊風險"
      severity: "critical"           # "low", "medium", "high", "critical"
      source-regulation: "內控規定 3.2"  # 法規或政策來源
```

#### 6.2 相互排斥（Mutual Exclusion）

```yaml
  mutual-exclusion:
    - id: MX-001
      name: "稽核員不能是操作員"
      rule: "EXCLUSIVE(R03, R04)"   # R03 和 R04 不能同時指派給同一人
      description: "檢查者和執行者必須分開"
      severity: "high"
```

#### 6.3 基數約束（Cardinality）

```yaml
  cardinality:
    - id: CARD-001
      name: "至少一個系統管理員"
      rule: "COUNT(R02) >= 1"        # R02（管理員）至少要有一個人
      description: "系統必須有人維護"
      severity: "critical"
      
    - id: CARD-002
      name: "最多三個管理員"
      rule: "COUNT(R02) <= 3"
      description: "避免權力過度集中"
      severity: "medium"
```

#### 6.4 自訂約束（Custom）

```yaml
  custom:
    - id: CUST-001
      name: "經理級需有兩年經驗"
      rule: "role == R02 IMPLIES employee.experience >= 2"
      description: "組織內部要求"
      severity: "high"
      tool-hint: "需要人力資源系統輔助驗證"
```

---

## 實踐技巧與常見錯誤

### ✅ 最佳實踐

#### 1. 從 User Story 開始

**錯誤**：直接寫「我們需要顧客、員工、管理員三個角色」

**正確**：
1. 先寫使用者故事
2. 為每個故事標記「誰」執行它
3. 從中提取出角色和權限

```
US-101: 顧客可以瀏覽商品
  → 誰執行？顧客
  → 需要什麼權限？read-product

US-201: 管理員上架新商品
  → 誰執行？管理員
  → 需要什麼權限？create-product, update-product
```

#### 2. 明確的權限命名

**不好** ❌：
```yaml
permissions:
  - id: P01
    name: "access"
    operation: "Read"
```

**好** ✅：
```yaml
permissions:
  - id: P01
    name: "view-order-list"
    operation: "Read"
    resource: "Order"
    scope: "all"
```

為什麼？因為「access」太模糊，而「view-order-list」清楚描述了做什麼、對什麼資源、範圍是什麼。

#### 3. 約束規則必須有「為什麼」

**不好** ❌：
```yaml
constraints:
  mutual-exclusion:
    - rule: "EXCLUSIVE(R03, R04)"
```

**好** ✅：
```yaml
constraints:
  mutual-exclusion:
    - rule: "EXCLUSIVE(R03, R04)"
      rationale: "稽核員和操作員分離，遵循內控原則"
      source-regulation: "財務管理規定 § 5.2"
      owner: "首席財務官"
```

為什麼？因為三個月後，新來的人會問「為什麼不能一個人同時做兩個角色？」規格必須能回答這個問題。

#### 4. 使用 Story ID 建立可追溯性

```yaml
participation-matrix:
  - story: "US-102"
    role: R01
    permissions: [P02, P03]
    ref-api: "haAPI::POST /orders"   # 也可以交叉引用 haAPI
```

這樣，你可以反向追蹤：
- 故事 US-102 需要哪些權限？
- 權限 P02 在哪些故事中被使用？
- 哪個 API 端點需要哪些角色？

---

### ❌ 常見錯誤

#### 錯誤 1：角色和權限混淆

```yaml
# ❌ 錯誤
roles:
  - id: R01
    name: "can-view-orders"   # 這是權限，不是角色
    
# ✅ 正確
roles:
  - id: R01
    name: "customer-support"  # 這是角色
    
permissions:
  - id: P01
    name: "view-orders"       # 這是權限
```

**記住**：
- **角色** = 職位（「收銀員」「經理」「審計員」）
- **權限** = 能力（「刪除訂單」「查看銷售報表」）

#### 錯誤 2：過度細粒度權限

```yaml
# ❌ 太細了
permissions:
  - id: P01
    name: "view-order-id"      # 分到每個欄位
  - id: P02
    name: "view-order-date"
  - id: P03
    name: "view-order-amount"
    
# ✅ 合理粗度
permissions:
  - id: P01
    name: "view-order-details" # 整體看訂單
    resource: "Order"
    operation: "Read"
```

**為什麼**？太細會導致管理複雜度爆炸。除非有特殊業務需求（如「財務不能看銷售額」），否則應該分組。

#### 錯誤 3：遺漏約束規則

```yaml
# ❌ 有潛在風險
actors:
  - A01: "顧客"
  - A02: "收貨員"
  - A03: "稽核員"

# 但沒定義：「收貨員和稽核員不能同一人」
# 這會讓系統允許舞弊配置

# ✅ 加入約束
constraints:
  mutual-exclusion:
    - rule: "EXCLUSIVE(R02, R03)"
      rationale: "避免收貨員自己稽核自己的訂單"
```

#### 錯誤 4：參與矩陣的故事 ID 不存在

```yaml
# ❌ 危險
participation-matrix:
  - story: "US-999"    # 這個故事在 haPDL 中不存在
    role: R01
    permissions: [P01]

# ✅ 正確
# 先確認 US-102 在你的 haPDL 中已定義
participation-matrix:
  - story: "US-102"
    role: R01
    permissions: [P01]
```

**驗證方法**：haARM 驗證工具應該檢查所有 `story` 引用是否真實存在（使用 Z3 SMT solver 或簡單的交叉檢查）。

#### 錯誤 5：不清楚的角色範圍

```yaml
# ❌ 模糊
actors:
  - id: A01
    name: "管理員"
    
# ✅ 清楚
actors:
  - id: A01
    name: "系統管理員"
    type: "human"
    scope: "internal"
    description: "內部 IT 部門的系統維護人員，負責維護應用系統和資料庫"
```

---

## 與 WA-RAPTor 的連接

### haARM 在 WA-RAPTor 中的位置

```
組織層級            規格層級              代碼層級
┌──────────┐      ┌──────────┐        ┌──────────┐
│ haPDL    │      │ User     │        │ Feature  │
│ (功能)   │  →   │ Story    │  →     │ Flag     │
└──────────┘      └──────────┘        └──────────┘
     ↓                 ↓                   ↓
┌──────────┐      ┌──────────┐        ┌──────────┐
│ haARM    │      │ Role +   │        │ RBAC     │
│ (角色)   │  →   │ Permission  │  →   │ Code     │
└──────────┘      └──────────┘        └──────────┘
     ↓                 ↓                   ↓
┌──────────┐      ┌──────────┐        ┌──────────┐
│ haAPI    │      │ Endpoint │        │ REST API │
│ (接口)   │  →   │ with Auth│  →     │ Server   │
└──────────┘      └──────────┘        └──────────┘
```

### 從 haARM 自動生成的產物

#### 1. 自動生成 Gherkin 權限測試場景

haARM 可以生成 BDD 測試：

```gherkin
# 自動生成自 haARM 規格
Feature: 顧客訂單權限驗證

  Scenario: 顧客可以查看自己的訂單
    Given 用戶 "alice" 以 "customer" 角色登入
    When alice 要求查看訂單 "ORD-2024-001"
    Then 應該成功返回訂單詳情
    
  Scenario: 顧客不能刪除訂單
    Given 用戶 "alice" 以 "customer" 角色登入
    When alice 嘗試刪除訂單 "ORD-2024-001"
    Then 應該拒絕並返回 403 Forbidden
    
  Scenario: 稽核員和操作員不能同一人
    Given 系統配置了用戶角色
    When 嘗試將用戶 "bob" 同時指派為 "receiving-clerk" 和 "auditor"
    Then 應該違反約束 "EXCLUSIVE(R03, R04)"
```

**效益**：自動化測試確保系統權限實現與規格一致。

#### 2. 自動生成 DBML 資料模型

haARM 可以生成資料庫設計：

```sql
-- 自動生成自 haARM 規格
Table user_roles {
  user_id INT
  role_id VARCHAR(50)
  assigned_date DATETIME
  assigned_by VARCHAR(100)
  
  primary key (user_id, role_id)
  foreign key (role_id) references roles(id)
}

Table roles {
  id VARCHAR(50) [primary key]
  name VARCHAR(100)
  description TEXT
  actor_id VARCHAR(50)
}

Table role_permissions {
  role_id VARCHAR(50)
  permission_id VARCHAR(50)
  story_id VARCHAR(50)
  
  primary key (role_id, permission_id)
  foreign key (role_id) references roles(id)
  foreign key (permission_id) references permissions(id)
}

Table permissions {
  id VARCHAR(50) [primary key]
  name VARCHAR(100)
  operation VARCHAR(20)  -- 'Read', 'Write', 'Delete', 'Approve'
  resource VARCHAR(100)
}
```

#### 3. 交叉引用到 haAPI

haARM 可以標記出哪個 API 端點需要什麼角色：

```yaml
# haARM 中
participation-matrix:
  - story: "US-102"
    role: R01
    permissions: [P02]
    ref-api: "haAPI::POST /orders"  # 交叉引用
    
# 對應到 haAPI 中
endpoints:
  - path: "/orders"
    method: POST
    required-role: R01
    required-permissions: [P02]
    generated-from: "haARM::US-102"
```

**效益**：API 端點自動帶上權限標籤，後續可生成 OpenAPI 規格的授權段落。

---

## 常見問題 FAQ

### Q1：我應該寫多詳細的 haARM？

**A**：看你的團隊規模和複雜度。

- **簡單系統**（< 5 角色）：只需基本的參與矩陣 + 1-2 個約束
- **中等系統**（5-20 角色）：詳細的權限定義 + 3-5 個分離約束 + 部分自訂約束
- **複雜系統**（> 20 角色）：完整的元資料 + 所有約束類型 + 定期稽核計畫

### Q2：haARM 要存在哪裡？

**A**：
- **版本控制**：放在 Git（同 haPDL、haAPI）
- **位置**：`specs/rbac/system-name.haarm.yaml`
- **自動驗證**：CI/CD 中加入 haARM 驗證步驟

```bash
# 在 GitHub Actions 中
- name: Validate haARM
  run: |
    python3 -m haarm.validator specs/rbac/system-name.haarm.yaml
    python3 -m haarm.z3_checker specs/rbac/system-name.haarm.yaml
```

### Q3：如何從舊系統遷移到 haARM？

**A**：分階段：

1. **第一步**：梳理現有角色和權限，列出清單
2. **第二步**：寫出最簡單的 haARM（只有 actors, roles, permissions）
3. **第三步**：加入 participation-matrix，連接到使用者故事
4. **第四步**：逐步加入約束規則，邊加邊驗證

```yaml
# 第一次迭代：最小可行規格
metadata: {...}
actors: [A01, A02]
roles: [R01, R02]
permissions: [P01, P02, P03]

# 第二次迭代：加入參與矩陣
participation-matrix: [...]

# 第三次迭代：加入約束
constraints:
  separation-of-duty: [...]
  mutual-exclusion: [...]
```

### Q4：規格寫好後，我該怎麼用？

**A**：三個用途：

1. **需求溝通**：展示給利益相關者（業務、法務），確認需求正確
2. **自動化測試**：生成 Gherkin 場景，測試系統權限
3. **代碼生成**：生成資料庫 schema、API middleware、RBAC 設定檔

### Q5：多個系統共用相同的角色怎麼辦？

**A**：使用命名空間和引用：

```yaml
# system-a.haarm.yaml
metadata:
  namespace: "com.company.system-a"

actors:
  - id: A01
    name: "company-admin"
    namespace: "com.company.shared"  # 引用共用角色

# system-b.haarm.yaml
metadata:
  namespace: "com.company.system-b"

actors:
  - ref: "com.company.shared::A01"   # 直接引用而不重複定義
```

### Q6：如何驗證我寫的 haARM 規格？

**A**：使用 haARM 驗證工具（Z3 SMT solver）：

```bash
# 安裝
pip install haarm-validator

# 驗證語法和邏輯
haarm validate my-system.haarm.yaml

# 檢查約束是否可滿足（使用 Z3）
haarm check-constraints my-system.haarm.yaml

# 生成報告
haarm report my-system.haarm.yaml --format=html
```

### Q7：Gherkin 場景應該寫得多詳細？

**A**：最少必須涵蓋：

✅ **必須有**：
- 正面案例：有權限的角色可以執行
- 負面案例：無權限的角色被拒絕
- 約束驗證：違反約束的配置被攔截

✅ **視情況新增**：
- 邊界案例：權限的閾值檢查（如「100萬以上需核准」）
- 異常狀況：系統故障時的降級行為

```gherkin
# 完整的場景套
Scenario: 正面 - 收貨員可以標記訂單已收貨
  Given 收貨員已登入
  When 收貨員標記訂單為已收貨
  Then 訂單狀態更新為 "received"

Scenario: 負面 - 顧客不能標記訂單已收貨
  Given 顧客已登入
  When 顧客嘗試標記訂單為已收貨
  Then 系統拒絕並返回 403

Scenario: 約束 - 不允許同時配置為收貨員和稽核員
  When 系統管理員嘗試將用戶同時指派兩個角色
  Then 驗證失敗 (EXCLUSIVE constraint violated)

Scenario: 邊界 - 超過 100 萬的付款需要稽核員核准
  Given 待付款金額為 150 萬
  When 收貨員確認付款
  Then 系統要求稽核員核准
```

---

## 快速檢查清單

在完成 haARM 規格前，確認你已完成這些：

- [ ] **Metadata**：版本號、建立日期、負責人都有填
- [ ] **Actors**：列出所有系統使用者類型（人類 or 系統）
- [ ] **Roles**：角色名稱清楚、與 Actor 有正確對應
- [ ] **Permissions**：每個權限都有明確的 operation 和 resource
- [ ] **Participation Matrix**：每個 User Story 都有對應的角色和權限
- [ ] **Constraints**：至少有 1-2 個分離或排斥約束
- [ ] **可追溯性**：可以回答「為什麼這個角色需要這個權限？」
- [ ] **交叉引用**：參與矩陣中的 Story ID 都在 haPDL 中存在
- [ ] **驗證**：用工具驗證過規格沒有語法或邏輯錯誤
- [ ] **文件**：有足夠的註釋讓他人理解

---

## 下一步

閱讀完本指南後，建議：

1. **找一個簡單的子系統**（如「權限管理模組」）試著寫 haARM
2. **與利益相關者討論**：確認規格反映了真實業務需求
3. **加入 CI/CD**：設定自動驗證流程
4. **迭代優化**：隨著系統發展，定期更新 haARM

如有問題，查閱進階文件：
- `haARM-Specification.md` – 完整語法參考
- `haARM-Z3-Constraint-Validation.md` – 約束驗證詳解

---

## 範例檔案清單

本指南提供的完整範例：

```
examples/
├── 1-simple-ecommerce.haarm.yaml        # 最簡單的例子
├── 2-ecommerce-with-operations.haarm.yaml  # 進階版本
├── 3-complex-enterprise.haarm.yaml      # 複雜企業系統
├── test-cases/
│  ├── valid-constraints.haarm.yaml
│  └── invalid-constraints.haarm.yaml   # 用來學習常見錯誤
└── generated/
   ├── gherkin-scenarios.feature
   ├── database-schema.sql
   └── api-permissions.openapi.yaml
```

---

**版本歷史**

| 版本 | 日期 | 異動 |
|------|------|------|
| 1.0 | 2026-06-24 | 初版發布 |

**文件維護**  
如有建議或發現錯誤，請聯絡 WA-RAPTor 框架團隊。
