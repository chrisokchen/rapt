# RAPTor SSoT 定義

RAPTor 將 artifact 分為三層：First-class SSoT、Supporting SSoT、Downstream Generated。只有前兩者能作為需求與設計決策的來源；Downstream Generated 必須可由 SSoT 重新產生，不可反向覆蓋 SSoT。

## First-class SSoT

| # | Artifact | v2 路徑 | 主要內容 | Owner |
|---|---|---|---|---|
| 1 | Annotated DBML | `docs/ssot/dbml/*.dbml` | 資料模型、欄位語意、label/group/sensitive/ref_code | `rapt-modeling` / `rapt-form-dbml` |
| 2 | haBDD | `docs/ssot/habdd/*.ha.feature` | 高階行為規格、business rule、scenario | `rapt-behavior` / `rapt-form-gherkin` |
| 3 | haARM | `docs/ssot/haarm/*.haarm.yaml` | 角色、權限、resource、policy、cross-cutting concerns | `rapt-modeling` / `rapt-form-haarm` |
| 4 | haAPI | `docs/ssot/haapi/*.haapi.yaml` | 後端 API intent、endpoint、DTO、auth policy | `rapt-intent` / `rapt-form-haapi` |
| 5 | haPDL | `docs/ssot/hapdl/*.hapdl.yaml` | 前端 page intent、component、interaction、state | `rapt-intent` / `rapt-form-hapdl` |

## Supporting SSoT

| Artifact | v2 路徑 | 用途 | Owner |
|---|---|---|---|
| discovery | `docs/discovery/*.md` | source intake、journey、event storming、vision/kpi/scope | `rapt-discovery` |
| glossary | `docs/ssot/dbml/glossary.md` | canonical term、legacy alias、domain language | `rapt-modeling` |
| seeds | `docs/ssot/dbml/seeds.md` | enum/ref-code/reference data | `rapt-modeling` / `rapt-clarify` |
| constraints | `docs/ssot/dbml/constraints.md` | 跨欄位、跨 entity、跨 DSL 的 constraint | `rapt-modeling` / `rapt-clarify` |
| traceability | `.raptor/traceability.md` | L1/L2/L3 與 decision traceability | `rapt-behavior` / `rapt-intent` / `rapt-reconcile` |
| impact matrix | `.raptor/impact-matrix.yml` | 決策或修復對下游 artifact 的影響 | `rapt-clarify` / `rapt-reconcile` |

## Downstream Generated

| Artifact | v2 路徑 | 來源 SSoT | 規則 |
|---|---|---|---|
| PDL | `docs/generate/pdl/` | haPDL | 不可手動回寫 haPDL |
| isaBDD / low-level Gherkin | `docs/generate/isabdd/` | haBDD + haAPI + haPDL | 只描述 implementation scenario |
| OpenAPI | `docs/generate/openapi/` | haAPI + DBML + haARM | `rapt-openapi` 只寫 generated |
| Lo-Fi | `docs/generate/lofi/` | haPDL + DBML + haARM | `rapt-lofi` 只寫 generated |
| Design Brief | `docs/generate/designbrief/` | haPDL + DBML + haARM | `rapt-design-brief` 只寫 generated |

## Boundary Rules

- haARM 是 role/permission 的唯一 SSoT；haAPI/haPDL 不可自行發明權限。
- DBML 是 entity/field 的唯一 SSoT；haAPI/haPDL 只能引用 DBML 已定義的 entity/field。
- haBDD 是高階業務行為 SSoT；isaBDD/low-level Gherkin 是 generated，不得當作需求來源。
- Preview output 是 inspection artifact；發現問題時產出 finding，不直接改 SSoT。
