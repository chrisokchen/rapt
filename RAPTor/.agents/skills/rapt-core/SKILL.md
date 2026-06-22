---
name: rapt-core
description: "RAPTor skill family 的共用 Reference Hub。Use when: 任何 rapt-* skill 需要載入共同原則、路徑與 arguments.yml 規則、SSoT 定義、Planner/Worker 合約、finding taxonomy、impact matrix、clarify payload、DSL cross-reference、phase gates 或 prompt migration map。"
metadata:
  user-invocable: false
  source: project-level
  skill-type: utility
---

# RAPTor Core 共用參考

## TRIGGER

- 任一 rapt-* skill 執行前需要載入共用 reference 規範時。
- 需要查閱跨 skill 共用的 utility 定義或 schema 時。

## SKIP

- 不直接接手任何會寫入 SSoT artifact 的階段工作。
- 應改用對應的 planner、worker、verifier 或 preview skill。

此 skill 是 RAPTor skill family 的共用知識中心，不是直接執行的 SOP。

所有 `rapt-*` skill 應依任務需要 LOAD REF，不可整包讀取所有 reference。若規則衝突，以更嚴格的 write boundary、Artifact Output Contract 與 SSoT policy 為準。

## PRINCIPLE

- rapt-core 是共用 reference hub，不直接執行 phase SOP。
- 其他 skill 只載入任務需要的 reference，不整包載入全部文件。
- rapt-core 的 scripts/templates 可被其他 skill 引用，但不得繞過各 skill 的 Artifact Output Contract。

## Artifact Output Contract

| Action | Path | Purpose |
|---|---|---|
| READ | `RAPTor/.agents/skills/rapt-core/references/**` | 共用原則與契約 |
| READ | `RAPTor/.agents/skills/rapt-core/templates/**` | 共用模板 |
| EXECUTE | `RAPTor/.agents/skills/rapt-core/scripts/**` | 共用輔助工具 |
| DENY | `docs/ssot/**` | core 不修改業務 SSoT |
| DENY | `docs/generate/**` | core 不直接產生 preview/generated artifact |

## References

| 文件 | 用途 |
|---|---|
| [principles.md](references/principles.md) | 核心執行原則：CWD、Artifact Output Contract、Strict SOP、TODO、deny-by-default |
| [verb-cheatsheet.md](references/verb-cheatsheet.md) | READ/DERIVE/ASSERT/EMIT/CREATE/UPDATE/DENY/ASK/DELEGATE 動詞規範 |
| [paths-and-arguments.md](references/paths-and-arguments.md) | `.raptor/arguments.yml` 解析規則與路徑慣例 |
| [ssot-definition.md](references/ssot-definition.md) | SSoT 與 downstream generated artifacts 邊界 |
| [planner-worker-contract.md](references/planner-worker-contract.md) | Planner -> Worker payload、Worker 禁止項與 failure contract |
| [finding-taxonomy.md](references/finding-taxonomy.md) | verify/reconcile/RAscore 共用 finding 分類、route 與 can_fix 規則 |
| [impact-matrix-schema.md](references/impact-matrix-schema.md) | `.raptor/impact-matrix.yml` schema 與更新規則 |
| [clarify-payload-schema.md](references/clarify-payload-schema.md) | 各 skill 交給 clarify loop 的問題 payload 標準 |
| [skill-writing-principle.md](references/skill-writing-principle.md) | TRIGGER/SKIP、Artifact Output Contract、長流程與 failure contract 撰寫原則 |
| [preview-audit-schema.md](references/preview-audit-schema.md) | preview generated artifact 的 audit output schema |
| [dsl-cross-reference-v33.md](references/dsl-cross-reference-v33.md) | 跨 DSL 對照規則與 v3.3 naming 對齊 |
| [dslspec-anchors.md](references/dslspec-anchors.md) | 各 DSL 規格 anchor 位置 |
| [cic-note-policy.md](references/cic-note-policy.md) | CiC note 的 GAP/ASM/BDY/CON 記錄政策 |
| [phase-gates.md](references/phase-gates.md) | 各 phase 完成條件與交付檢查 |
| [prompt-migration-map.md](references/prompt-migration-map.md) | `0_prompts/` 到 skill sub-SOP 的對照表 |

## Scripts

| Script | 用途 |
|---|---|
| [resolve_args.py](scripts/resolve_args.py) | stdlib-only 解析 `.raptor/arguments.yml`，輸出 `KEY=value` |
| [manage_impact_matrix.py](scripts/manage_impact_matrix.py) | 管理 `.raptor/impact-matrix.yml` 的 validate/query/upsert |
| [migrate_docs_layout.py](scripts/migrate_docs_layout.py) | dry-run 或 apply v1 docs layout 到 v2 layout 的遷移 |

## Templates

| Template | 用途 |
|---|---|
| [principle-artifact-output-contract.template.md](templates/principle-artifact-output-contract.template.md) | 新增或改寫 skill 的 Artifact Output Contract |
| [principle-long-process-todo.template.md](templates/principle-long-process-todo.template.md) | 長流程執行 checklist |
| [principle-strict-sop.template.md](templates/principle-strict-sop.template.md) | sub-SOP 的 READ/ASSERT/DERIVE/CREATE/EMIT 結構 |

## 禁止事項

- 不在此 skill 寫入專案 artifact。
- 不把所有 reference 無差別載入 worker context。
- 不在各 skill 複製另一份路徑設定；路徑唯一來源仍是 `.raptor/arguments.yml`。
- 不繞過 Artifact Output Contract 修改非授權檔案。
