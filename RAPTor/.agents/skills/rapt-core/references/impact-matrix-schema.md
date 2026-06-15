# RAPTor Impact Matrix Schema

`.raptor/impact-matrix.yml` 用來記錄「決策、澄清、修復」對下游 artifact 的影響。它不是取代 traceability，而是補足跨 phase 的改動傳播清單。

## File Path

```text
.raptor/impact-matrix.yml
```

## Entry Schema

```yaml
- id: IMPACT-20260611-001
  source_type: clarify_decision | finding | manual_change | reconcile_fix
  source_ref: .clarify/decision-log.md#CLR-20260611-001
  target_artifact: docs/ssot/haapi/user.haapi.yaml
  impact_type: create | update | verify | regenerate | review_only
  decision_id: CLR-20260611-001
  status: open | applied | verified | obsolete
  owner_skill: rapt-intent
  notes: 角色權限改動後需同步 API auth policy。
```

## Rules

- `id` 必須唯一，格式建議為 `IMPACT-YYYYMMDD-NNN`。
- `source_ref` 必須指向可追溯來源，例如 clarify decision、finding report、reconcile session。
- `target_artifact` 一律使用 arguments.yml 解析後的相對路徑。
- `status` 不可直接從 `open` 跳到 `verified`；必須先有 `applied` 或明確標示 `review_only`。
- 任何 clarify decision 被 apply 時，都應至少查詢一次 impact matrix，確認下游是否需要同步。

## Tool

共用工具：`rapt-core/scripts/manage_impact_matrix.py`
