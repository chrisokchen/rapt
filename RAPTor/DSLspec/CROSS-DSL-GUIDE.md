# WA-RAPTor 跨規格整合導覽（CROSS-DSL-GUIDE）

> **本文件是四個 DSL 的整合入口**，給 PM/SA 與 codegen 實作者：先看這裡了解四 DSL 如何串成端對端規格，再回各 *doc.md 看細節。
>
> **版本**：v3.3.0（與四 DSL 同步升版）
> **建立**：2026-05-14（M3.1 落地）
> **SSoT 主手冊**：本檔為跨規格層 SSoT；各 DSL 細節以對應 *doc.md 為準

---

## 0. 版本互鎖表

> 任何時候四 DSL 必須在同一版本平面上。跨 DSL 升版時，先寫入此表再到各 *doc.md sync。

| DSL | 主檔（SSoT） | 規格檔 | 版本 | 升版日 |
|-----|-------------|--------|------|-------|
| haAPI | [`haAPIdoc.md`](haAPIdoc.md) | [`haAPI-specification_v3.3.md`](haAPI-specification_v3.3.md) | **v3.3.0** | 2026-05-14 |
| haPDL | [`haPDLdoc.md`](haPDLdoc.md) | [`haPDL-specification-v3.3.md`](haPDL-specification-v3.3.md) + [`pdl-syntax-v3.3.md`](pdl-syntax-v3.3.md) | **v3.3.0** | 2026-05-14 |
| haARM | [`haARMdoc.md`](haARMdoc.md) | [`haARM-Specification_v3.3.md`](haARM-Specification_v3.3.md) | **v3.3.0** | 2026-05-14 |
| DBML | [`annotated_DBML-v3.3.md`](annotated_DBML-v3.3.md) | — | **v3.3.0** | 2026-05-14 |

**Freeze 視窗**：2026-05-19 起 freeze EBNF/JSON Schema/欄位語意；文字、範例、速查卡不受限。詳見 `ccwLog/0513-specsAlign_plan.md` §0 與 `ccwLog/0513-PQ_discuss.md` Q12。

---

## 1. 七個跨 DSL 引用點

下表列出四 DSL 之間所有**ID 級引用界面**。跨 DSL 修改時，必須先確認此表的引用關係不破。

| # | 引用點 | 來源 DSL | 來源欄位 | 目標 DSL | 目標欄位 | 語義 |
|:-:|--------|---------|---------|---------|---------|------|
| 1 | DBML Table 名稱 | DBML | `Table <Name>` | haARM | `resource.id`（case-insensitive） | RBAC 資源對應實體 |
| 2 | DBML Field 名稱 | DBML | `<field> <type>` | haARM | `resource.fields[]` + `condition.field` | 欄位級權限 / 條件 |
| 3 | DBML Table 名稱 | DBML | `Table <Name>` | haAPI | `entity:` | API 對應實體 |
| 4 | haARM permission.id | haARM | `permissions[].id` | haAPI | `access.endpoints.{op}.required_permissions[].id` | API 端點權限引用 |
| 5 | haARM role.id | haARM | `roles[].id` | haAPI | `access.endpoints.{op}.required_roles[]` + haPDL `auth.roles[]` | 端點/頁面權限引用 |
| 6 | haARM constraint.id | haARM | `constraints[].id` | haAPI | `access.endpoints.{op}.conditions[].haarm_constraint` | API 端點條件引用（opaque ref） |
| 7 | haAPI api: id | haAPI | `api:` 頂層欄位 | haPDL | `api:` 頂層欄位 | 頁面綁定 API |

### 1.1 引用方向圖

```
   DBML (Schema/Domain)
     │       │
     ▼       ▼
  ┌──────┐  ┌──────────────────┐
  │ haARM│  │ haAPI            │  ── 引用點 #3,#7 ──>  haPDL
  │      │←─┤ required_perms   │                        │
  │      │  │ required_roles   │                        │
  │      │  │ haarm_constraint │  ←────── 引用點 #5 ────┤ auth.roles
  └──────┘  └──────────────────┘                        │
     ▲                                                  │
     └────────────── 引用點 #5 ──────────────────────────┘
                    （haPDL auth.roles → haARM role.id）
```

### 1.2 為何採 ID 級引用，不採內聯？

- **單一事實源**：權限規則只能寫在 haARM 一處；haAPI/haPDL 內聯權限邏輯 = 雙重事實源 = 維護地獄
- **codegen 友善**：codegen 看到 `id: foo_bar` 即可去 haARM YAML 查完整定義，不必跨檔 reasoning
- **lint 容易**：跨 DSL 引用完整性可由 `haarm-lint --validate-cross-dsl` 一鍵驗證
- **跨團隊分工**：DBA 改 DBML、Auth team 改 haARM、API team 改 haAPI、Frontend 改 haPDL，各自不互相阻擋

---

## 2. 端對端範例：hycms-ht002

> 本範例展示「同一業務情境」如何同時體現在四個 DSL 上。所有檔案使用相同 anchor `hycms-ht002`，由 `validate_cross_dsl.py hycms-ht002` 一鍵驗證引用一致性。

### 2.1 業務情境

hyCMS HT002「使用者管理」：

- 主管（htsd）只能看自己單位與下屬單位的使用者（部門前綴樹隔離，`deptId starts_with $self.department_id`）
- 系統管理員（sysadm）可全域 CRUD
- 稽核員（audit）只能讀，且與 sysadm 互斥（SoD）

### 2.2 四 DSL 檔案

| DSL | 檔案 | 角色 | 行數 |
|-----|------|------|:---:|
| DBML | [`benchmarks/DBML/hycms-ht002.dbml`](../benchmarks/DBML/hycms-ht002.dbml) | 資料層：InfoUser + Dept 兩 table 帶 v3.3 一級標註 | ~30 |
| haARM | [`benchmarks/haARM/hycms-ht002.haarm.yaml`](../benchmarks/haARM/hycms-ht002.haarm.yaml) | 橫切面：3 roles、1 resource (`profile: dept_isolated_crud`)、6 permissions、1 constraint | ~100 |
| haAPI | [`benchmarks/haAPI/hycms-ht002.haapi.yaml`](../benchmarks/haAPI/hycms-ht002.haapi.yaml) | API：standard CRUD + export operation；Access v2 雙軌引用 haARM | ~95 |
| haPDL | [`benchmarks/haPDL-v3.2/hycms-ht002.hapdl.yaml`](../benchmarks/haPDL-v3.2/hycms-ht002.hapdl.yaml) | 頁面：type=list；auth.roles + security.permission_refs 引用 haARM | ~60 |

### 2.3 跨檔引用對照

```
DBML Table InfoUser
  │
  ├── haARM resource.id: infouser          （#1 case-insensitive）
  │     ├── fields: [userId, deptId, ...]  （#2 必須是 DBML 欄位）
  │     ├── profile: dept_isolated_crud    （v3.3 §3.10）
  │     └── permissions:
  │           infouser_read, infouser_create, infouser_update, infouser_delete, infouser_export
  │
  ├── haAPI entity: InfoUser                （#3）
  │     ├── api: hycms-ht002
  │     └── access.endpoints.{op}:
  │           required_permissions: [infouser_*]   （#4）
  │           required_roles: [htsd, sysadm, audit] （#5）
  │
  └── haPDL api: hycms-ht002                 （#7 必須匹配 haAPI api:）
        ├── auth.roles: [htsd, sysadm, audit] （#5）
        └── security.permission_refs:
              view/edit/delete → infouser_* （#4）
```

### 2.4 驗證

```bash
$ python benchmarks/validate_cross_dsl.py hycms-ht002

============================================================
  四 DSL 跨規格一致性驗證：hycms-ht002
  根目錄：D:\0wk\hyRAPTor\benchmarks
============================================================

✅  無問題，四 DSL 引用一致。
```

---

## 3. 同步維護機制

### 3.1 何時必須跑 `validate_cross_dsl.py`？

**強制**：

- 任何 `.haarm.yaml` 改動 → 對所有引用該檔的 anchor 跑一次
- 任何 `.haapi.yaml` 改動 `entity:` / `access.{permissions, roles}` → 跑
- 任何 `.hapdl.yaml` 改動 `api:` / `auth.roles[]` / `security.permission_refs[]` → 跑
- 任何 `.dbml` table/field 改名 → 跑（檢查 haARM resource.fields 是否還對得起來）

**選用**：

- DBML 內 `note:`、`label:`、`group:` 等標註改動：不影響跨 DSL 引用，可不跑
- haARM constraints 改動：對 haAPI `haarm_constraint` 引用有影響時才跑

### 3.2 流程：新增一個跨 DSL anchor（如 `hycms-ht002`）

> Q10 決議流程：AI 產初稿 → `validate_cross_dsl.py` 零 error → Chris 審 → 索引到本檔。

```
1. AI 用既有檔（erm.dbml + aisystem.haarm.yaml + info-user.haapi.yaml + ugrpList.hapdl.yaml）
   為上下文，生成四個 hycms-ht002.* 初稿（一次 prompt）
2. python benchmarks/validate_cross_dsl.py hycms-ht002
   要求：零 error 才算初稿通過
3. Chris 審查業務語意正確性
4. 把四個檔案路徑加入本檔 §2.2 範例索引表
```

### 3.3 既有同步工具

| 工具 | 位置 | 作用 |
|------|------|------|
| `validate_cross_dsl.py` | `benchmarks/validate_cross_dsl.py` | 自動檢查六條跨規格引用規則 |
| `cross-dsl-sync.instructions.md` | `0_prompts/Common/cross-dsl-sync.instructions.md` | Copilot 編輯 benchmark 時自動載入的 SOP |
| `haarm-lint --validate-cross-dsl` | （M4 規劃中）| 讀 `cross_dsl_anchor` 驗證四 DSL 同 anchor 存在 |

### 3.4 為何不做「自動 hook」？

此專案是文件/規格專案（非程式碼庫），沒有 git pre-commit hook 環境。最輕量且可持續的做法：

- ✅ 人工觸發的腳本（已建立：`validate_cross_dsl.py`）
- ✅ AI 的 instructions 提醒（已建立：`cross-dsl-sync.instructions.md`）
- ⏳ 未來若加入 CI（GitHub Actions），可在 `on: push` 時執行 `validate_cross_dsl.py` 自動驗證

---

## 4. 跨 DSL 反模式（Anti-Pattern）

> 各 *doc.md §9.5（或對應節）有 DSL 內部的 Anti-Pattern；此節列出**跨 DSL 層級**的反模式。

| 編號 | 反模式 | 為何錯 | 正確做法 |
|------|--------|--------|---------|
| **CDS-AP-01** | 在 haAPI/haPDL 內聯權限邏輯（如直接寫 `conditions: [{field: dept_id, op: starts_with, value: ...}]`）| 雙重事實源；haARM constraint 更新時 haAPI/haPDL 不會跟 | 用 `conditions[].haarm_constraint: <id>` opaque ref，由 haARM 持有事實 |
| **CDS-AP-02** | 跨 DSL anchor 不同名（DBML `hycms-ht002.dbml`、haARM `ht002.haarm.yaml`）| `validate_cross_dsl.py` 無法配對；新人找不到對應 | 四 DSL 一律用同 anchor，`benchmarks/<DSL>/<anchor>.<ext>` |
| **CDS-AP-03** | 任一 DSL 升版未 sync 到 `CROSS-DSL-GUIDE.md` §0 互鎖表 | 後續開發者讀到不一致版本資訊 | 升版 PR 必須包含本檔 §0 的編輯 |
| **CDS-AP-04** | haPDL 的 `auth.roles[]` 寫 haARM 未定義的 role | runtime 拒登行為依 codegen 實作而異 | 提交前跑 `validate_cross_dsl.py`，Rule 6 會擋 |
| **CDS-AP-05** | DBML 改 Table 名（如 `InfoUser` → `User`）但 haARM `resource.id` 未跟 | Rule 1 case-insensitive 比對失敗，欄位驗證 silently skip | 同 PR 內更新四 DSL；或讓 Rule 1 在缺少 matched_table 時也報 warning |

---

## 5. Lint 與 codegen 契約（v3.3 規格層宣告 → M4 codegen 落地）

> 本節為**規格層對 lint / codegen 工具的契約宣告**。實作屬 codegen owner 範圍（不在 M0~M3 規格落地範圍內）；列在此處作為驗收標準與實作者參考。

### 5.1 haarm-lint v3.3 必須支援

| 指令 / 規則 | 來源章節 | 嚴重度 |
|------------|---------|:----:|
| 接受 `starts_with` / `ends_with` 運算子（不報「未知運算子」）| §3.8.1 | — |
| `--explain-profile <resource-id>` 印出 profile 展開後完整 YAML | §3.10.3 | — |
| `--trace <resource-id> <role-id> <attr>` 反向追蹤推斷鏈 | §3.11.4 | — |
| `--validate-cross-dsl <anchor>` 讀 `cross_dsl_anchor` 驗證四 DSL 同 anchor | M3.2 | — |
| 偵測 AP-01：`contains` 當前綴比對（如 `deptId contains $self.x`） | haARM §9.5 | **error** |
| 偵測 AP-02：profile_overrides 合併後 `conditions == []` 但無明示 `[]` 鍵 | §3.10.3 | **error** |
| 偵測 AP-03：同 namespace ≥2 個 `implicit: true` role | §3.4（Q8）| warning |
| 偵測 AP-04：end-user 角色（無 `super_admin` profile）用 `scope: all` | §9.5 | warning |
| 偵測 AP-05：`enabled: false` actor 被引用（提醒非 runtime 拒登）| §3.3 | hint |
| 偵測 dynamic_grants.enabled=true（v3.3 強制 false）| §3.14 | error |
| 引用完整性：resource 引用的 DBML table、permission 引用的 resource 都存在 | （沿用 v2）| error |

### 5.2 haapi-lint v3.3 必須支援

| 指令 / 規則 | 來源章節 | 嚴重度 |
|------------|---------|:----:|
| 偵測 AP-01：在新規格用 `access.permissions:` | haAPI §8.5 | error |
| 偵測 AP-02：`rate_limit` 寫在 permission（應在 endpoint）| §8.5 | error |
| 偵測 AP-03：雙軌 required_* 但無 mode 註記 | §8.5 | warning |
| 偵測 AP-04：`conditions[]` 內聯邏輯字串（非 `haarm_constraint` ref）| §8.5 | error |
| 偵測 AP-05：resilience 逐 endpoint 重複寫 | §8.5 | warning |
| 引用完整性：required_permissions 與 required_roles 必須在 haARM 已定義 | M3 Rule 3/4 | error |

### 5.3 hapdl-lint v3.3 必須支援

| 指令 / 規則 | 來源章節 | 嚴重度 |
|------------|---------|:----:|
| 偵測 AP-01：新規格用 `security.permissions:` | haPDL §20.5 | error |
| 偵測 AP-02：deptId 過濾寫在 `datasource.query` | §20.5 | warning |
| 偵測 AP-03：`actions.standard` 與 custom 同名 | §20.5 | warning |
| 偵測 AP-04：顯示型別硬編在 columns | §20.5 | hint |
| 偵測 AP-05：`auth.roles:` 引用 haARM 未定義的 role | M3 Rule 6 | error |
| `security.permission_refs.*[].id` 引用 haARM 必須存在 | — | error |

### 5.4 dbml_parser.py v3.3 必須支援

| 行為 | 來源章節 |
|------|---------|
| 解析 `label:` / `ref_code:` / `sensitive:` / `group:` 為一級欄位 | DBML §五（已落地 M0.5）|
| 偵測 AP-01：`note:` 內嵌 label/group 子格式 | DBML §9.5 | warning |
| 偵測 AP-02：`ref_code:` 與 `ref: >` 並存 | §9.5 | warning |
| 偵測 AP-03：顯式 `sensitive: false`（冗餘）| §9.5 | hint |

### 5.5 codegen 端必須支援（whyAPI / haPDL2PDL / Pdl2whyVue）

| 行為 | 來源 |
|------|------|
| `starts_with` 編譯為 Spring Data `LIKE 'prefix%'` / TypeORM `Like('prefix%')` | M1.1 |
| `ends_with` 編譯為 `LIKE '%suffix'` | M1.1 |
| Profile 展開前置步驟（runtime 視 profile + auto_infer 等價展開為完整 permission 集合） | M2.1 / M2.2 |
| `profile_overrides` 合併語意：scalar deep merge + conditions 完全覆寫（沿用 haPDL Convention） | M2.4 / Q6 |
| `Actor.enabled: false` 在 auth middleware 拒登 | M1.2 / Q7 |
| `dynamic_grants` v3.3 預設 disabled，v3.4 才開放 | §3.14 / Q13 |

### 5.6 VSCode 擴展 v3.3 必須支援

| 功能 | 觸發 |
|------|------|
| `starts_with` / `ends_with` 自動完成 | 在 condition.operator 補 enum |
| Profile id 跳轉 | 點 `profile: dept_isolated_crud` 跳至 §3.10.1 內建定義 |
| Cross-DSL anchor 跳轉 | 點 `cross_dsl_anchor: hycms-ht002` 列出四檔路徑 |
| haARM `permission.id` / `role.id` 跳轉 | 從 haAPI/haPDL 引用點跳回 haARM 定義 |
| DBML `label:` / `ref_code:` 自動完成 | 屬性鍵列表補上 v3.3 新項 |

### 5.7 驗收檢查清單（codegen owner 完工標準）

```bash
# 1. lint 在現有 benchmarks 不報錯（無假警報）
haarm-lint benchmarks/haARM/*.haarm.yaml
hapdl-lint benchmarks/haPDL-v3.2/*.hapdl.yaml
haapi-lint benchmarks/haAPI/*.haapi.yaml

# 2. lint 對 §9.5 反模式範例正確報錯（無漏網）
haarm-lint --self-test  # 內建反模式測試案例

# 3. 跨 DSL 驗證
python benchmarks/validate_cross_dsl.py hycms-ht002

# 4. codegen 對 v3.3 範例產出可編譯程式
cd whyAPI && npm test
cd haPDL2PDL && npm test
cd Pdl2whyVue && npm test
```

---

## 6. 進一步閱讀

- 各 DSL 細節：[haAPIdoc](haAPIdoc.md)、[haPDLdoc](haPDLdoc.md)、[haARMdoc](haARMdoc.md)、[annotated_DBML-v3.3](annotated_DBML-v3.3.md)
- 速查卡（1 頁版）：[haAPI](haAPI-QUICK-REFERENCE.md)、[haPDL](haPDL-QUICK-REFERENCE.md)、[haARM](haARM-QUICK-REFERENCE.md)、[DBML](DBML-QUICK-REFERENCE.md)
- v3.3 對齊計畫：`ccwLog/0513-specsAlign_plan.md`
- v3.3 決策紀錄：`ccwLog/0513-PQ_discuss.md`
- Convention over Configuration 設計動機：`ccwLog/0512-hyCmcAcs_discuss_Opus.md`
- hyCMS 遷移目標：`ccwLog/0512-hyCMS_ACS.md`
