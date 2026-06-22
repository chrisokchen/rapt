# Annotated DBML 規格 v3.3

**版本**: v3.3.0 (Release Candidate, 2026-05-13)
**最後更新**: 2026-05-13
**前版**: v3.2（見 `archive/annotated_DBML-v3.2.md`）

**版本沿革**：
- v1.1：正式化 Resolution Order 查找矩陣，新增 haAPI 作為查找來源
- v3.2：版本號對齊至 v3.2，Resolution Order 新增 Resilience 屬性、引用更新至 haAPI v3.2
- **v3.3：正式收編 `label:` / `ref_code:` / `sensitive:` / `group:` 為一級語法（Q9 決議）；`group:` 可被 haPDL 覆寫；移除「是否需要？」探索性標題**

**SSoT 主手冊**: 本檔即為 DBML 標註層 SSoT（Schema 本體請見 `benchmarks/DBML/*.dbml`）

---

## 0. 版本沿革

### 0.1 跨 DSL 版本歷程（v1.0 → v3.3）

| 版本 | 日期 | 主要變更 |
|------|------|---------|
| v1.0 | 2026-04 早期 | 初版規格分散建立（haARM v1、haAPI v1.0、haPDL v1.0、DBML v1.1） |
| v2.0 | 2026-04 中 | haARM：新增 `resources` 區段、`scope`、`$self`、`context:`、`TimeWindowCondition` |
| v3.0 | 2026-04 末 | haAPI 新增 `proxy`/`ext.*`/`logic`；haPDL 新增 State/Error/Async/A11y/Security/Testability |
| v3.1 | 2026-05 初 | haPDL：Scope Declaration、`security.permission_refs`、`datasource_scope` 雛形 |
| v3.2 | 2026-05-11 | haAPI Access v2 雙軌、PDL `permission_refs` 落地、DBML 四個自訂標註（探索性） |
| **v3.3** | **2026-05-13** | (a) DBML：`label:` / `ref_code:` / `sensitive:` / `group:` 升為一級語法（Q9）；`group:` 可被 haPDL 覆寫；移除「是否需要？」標題；(b) haARM 跳版 v3.3，新增 `starts_with`/`ends_with`；(c) Convention over Configuration 三段式；(d) 四 DSL 統一 12 章骨架；(e) 新增 `CROSS-DSL-GUIDE.md` |

### 0.2 v3.3 四 DSL 版本互鎖表

| DSL | 主檔（SSoT） | 規格檔 | 版本 | 對齊狀態 |
|-----|-------------|--------|------|---------|
| haAPI | `haAPIdoc.md` | `haAPI-specification_v3.3.md` | **v3.3.0** | Access v2 雙軌引用 haARM `permission.id`/`role.id` |
| haPDL | `haPDLdoc.md` | `haPDL-specification-v3.3.md` + `pdl-syntax-v3.3.md` | **v3.3.0** | `auth.roles[]` / `security.permission_refs` 對齊 haARM |
| haARM | `haARMdoc.md` | `haARM-Specification_v3.3.md` | **v3.3.0** | 新增 `starts_with`，引入 profile / auto_infer |
| DBML | `annotated_DBML-v3.3.md` | — | **v3.3.0** | 收編 4 個一級標註；與 haARM `resource.id` ↔ table 對齊 |

> **維護規則**：跨 DSL 版本升級時先寫入本 §0.1，再到各 *doc.md sync；不在各檔自行加非同步版本。Freeze 視窗起於 **2026-05-19**（凍結 EBNF/JSON Schema/欄位語意；文字、範例、速查卡不受限）。詳見 `ccwLog/0513-specsAlign_plan.md` §0 與 `ccwLog/0513-PQ_discuss.md` Q12。

### 0.3 章節骨架對照表（v3.3 統一 12 章）

> 本檔現行用中文編號「一、二、…十一、」，M0.3 階段先建對照表，實際轉換到 Arabic 「## 2. ... ## 11.」排程在 freeze 視窗結束後（>2026-05-26）。

| v3.3 標準章 | 標題 | 本檔現行位置 | 完工里程碑 |
|:----------:|------|------------|:---------:|
| 0 | 版本沿革 | §0（已就位） | ✅ M0.4 |
| 1 | 設計理念與定位 | §1.1（含原「一、定位」）+ §1.5 SSoT | ✅ M0.4 |
| 2 | 適用情境 | 散見於 §1.1 | ⏳ M0.3 後續 polish |
| 3 | EBNF / DBML 文法 | 採 dbdiagram.io 官方語法（外部規格） | — |
| 4 | JSON Schema 定義 | 無（DBML 非 JSON 結構） | — |
| 5 | 語義規則表（含 v3.3 4 個一級標註） | 「五、DBML v3.3 一級標註語法」（M0.5 已升為正式定義） | ✅ M0.5 |
| 6 | Convention over Configuration | 「十一、Resolution Order 查找矩陣」升為一級規則 | ⏳ M2.6 |
| 7 | 跨規格整合 | 散見於各章；補 hycms-ht002 範例 | ⏳ M3 |
| 8 | 完整範例 | 「八、實際範例：改造前後對比」 | M0.3 重排 |
| 9 | 驗證規則（含 §9.5 Anti-Pattern） | 「九、與既有 `note:` 的關係」+ 新 §9.5 | ⏳ M1（§9.5）+ M0.3 重排 |
| 10 | 工具支援與 Lint | 「七、轉換器的對應改動」 | M0.3 重排 |
| 11 | 遷移指引 | 「十、總結」+ 文末 TODO | M0.3 重排 |

---

## 1. 設計理念與定位

### 1.1 核心理念（DBML 在七規格體系中的定位）

七規格體系中 DBML 是星狀模型的中心：

```
          High-level Gherkin
               ↑
    haAPI  ←─ DBML ─→  haPDL
      ↓         ↓          ↓
  TypeSpec    Low-level   PDL
  /OpenAPI    Gherkin
```

每條連線都代表一個「推斷過程」：

- **DBML → haPDL/PDL**：欄位型別→表單輸入型別、顯示型別、驗證規則、中文標籤
- **DBML → haAPI/TypeSpec**：欄位型別→語言映射、PK→路由參數、FK→子資源 API
- **DBML → Gherkin**：Entity 名稱→步驟語彙、Enum 值→Given 條件範例
- **DBML → Linter**：欄位名稱/型別比對驗證

這些推斷規則目前散佈在：
- `convention.py`（~250 行推斷邏輯）
- `dbml_parser.py`（~150 行，含 `infer_input_type()` / `infer_column_type()`）
- ccwLog 中各 CodeGen 的型別映射表（3 份冗餘）

使用者的問題是：**能否在 DBML 本身加入足夠的語意標註，讓下游不需要猜？**

### 1.5 SSoT 主手冊宣告

**本文件為 DBML 標註層的 SSoT 主手冊**，PM/SA 與下游 codegen 對「DBML 自訂標註」的單一可信來源。

- 技術參考：本檔即為標註層完整規格（DBML 本體語法見 [dbdiagram.io 官方文件](https://dbml.dbdiagram.io)）
- Parser 實作：`haPDL/hapdl_converter/dbml_parser.py`（M0.5 擴展支援 v3.3 四個一級標註）
- 跨 DSL 整合：`CROSS-DSL-GUIDE.md`（v3.3 待建，詳見 M3）
- 與 haARM 引用：`resource.id` ↔ DBML table 名稱；`resource.fields[]` ↔ DBML column 名稱

三者描述衝突時**以本檔為準**；補充檔需於下次版本同步至本檔對應章節。

> M0.3 重排時，現行中文編號的「二、三、...十一、」會轉為「## 2. ... ## 11.」並對齊 12 章統一骨架。

---

### 二、現有 DBML 標註能力盤點

| 語法 | 來源 | 型別 | 範例 |
|------|------|------|------|
| `[pk]` | DBML 標準 | 結構化 | `id integer [pk]` |
| `[not null]` | DBML 標準 | 結構化 | `name varchar(100) [not null]` |
| `[unique]` | DBML 標準 | 結構化 | `email varchar(255) [unique]` |
| `[default: value]` | DBML 標準 | 結構化 | `[default: 'active']` |
| `[ref: > Table.field]` | DBML 標準 | 結構化 | `[ref: > Department.id]` |
| `[note: 'text']` | DBML 標準 | **自由文字** | `[note: '使用者類別']` |
| `[increment]` | DBML 標準 | 結構化 | `[pk, increment]` |
| `Enum Name { ... }` | DBML 標準 | 結構化 | `Enum bOnOff { Y; N }` |
| `Ref: A.x > B.y` | DBML 標準 | 結構化 | `Ref: Order.id < OrderItem.order_id` |
| **`[ref_code: 'ID']`** | **自定義** | 結構化 | `[ref_code: 'UserType']` ← 已使用 |

**關鍵發現**：DBML 的 `[...]` 括號內支援自定義鍵值對，`dbdiagram.io` 不認識但也不報錯。`ref_code` 就是利用這個機制的成功案例。

---

### 三、轉換器中的推斷規則分析

以下列出目前 `convention.py` 與 `dbml_parser.py` 中的所有推斷規則，分析每條是否適合用 DBML 標註取代：

#### 3.1 適合放入 DBML 的（Schema/Domain 語意）

| 推斷規則 | 目前邏輯 | 建議 DBML 標註 | 理由 |
|----------|---------|---------------|------|
| 動態列舉來源 | 無（需手動查 CodeMain） | `ref_code: 'UserType'` ✅ 已有 | 值域約束，屬於 schema |
| 靜態列舉定義 | `field.type == 'enum'` 時解析 | `Enum` 區塊 ✅ 已有 | 值域結構，屬於 schema |
| 中文欄位標籤 | 硬編碼字典 `{name: '名稱'}` | `note:` 已有描述但未解析 | 領域語言，適合放 DBML |
| 欄位精密度 | 無 | `decimal(15,2)` ✅ 已有 | 約束資訊，屬於 schema |
| 業務規則備註 | 無（僅在 DBML 註解中有） | 結構化 Table `Note:` | 領域規則，屬於 schema |

#### 3.2 灰色地帶（可放可不放）

| 推斷規則 | 目前邏輯 | 可行標註 | 考量 |
|----------|---------|---------|------|
| 是否為篩選欄位 | 黑白名單 + 型別判斷 | `filterable: true` | 是 UI 需求，但與資料查詢有關 |
| 欄位排序性 | haPDL `^` 符號 | `sortable: true` | 需建 index，與 DB 有關 |
| 欄位敏感性 | haPDL `*` 符號 + 名稱推斷 | `sensitive: true` | 安全性質，跨越 schema 與 UI |

#### 3.3 不適合放入 DBML 的（Presentation/UI 語意）

| 推斷規則 | 目前邏輯 | 為何不放 DBML |
|----------|---------|-------------|
| 表單輸入型別 | `enum→select, boolean→switch, text+email→email` | 同一欄位在不同頁面可能用不同輸入控制項 |
| 列表顯示型別 | `status+enum→badge, avatar→image, price→currency` | 顯示方式是 UI 決策，非資料屬性 |
| Enum 狀態顏色 | `active→success, pending→warning` | 視覺設計，會隨主題/品牌改變 |
| Action icon/variant | `create→plus/primary, delete→trash/danger` | 與 DBML 完全無關（是動作定義） |
| API 端點命名 | `CamelCase→kebab-case→plural` | 是路由慣例，不是資料模型 |
| 欄位寬度 | `id→80px, status→100px, _at→160px` | 純 UI 佈局 |

---

### 四、建議方案：三層語意分離

經上述分析，**不建議把所有東西都塞進 DBML**。正確做法是**三層各司其職**：

```
┌─────────────────────────────────────────────────────────┐
│  Layer 1：DBML（Schema & Domain 語意）                   │
│  ── 資料結構、值域約束、領域詞彙、業務規則               │
│  ── 所有下游 都能讀取的「不變的事實」                     │
│                                                         │
│  已有：pk, not null, unique, ref, default, Enum, note   │
│  建議新增：ref_code ✅, label:, sensitive:, group:      │
├─────────────────────────────────────────────────────────┤
│  Layer 2：haPDL（Intent & Convention 語意）               │
│  ── 頁面類型、欄位符號（!@#*）、動作定義、顯示提示       │
│  ── 會隨「UI 需求」變動的資訊                            │
│                                                         │
│  已有：符號語法、actions、features、view 配置            │
│  保持不變：:badge, |currency, filterable, sortable       │
├─────────────────────────────────────────────────────────┤
│  Layer 3：Convention Resolver（推斷引擎）                 │
│  ── 讀取 Layer 1 + Layer 2，推斷 Layer 1&2 都沒明確指   │
│     定的細節                                             │
│  ── 「慣例優於配置」的實現                                │
│                                                         │
│  保留：API 端點推斷、欄寬推斷、icon/variant 推斷         │
│  強化：讀取 DBML 新標註（label, ref_code）減少硬編碼      │
└─────────────────────────────────────────────────────────┘
```

**核心原則**：
- **DBML 只放「不會因 UI 需求改變的事實」** — 修改頻率最低
- **haPDL 放「頁面級的呈現意圖」** — 不同頁面可能不同
- **推斷引擎處理「沒有人明確指定的合理預設」** — 減少配置量

---

### 五、DBML v3.3 一級標註語法（正式收編）

> **v3.3 變更（Q9 決議）**：以下 4 個自定義屬性自 v3.3 起為 **DBML 一級語法**（不再標示為「建議」）。`haPDL/hapdl_converter/dbml_parser.py` 自 v3.3 起原生支援；對 dbdiagram.io 與其他 DBML 工具仍**保持向前相容**（未識別屬性會被忽略，不會報錯）。

**語法總表**：

| 標註 | 型別 | 必需 | 預設 | 來源優先序 | PM 何時填 |
|------|------|:----:|-----|----------|----------|
| `label:` | string | N | 由 `infer_field_label()` 推斷（v3.3 改為「DBML label 優先，推斷兜底」） | DBML label > 推斷字典 > Capitalize | 當欄位的 UI 顯示文字與英文欄位名差異大、或推斷字典不準確時填；常見於非英語系業務專案 |
| `ref_code:` | string（CodeMain key） | N | 無（無則不生成 select 與 JOIN） | 僅 DBML 一處宣告 | 該欄位值來自 CodeMain 動態列舉（如使用者類別、訂單狀態 code）時填；靜態 enum 用 DBML 原生 `enum` |
| `sensitive:` | boolean | N | `false` | 僅 DBML 一處宣告（資料本質屬性） | 該欄位涉及個資、密碼、金融資料時填 `true`；下游 UI 自動遮罩、API 自動排除回傳 |
| `group:` | string（group id） | N | 由 `infer_field_group()` 推斷 | **DBML group 為預設；haPDL `groups[]` 顯式宣告可覆寫**（Q9 例外） | 表格欄位需要在 form 頁面分區呈現時填（如「基本資訊/聯絡方式/系統欄位」）；推斷不準才需手動 |

各標註的範例與下游效果如下：

#### 5.1 `label:` — 欄位的顯示標籤（取代硬編碼字典）

```dbml
Table Order {
  order_number varchar(50) [unique, not null, label: '訂單編號']
  customer_name varchar(100) [not null, label: '客戶名稱']
  delivery_date date [label: '預計交貨日期']
  status enum(...) [not null, label: '訂單狀態']
  total decimal(15,2) [not null, label: '訂單總額']
}
```

**效果**：`convention.py` 的 `infer_field_label()` 改為「先查 DBML `label:`，找不到才用推斷字典」。

**好處**：
- 消除硬編碼 translations 字典（目前只有 20 個常見名稱，其餘全靠 `Capitalize`）
- 與 DBML `note:` 互補：`note:` = 開發者文件，`label:` = 使用者看的
- 實現通用語言 (Ubiquitous Language) 與 DBML 的統一

**vs `note:`**：OrderManage 的 DBML 已經在 `note:` 寫了中文描述（如 `[note: '訂單編號（業務用）']`），目前 parser 完全沒讀取。但 `note:` 通常包含較長的說明文字（如「訂單唯一識別碼 (UUID)」），不適合直接當 UI 標籤。分開用 `label:` 更精確。

#### 5.2 `ref_code:` — 動態列舉來源（已在使用，僅需標準化）

```dbml
Table InfoUser {
  userType nchar(1) [not null, ref_code: 'UserType', label: '使用者類別']
}
```

**現狀**：已在 ccwLog 討論中定案並在 erm.dbml 局部使用。需完成以下工作：
- 回填 5 個缺少標記的欄位
- 如果欄位有 `ref_code`，轉換器自動生成：
  - haPDL/PDL：`input: select` + `options.source: '/api/code-mains/{ref_code}'`
  - haAPI/TypeSpec：LEFT JOIN CodeMain

#### 5.3 `sensitive:` — 敏感欄位標記

```dbml
Table InfoUser {
  password varchar(255) [not null, sensitive: true, label: '密碼']
  id_number varchar(20) [sensitive: true, label: '身分證號']
}
```

**效果**：
- haPDL/PDL：自動遮罩顯示、表單用 password 輸入
- haAPI：回傳時自動排除或加密
- 安全性規格（v3.0 security section）：自動標記為需 field-level masking

**理由**：敏感性是**資料本質屬性**，不會因頁面而異。放在 DBML 確保所有下游一致處理。

#### 5.4 `group:` — 欄位邏輯分組

```dbml
Table Order {
  // 基本資訊
  order_number varchar(50) [unique, not null, group: 'basic', label: '訂單編號']
  customer_name varchar(100) [not null, group: 'basic', label: '客戶名稱']
  
  // 日期
  order_date date [not null, group: 'dates', label: '訂單日期']
  delivery_date date [group: 'dates', label: '預計交貨日期']
  
  // 金額
  total decimal(15,2) [not null, group: 'amount', label: '訂單總額']
  
  // 系統欄位
  created_at timestamp [not null, group: 'system', label: '建立時間']
  updated_at timestamp [not null, group: 'system', label: '更新時間']
}
```

**效果**：
- haPDL/PDL：form 頁面自動分區佈局（`group: 'basic'` → 第一個 section）
- 轉換器不需要靠欄位名稱猜測分組

**理由**：欄位分組反映**領域結構**（「基本資訊」「日期」「金額」是實體的邏輯結構），不是 UI 偏好。同一實體在不同頁面的分組方式通常一致。

#### 5.5 `group:` 的 haPDL 覆寫邏輯（Q9 例外）

雖然 §5.4 將 `group:` 定位為「領域結構」，但實務上同一實體在不同頁面（list / form / detail）可能有不同分組需求。v3.3 採取以下優先序：

```
haPDL `groups:` 明示宣告  →  DBML `group:` 預設  →  `infer_field_group()` 推斷
（最高優先）                  （次高）              （兜底）
```

- 大多數場景：PM/SA 在 DBML 寫一次 `group:`，所有下游頁面自動套用
- 例外場景：某個頁面需要不同分組，在 haPDL 顯式寫 `groups:` 覆寫
- 這與 Q6（profile_overrides 合併語意）一致：**有寫即取代，無寫即繼承**

---

### 六、不建議放入 DBML 的標註

以下屬性雖然技術上可以放入 DBML，但**不應該放**：

| 屬性 | 為何不放 DBML | 應放在哪裡 |
|------|-------------|-----------|
| `display: 'badge'` | 同欄位在 list 用 badge、在 form 用 select、在 detail 用 text — 與頁面類型有關 | haPDL 的 `:badge` 符號 |
| `input_type: 'textarea'` | 同欄位在不同表單可能用不同輸入控制項 | haPDL 符號 / Convention 推斷 |
| `color_map: {...}` | 顏色是視覺設計決策，會隨品牌/主題改變 | PDL theme / Convention 推斷 |
| `width: 100` | 純 UI 佈局，與資料無關 | Convention 推斷 |
| `filterable: true` | 同欄位可能在某些 list 頁面可篩選、某些不行 | haPDL view.filters |
| `sortable: true` | 同上 | haPDL view.features.sortable |
| `icon: 'user'` | 圖示是 UI 元素 | Convention 推斷 |

---

### 七、轉換器的對應改動

若採用上述方案，轉換器需要以下改動：

#### 7.1 `dbml_parser.py` — 擴展解析

```python
# 新增解析的自定義屬性
def _parse_field(self, name, type_str, constraints):
    # ... 現有解析 ...
    
    # 新增：解析 label
    label_match = re.search(r"label:\s*['\"]([^'\"]+)['\"]", constraints)
    label = label_match.group(1) if label_match else None
    
    # 新增：解析 ref_code
    ref_code_match = re.search(r"ref_code:\s*['\"]([^'\"]+)['\"]", constraints)
    ref_code = ref_code_match.group(1) if ref_code_match else None
    
    # 新增：解析 sensitive
    sensitive = 'sensitive:' in constraints and 'true' in constraints
    
    # 新增：解析 group
    group_match = re.search(r"group:\s*['\"]([^'\"]+)['\"]", constraints)
    group = group_match.group(1) if group_match else None
```

#### 7.2 `models.py` — 擴展 DBMLField

```python
@dataclass
class DBMLField:
    name: str
    type: str
    nullable: bool = True
    unique: bool = False
    primary_key: bool = False
    default: Optional[str] = None
    enum_values: List[str] = field(default_factory=list)
    references: Optional[str] = None
    # v3.0 新增
    label: Optional[str] = None       # 顯示標籤（中文）
    ref_code: Optional[str] = None    # 動態列舉來源
    sensitive: bool = False            # 敏感欄位
    group: Optional[str] = None       # 邏輯分組
```

#### 7.3 `convention.py` — 改為「標註優先、推斷兜底」

```python
def infer_field_label(self, field_name: str, dbml_field=None) -> str:
    # 1. 優先使用 DBML label 標註
    if dbml_field and dbml_field.label:
        return dbml_field.label
    
    # 2. 嘗試從 DBML note 提取（取第一句）
    if dbml_field and dbml_field.note:
        return dbml_field.note.split('（')[0].split('(')[0].strip()
    
    # 3. 兜底：推斷字典 + Capitalize
    return self._fallback_label(field_name)
```

---

### 八、實際範例：改造前後對比

#### Before（目前）— 推斷驅動

```dbml
// DBML 只有基礎資訊
Table Order {
  order_number varchar(50) [unique, not null, note: '訂單編號（業務用）']
  customer_name varchar(100) [not null]
  status enum('pending','confirmed','shipped','delivered','cancelled') [not null, default: 'pending']
}
```

```python
# convention.py 裡需要大量推斷
translations = {'name': '名稱', 'status': '狀態', ...}  # 20+ 個硬編碼
# order_number 不在字典中 → 只能輸出 "Order Number"（不理想）
```

#### After（建議）— 標註 + 推斷互補

```dbml
// DBML 加入語意標註
Table Order {
  order_number varchar(50) [unique, not null, label: '訂單編號', note: '業務用流水號，格式 ORD-yyyymmdd-nnn']
  customer_name varchar(100) [not null, label: '客戶名稱', group: 'basic']
  status enum('pending','confirmed','shipped','delivered','cancelled') [not null, default: 'pending', label: '訂單狀態', group: 'basic']
  password varchar(255) [not null, sensitive: true, label: '密碼']
  userType nchar(1) [not null, ref_code: 'UserType', label: '使用者類別']
}
```

```python
# convention.py 簡化為
def infer_field_label(self, field_name, dbml_field=None):
    if dbml_field and dbml_field.label:
        return dbml_field.label  # ← 直接用 DBML 的，不猜
    return self._fallback_label(field_name)  # ← 只有沒標的才猜
```

---

### 九、與既有 `note:` 的關係

| | `note:` | `label:` |
|---|---------|---------|
| **用途** | 開發者文件 | UI 顯示標籤 |
| **內容** | 可能很長：`'訂單唯一識別碼 (UUID)'` | 精簡：`'訂單編號'` |
| **讀者** | 看 DBML 的人、dbdiagram.io | 最終使用者（透過 UI） |
| **被轉換器使用** | 目前**未被解析** | 建議**直接解析** |
| **是否可選** | 是 | 是（沒有就走推斷） |

兩者互補，不衝突。`note:` 描述「是什麼」，`label:` 描述「叫什麼」。

### 9.5 常見誤用與反模式（Anti-Pattern, v3.3 新增）

> Q14 決議：Anti-Pattern 整合進驗證規則章節，dbml_parser 警告可直接引用本節編號。

| 編號 | 反模式 | 為何錯 | 正確寫法 |
|------|--------|--------|---------|
| **AP-01** | 用 `note: 'label:訂單編號\|group:basic'` 嵌入子格式 | v3.3 起 `label:`/`ref_code:`/`sensitive:`/`group:` 為一級語法（Q9）；嵌入式 micro-DSL 無型別保證、易拼錯 | 直接寫一級語法：`[label: '訂單編號', group: 'basic']` |
| **AP-02** | 同欄位同時寫 `ref_code: 'UserType'` 與 `ref: > UserType.id` | 語義衝突：`ref_code` 是動態 enum 列表來源（CodeMain），`ref:` 是 FK 關聯；兩者並存讓 codegen 無所適從 | 二擇一：值集合屬性用 `ref_code:`、關聯實體用 `ref:` |
| **AP-03** | `sensitive: false` 顯式寫出 | 預設即 false，冗餘且製造維護負擔（變更預設值時所有 false 都要清掉） | 省略；只在 `sensitive: true` 時寫 |
| **AP-04** | DBML 寫 `group: 'basic'`、haPDL 又重複寫同名 group | Q9 決議：DBML 為預設、haPDL 顯式宣告才覆寫。同值重複等於白寫，且 DBML 變更時 haPDL 不會跟 | DBML 宣告一次；haPDL 僅在「該頁面需不同分組」時寫 |
| **AP-05** | 把純 UI 偏好（color、icon、display_type）寫進 DBML | DBML 是 Schema/Domain SSoT，非 Presentation。同實體在不同頁面可能要不同 UI，DBML 寫死會破壞重用 | UI 偏好放 haPDL（`columns:` / `:badge` / `|date`）；DBML 只保留資料本質屬性 |

> **lint 觸發規則**：`dbml_parser.py` 在 v3.3 起警告 AP-01～AP-03（**warning**）；AP-04/AP-05 由 `validate_cross_dsl.py` 檢測（**hint**）。

---

### 十、總結

#### 回答：是否需要在 DBML 裡加標記？

**需要，但要克制。** 只加**領域語意**，不加 **UI 語意**。

#### 建議新增的 4 個標註

| 標註 | 性質 | 效果 | 優先級 |
|------|------|------|:---:|
| `label:` | 領域語言 | 消除硬編碼 translations；通用語言統一管理 | **P0** |
| `ref_code:` | 值域約束 | 動態列舉自動化（已有共識，需回填） | **P0** |
| `sensitive:` | 安全屬性 | 全鏈路敏感欄位一致處理 | P1 |
| `group:` | 領域結構 | Form 自動分區佈局 | P2 |

#### 不碰的部分

- ❌ 不加 `display:`、`input_type:`、`color_map:`、`width:`、`icon:` — 這些是 UI 決策，留給 haPDL + Convention
- ❌ 不加 `filterable:`、`sortable:` — 同欄位在不同頁面可能不同，留給 haPDL

#### 設計原則

> **DBML = 資料模型 + 領域詞彙 + 值域約束**
> **haPDL = 頁面意圖 + 呈現提示**
> **Convention = 合理預設 + 兜底推斷**

三者各司其職，標註是「配置」，推斷是「慣例」。**配置覆蓋慣例 (Configuration over Convention)**，而非取消慣例。使用者可以只寫 DBML 基礎結構（不加任何新標註），推斷引擎仍然能工作。加了標註後，推斷結果更精確。

```
查找順序：DBML 明確標註 → haPDL 符號/配置 → Convention 推斷 → 預設值
```

這就是「漸進式細化」——從簡單開始，需要精確時才加標註。

---

### 十一、Resolution Order 查找矩陣（正式定義）⭐ v1.1 · 更新 v3.2

> v1.0 提出了「查找順序」概念，v1.1 正式化為完整查找矩陣，並新增 **haAPI** 作為查找來源。v3.2 新增 Resilience 屬性。

**完整優先順序（左高右低）：**

```
① DBML 明確標註 → ② haAPI 定義 → ③ haPDL 符號/配置 → ④ Convention 推斷 → ⑤ 預設值
```

| 屬性 | ① DBML 標註 | ② haAPI 定義 | ③ haPDL 配置 | ④ Convention | ⑤ 預設值 |
|------|:---:|:---:|:---:|:---:|:---:|
| **欄位標籤** | `label:` | — | — | `translations{}` | `Capitalize` |
| **輸入型別** | — | — | 符號 `@[]{}` | `dbml_type→input` | `text` |
| **顯示型別** | — | — | 符號 `:badge` | `dbml_type→display` | `text` |
| **必填** | `[not null]` | — | 符號 `!` | — | `false` |
| **敏感** | `sensitive:` | `data_masking` | 符號 `*` | 名稱推斷 | `false` |
| **列舉來源** | `ref_code:` | `enum` in filters | — | — | — |
| **分組** | `group:` | — | section 配置 | — | 無分組 |
| **API 端點** | — | `exposes` | `api:` 引用 | CamelCase→kebab | — |
| **權限** | — | `access.permissions` | `auth.roles` | — | 無限制 |
| **MFA 需求** | — | `require_mfa` | — | — | `false` |
| **Resilience (timeout/retry)** | — | `ext.*` step / `advanced.external_resilience` / `codegen.config` | — | — | 框架內建值 |

**特殊合併規則：**

- **sensitive**：DBML ∪ haPDL（聯集，任一來源標記即生效）
- **權限**：haAPI `field_restrictions` 推導至 PDL `security.field_level.access_control`
- **MFA**：haAPI `require_mfa` 推導至 PDL `security.sensitive_operations.require_mfa`
- **Resilience** ⭐ v3.2：haAPI 專屬，採三層級聯（Step-level → API-level `advanced.external_resilience` → Project-level `codegen.config.yaml` → 框架內建預設）。haPDL/PDL 不直接參與此解析鏈。

> 此矩陣同步於 `haPDL-specification-v3.2.md` 附錄 C 與 `pdl-syntax-v3.2.md` 附錄 G。

---

**文件維護者**: WA-RAPTor 團隊
**最後更新**: 2026-04-02
**版本**: 3.2

---

## TODO（待辦事項）

### [2026-04-23] `not null` 欄位在 PATCH 語境下的「空值 = 不修改」語義

**來源**：`ccwLog/0423-UiTest_UserEdit-password.md`（密碼選填欄位驗證豁免問題）

**議題**：
DBML 的 `[not null]` 是 DDL 層級硬約束，但在 `update`/PATCH API 語境下，某些欄位（如 `password`）「空值」其實代表「保持原值」，而非違反 not null。若 codegen 直接把 DBML not null → DTO required，會導致前端無法送出空白 password 去更新其他欄位。

**行動項**：
- [ ] 新增 annotation 約定：`[note: 'patch_optional']` 或 `[patch_optional]` 以標記「PATCH 時可省略，不代表可存 null」
- [ ] 或透過 haAPI 層 `field_overrides` 表達（DBML 保持純 DDL 意圖，不污染）
- [ ] 在「DBML → haAPI field overrides」映射規則中，註明「Insert/Create 尊重 not null，Update/PATCH 依 haAPI override」
- [ ] 與 `pdl-syntax` 的 `skip_if_empty`、`haPDL` 的 `*?` 符號語義對齊

**優先度**：P2（DBML 保持語意純淨，改由上層 DSL 表達）

---

## 附錄 A: §6 Convention over Configuration（v3.3 新增；M3 重排時升為正式 §6）

> v3.3 統一章節骨架中 §6 為 Convention over Configuration（見 §0.3）。本附錄是 DBML 的 §6 內容；待 freeze 視窗結束（>2026-05-26）後由 M3 polish 升至正式編號。

### A.6.1 三段式優先序

```
   隱含預設值                慣例（DBML 標註）          明示覆寫
   (推斷字典 fallback)   →   (label/ref_code/...)    →   (haPDL 顯式宣告)
   ─────────────────────     ─────────────────         ──────────────────
   infer_field_label        label: '訂單編號'          haPDL columns 內 label
   sensitive=false           sensitive: true           haPDL form input=password
   group=null                group: 'basic'            haPDL groups 重排序
```

### A.6.2 Resolution Order 為一級規則

> **v3.3 變更**：將原 §十一「Resolution Order 查找矩陣」由附錄升為一級規則。

下游 codegen 在解析 DBML 欄位屬性時，必須按下表順序查找（先找到的勝出）：

| 屬性 | 查找順序（高 → 低） |
|------|-------------------|
| **label**（UI 顯示標籤） | (1) haPDL `columns:` / `fields:` 內 label → (2) DBML `label:` → (3) `convention.py` 推斷字典 → (4) `Capitalize(field_name)` |
| **input type**（表單輸入控件） | (1) haPDL `:type` 後綴 → (2) DBML enum/type → (3) `infer_input_type()` |
| **sensitive**（敏感欄位） | (1) DBML `sensitive: true`（v3.3 一級語法）→ (2) 欄位名含 `password`/`secret`/`id_number` 推斷 → (3) false |
| **ref_code**（動態列舉來源） | DBML `ref_code:` 為**唯一來源**（不推斷，不被 haPDL 覆寫） |
| **group**（欄位分組） | (1) haPDL `groups:` → (2) DBML `group:`（Q9 例外：haPDL 可覆寫）→ (3) `infer_field_group()` |
| **resilience**（API 韌性配置） | (1) haAPI step.resilience → (2) haAPI API.resilience → (3) `codegen.config.yaml` → (4) 框架預設 |

### A.6.3 DBML 4 個一級標註的 Convention 角色

| 標註 | Convention 角色 |
|------|----------------|
| `label:` | **預設層**：DBML 寫一次，所有下游 UI 套用 |
| `ref_code:` | **唯一事實源**：DBML 明示，無推斷 fallback |
| `sensitive:` | **預設層**：DBML 寫一次，所有下游遮罩 |
| `group:` | **預設層 + 可被 haPDL 覆寫**（Q9 例外：頁面層次有重排需求） |

### A.6.4 何時不該套 DBML Convention

| 情境 | 替代方案 |
|------|---------|
| UI 偏好（color/icon/display_type）| 放 haPDL；DBML 只保留資料本質屬性 |
| 多語系標籤 | DBML 寫主語言 label，i18n 在 haPDL/前端處理 |
| 同欄位在不同頁面用不同 group | DBML 寫主分組，haPDL 在需要的頁面覆寫 |
| 動態權限決定可見性 | 放 haARM（resource.fields）；不在 DBML 標 `visible_to:` |

### A.6.5 與 haARM/haPDL/haAPI 的引用對齊

| 跨 DSL 引用點 | DBML 端 | 對方 DSL |
|--------------|---------|---------|
| Table 名稱 | `Table InfoUser` | haARM `resource.id: users`、haAPI `entity: InfoUser` |
| Field 名稱 | `userId, deptId, ...` | haARM `resource.fields[]`、haAPI 與 haPDL 通用 |
| FK 關聯（`ref: >`） | `dept_id ref: > Department.id` | haAPI virtual_relations 子查詢計數 |
| 動態列舉（`ref_code:`） | `userType ref_code: 'UserType'` | haAPI LEFT JOIN CodeMain、haPDL select options |

詳見下方附錄 B 與 `8specDSLs/CROSS-DSL-GUIDE.md`（M3 已建立）。

---

## 附錄 B: §7 跨規格整合（v3.3 新增；M3 已落地）

> v3.3 統一章節骨架 §7 = 跨規格整合（見 §0.3）。完整跨 DSL 導覽請見 [`CROSS-DSL-GUIDE.md`](CROSS-DSL-GUIDE.md)；本節僅列 DBML 端的引用界面與 hycms-ht002 範例對應。

### B.7.1 DBML 是星狀模型的中心

```
              High-level Gherkin
                    ↑
         haAPI  ←─ DBML ─→  haPDL
           ↓        ↓          ↓
       TypeSpec   Low-level    PDL
       /OpenAPI   Gherkin
                   ↓
                 haARM（橫切面：透過 resource.id case-insensitive 匹配 DBML table）
```

### B.7.2 DBML 端的跨 DSL 引用點

| 引用點 | DBML 結構 | 被引用 DSL | 引用方式 |
|--------|----------|----------|---------|
| Table 名稱 | `Table <Name>` | haARM `resource.id`、haAPI `entity:` | case-insensitive 匹配 |
| Field 名稱 | `<field> <type>` | haARM `resource.fields[]` + condition.field、haPDL columns、haAPI list.filters | 名稱完全一致 |
| FK 關聯 | `ref: > Table.field` | haAPI `virtual_relations` 子查詢計數 | DBML 提供事實源 |
| 動態列舉 | `ref_code: '<key>'` | haAPI LEFT JOIN CodeMain、haPDL select options | v3.3 一級語法 |
| label/group/sensitive | v3.3 一級標註 | haPDL columns 顯示、PDL form input 推斷 | DBML 為預設，haPDL 可覆寫 group |

### B.7.3 hycms-ht002 範例對應

`benchmarks/DBML/hycms-ht002.dbml`：

```dbml
Table InfoUser {
  userId    nvarchar(60)  [pk, label: '使用者帳號', group: 'basic']
  deptId    nvarchar(20)  [label: '部門ID', group: 'basic']
  email     nvarchar(50)  [sensitive: true, label: '電子郵件', group: 'contact']
  ...
}
```

被引用點：

- **haARM** `resource.id: infouser` ← case-insensitive 匹配 `Table InfoUser`
- **haARM** `resource.fields: [userId, deptId, email, ...]` ← 必須是 DBML 欄位
- **haAPI** `entity: InfoUser` ← 對應 DBML Table（注意大小寫）
- **haPDL** columns 自動套用 DBML `label:` 與 `group:`（v3.3 一級標註，dbml_parser.py 原生支援）

跑 `python benchmarks/validate_cross_dsl.py hycms-ht002` 驗證引用一致性。

### B.7.4 與 `CROSS-DSL-GUIDE.md` 的關係

本節是 DBML 視角的引用清單；CROSS-DSL-GUIDE.md 是四 DSL 平面的完整對應表（含版本互鎖、Anti-Pattern、同步機制）。

---
