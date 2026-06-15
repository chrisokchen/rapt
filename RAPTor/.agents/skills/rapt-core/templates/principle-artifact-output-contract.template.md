# Artifact Output Contract Template

```markdown
## Artifact Output Contract

| Action | Path | Purpose |
|---|---|---|
| READ | `${paths...}` | 輸入來源 |
| CREATE / UPDATE | `${paths...}` | 本 skill 唯一允許寫入範圍 |
| DENY | `**/*` outside allowlist | 未明確授權者一律不可寫 |

若需要修改 contract 外的 artifact，必須輸出 finding 或 clarify payload，不可直接修改。
```
