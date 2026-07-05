# DSLspec Anchor 指向列表

本文件是所有 DSL 格式規範的 **anchor（指向）索引**。

**原則**：各 worker skill 的 anchor 檔案**只指向**這裡；不複製 DSLspec 的格式內容。  
**版本鎖定**：所有 DSL 版本 = **v3.3.0**。若 DSLspec 目錄有更新版本，以 DSLspec 目錄的最新版為準。

---

## DSLspec 根目錄

```
DSLspec/
```

---

## 各 DSL 速查卡（Quick Reference）

| DSL | 速查卡路徑 | 用途 |
|-----|----------|------|
| Annotated DBML v3.3 | `DSLspec/DBML-QUICK-REFERENCE.md` | 一級標註、反模式、範例 |
| haARM v3.3 | `DSLspec/haARM-QUICK-REFERENCE.md` | 角色/權限/資源、v3.3 新運算子、五個 Profile |
| haAPI v3.3 | `DSLspec/haAPI-QUICK-REFERENCE.md` | Access v2 雙軌、Resilience、列表能力 |
| haPDL v3.3 | `DSLspec/haPDL-QUICK-REFERENCE.md` | 欄位符號、v3.3 雙軌權限、Convention 三層 |

---

## 各 DSL 完整文件

| DSL | 完整文件路徑 |
|-----|----------|
| Annotated DBML v3.3 | `DSLspec/annotated_DBML-v3.3.md` |
| haARM v3.3 | `DSLspec/haARMdoc.md` |
| haAPI v3.3 | `DSLspec/haAPIdoc.md` |
| haPDL v3.3 | `DSLspec/haPDLdoc.md` |

---

## 跨 DSL 整合指南

| 文件 | 路徑 |
|------|------|
| 跨 DSL 整合（所有 DSL）| `DSLspec/CROSS-DSL-GUIDE.md` |

---

## 版本優先序規則

```
DSLspec 目錄的實際文件內容  >  任何 skill 的 anchor 範例  >  任何 SOP 中的內嵌範例
```

若 anchor 範例與 DSLspec 文件有衝突，以 **DSLspec 文件為準**，anchor 為舊；請 EMIT 提醒更新。

---

## 各 Worker 的 Anchor 位置

| Worker Skill | Anchor 檔案 |
|------------|-----------|
| `rapt-form-dbml` | `skills/rapt-form-dbml/references/dbml-format-anchor.md` |
| `rapt-form-haarm` | `skills/rapt-form-haarm/references/haarm-format-anchor.md` |
| `rapt-form-gherkin` | `skills/rapt-form-gherkin/references/gherkin-format-anchor.md` |
| `rapt-form-haapi` | `skills/rapt-form-haapi/references/haapi-format-anchor.md` |
| `rapt-form-hapdl` | `skills/rapt-form-hapdl/references/hapdl-format-anchor.md` |

各 anchor 檔案均聲明：「**DSLspec v3.3 takes precedence over this anchor's examples**。」
