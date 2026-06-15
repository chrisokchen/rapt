# rapt-human-sync HSYNC Schema

`.raptor/human-sync/HSYNC-*.yml` 是人工修改 SSoT 的結構化登錄檔。它承載比 `impact-matrix.yml` 更細的資料，例如 hunk 摘要、risk、operator、working-tree provenance 與 generated stale 提示。

## Schema Version

```yaml
schema_version: rapt-human-sync/v1
```

## Root

```yaml
schema_version: rapt-human-sync/v1
sync:
  id: HSYNC-20260613-001
  scanned_at: "2026-06-13T15:30:00+08:00"
  mode: committed | working_tree | mixed
  baseline:
    commit: <git commit hash>
    source: explicit | session_md | raptor_commit | tag
    label: <human readable label>
  head:
    commit: <git commit hash>
    dirty: true | false
  operator:
    name: <person who ran human-sync>
    email: <optional>
    source: argument | environment
  human_note: <session-level why>
  decision_ref: <optional external requirement or decision id>
changes:
  - id: C001
    impact_id: IMPACT-<deterministic-hash>
    fingerprint: <sha256>
    file: docs/ssot/dbml/schema.dbml
    old_file: ""
    ssot_class: first_class | supporting
    dsl: dbml | habdd | haarm | haapi | hapdl | glossary | seeds | constraints | unknown
    change_type: added | modified | deleted | renamed
    risk: medium | high
    source: committed | working_tree | untracked
    author: { name: <git author or operator>, email: <optional>, source: git_commit | working_tree | untracked }
    committed_at: <git commit time or scan time>
    commit: <git commit hash or WORKTREE>
    diff_summary:
      added_lines: 3
      removed_lines: 1
    semantic_summary:
      - { kind: table, name: Order, action: changed }
    hunks:
      - location: "table Order"
        hunk_header: "@@ -12,6 +12,8 @@"
        added: 3
        removed: 1
        snippet:
          - "+ totalWeight decimal"
    effective_human_note: <inherited why>
    effective_decision_ref: <decision_ref or HSYNC#change>
    impact_assessment:
      affected_dsls: [haapi, hapdl]
      stale_generated: [openapi, lofi]
      needs_verify: true
```

## Rules

- `fingerprint` 用於 HSYNC 去重。
- `impact_id` 必須符合 `impact-matrix-schema.md` 的 `IMPACT-[0-9A-Za-z_.-]+` 格式。
- `impact-matrix.yml` 不得新增本 schema 的豐富欄位；只能透過 `manage_impact_matrix.py upsert` 寫入合法欄位。
- `working_tree` / `untracked` 來源的 who/when 可信度低於 git commit，必須保留 `source`。

