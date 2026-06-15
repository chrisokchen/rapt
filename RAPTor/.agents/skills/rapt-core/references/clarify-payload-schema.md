# RAPTor Clarify Payload Schema

本文件定義各 skill 發現不確定性時，交給 `rapt-clarify` 或 `rapt-clarify-loop` 的標準 payload。

## Payload Shape

```yaml
clarify_payload:
  batch_id: CLR-BATCH-YYYYMMDD-001
  source_skill: rapt-verify
  source_report: .raptor/reports/verify-20260611.yml
  questions:
    - id: Q-001
      route: NEED_TO_CLARIFY
      severity: high
      topic: 權限模型
      artifact: docs/ssot/haarm/admin.haarm.yaml
      location: roles.Admin.permissions
      question: Admin 是否可覆核自己建立的案件？
      why: haARM 與 behavior scenario 對職責分離的描述不一致。
      options:
        - id: A
          label: 可以覆核
          impact:
            - docs/ssot/haarm/admin.haarm.yaml
            - docs/ssot/haapi/case.haapi.yaml
        - id: B
          label: 不可覆核
          impact:
            - docs/ssot/haarm/admin.haarm.yaml
      default_when_no_answer: B
      blocking_artifacts:
        - docs/ssot/haapi/case.haapi.yaml
```

## Rules

- 每個問題必須能對應到至少一個 artifact 或 finding。
- `why` 必須描述不問會造成什麼具體風險。
- `options.*.impact` 應同步寫入 `.raptor/impact-matrix.yml`。
- `default_when_no_answer` 只能用在低風險或已有 policy fallback 的問題；高風險問題不得假設答案。
