---
name: rapt-human-sync
description: "RAPTor 人工 SSoT 變更同步。偵測使用者直接修改的 SSoT artifact，產生 HSYNC 變更紀錄，透過既有 impact-matrix 工具登錄 manual_change，並建議接續 /rapt-verify。Use when: /rapt-human-sync、人工修改 SSoT 後、verify 前需要補齊人工變更追蹤。"
metadata:
  user-invocable: true
  source: project-level
  skill-type: utility
---

# RAPTor Human Sync — 人工 SSoT 變更同步

先遵守 rapt-core：
- LOAD REF [rapt-core::principles.md]
- LOAD REF [rapt-core::paths-and-arguments.md]
- LOAD REF [rapt-core::ssot-definition.md]
- LOAD REF [rapt-core::impact-matrix-schema.md]
- LOAD REF [rapt-core::traceability-schema.md]
- LOAD REF [rapt-core::finding-taxonomy.md]
- LOAD REF [rapt-core::encoding-policy.md]

## TRIGGER

- 使用者執行 `/rapt-human-sync`。
- 人工直接修改 `docs/ssot/**` 後，需要接回 RAPTor 流程。
- `/rapt-verify` 前發現 SSoT 變更尚未登錄為 `manual_change`。

## SKIP

- `.raptor/arguments.yml` 不存在：EMIT 錯誤並建議先執行 `/rapt-kickoff`。
- 無法解析 baseline：EMIT 錯誤並要求使用者用 `--baseline <commit>` 明確指定。
- SSoT path 沒有任何變更：不建立空 HSYNC，不新增 impact entries，只回報可直接執行 `/rapt-verify`。

## PRINCIPLE: CWD 為產出錨點
## PRINCIPLE: Artifact Output Contract
## PRINCIPLE: STRICT SOP

---

## Artifact Output Contract

| 操作 | 路徑 | 說明 |
|------|------|------|
| READ | `.raptor/arguments.yml` | 解析 SSoT 路徑與追蹤檔位置 |
| READ | `.raptor/session.md` | 解析最近 skill 收手點的 git commit |
| READ | `docs/ssot/**` | 掃描人工修改，不直接修改 |
| CREATE | `.raptor/human-sync/HSYNC-*.yml` | 人工變更 session record |
| CREATE / UPDATE | `.raptor/impact-matrix.yml` | 只透過 `rapt-core/scripts/manage_impact_matrix.py upsert` 寫入 `manual_change` |
| CREATE / UPDATE | `.raptor/traceability.md` | 追加 Decision Traceability 摘要 |
| CREATE / UPDATE | `.raptor/session.md` | 追加 human-sync 執行摘要 |
| **DENY** | 任何 SSoT artifact | human-sync 只登錄，不修復 |
| **DENY** | `docs/generate/**` | 不觸碰 generated artifacts |
| **DENY** | `docs/discovery/**` | V1 不把 discovery 當人工 SSoT 掃描範圍 |

---

## V1 行為合約

### Baseline Resolution

依序嘗試：

1. 使用者明確指定 `--baseline <commit>`。
2. 最近一筆觸及 `.raptor/session.md` 的 commit。
3. 最近一筆 commit message 符合 `^raptor:` 的 commit。
4. 最近一個符合 `raptor/*-done` 的 tag。
5. 全部失敗則停止，不用時間推估。

### Scan Mode

| mode | 說明 |
|------|------|
| `auto` | 預設；若 working tree 有 SSoT dirty/untracked 變更，使用 `mixed` 或 `working_tree`，否則使用 `committed` |
| `committed` | 掃 `git diff <baseline> HEAD -- <ssot-paths>`，who/when 由 git log 取得 |
| `working_tree` | 掃 `git diff <baseline> -- <ssot-paths>` 與 untracked SSoT，who/when 記為 operator/scanned_at |
| `mixed` | baseline 後已有 commit，且 working tree 也有未 commit 變更 |

### Idempotency

- 每個 change 以 `baseline + mode + file + change_type + normalized diff` 產生 `fingerprint`。
- 每個 impact entry 以同一份 fingerprint 產生決定性 `IMPACT-<hash>` id。
- 若既有 `.raptor/human-sync/*.yml` 已包含相同 fingerprint，重跑時不新增重複 HSYNC change。
- `impact-matrix.yml` 一律經 `manage_impact_matrix.py upsert`，以既有 id 更新而非 append duplicate。

### Schema Boundary

- `impact-matrix.yml` 僅使用既有 schema 欄位與 enum：
  - `source_type: manual_change`
  - `impact_type: verify`
  - `status: open`
- `risk`、`semantic_summary`、`stale_generated`、`fingerprint` 等豐富資訊只寫入 HSYNC，不寫入 impact-matrix 主檔。

---

## SOP

### 步驟 0：ASK session-level why

若使用者尚未提供：

```text
這批人工 SSoT 修改的共同原因是什麼？
是否有需求文件、issue、decision 或 CiC 可引用？
```

若使用者略過，`decision_ref` 使用 `HSYNC-<id>#Cxxx` 作為必填佔位值。

### 步驟 1：EXECUTE scan

```powershell
python RAPTor/.agents/skills/rapt-human-sync/scripts/human_sync_scan.py `
  --root . `
  --mode auto `
  --human-note "<人工補充原因>" `
  --decision-ref "<需求或決策引用>"
```

可選：

```powershell
python RAPTor/.agents/skills/rapt-human-sync/scripts/human_sync_scan.py --root . --baseline <commit>
```

### 步驟 2：確認輸出

腳本會：

1. 解析 `.raptor/arguments.yml` 的 SSoT path allowlist。
2. 排除 `.raptor/**`、`docs/generate/**`、`docs/discovery/**`。
3. 產生 `.raptor/human-sync/HSYNC-*.yml`。
4. 呼叫 `rapt-core/scripts/manage_impact_matrix.py upsert` 建立 `manual_change` entries。
5. 呼叫 `manage_impact_matrix.py validate`。
6. 追加 `.raptor/traceability.md` 的 `Decision Traceability` row。
7. 追加 `.raptor/session.md` 的 human-sync 摘要。

### 步驟 3：EMIT 接續建議

```text
rapt-human-sync 完成。

已登錄人工 SSoT 變更：{N} 筆
HSYNC：.raptor/human-sync/HSYNC-YYYYMMDD-NNN.yml
Impact entries：{M} 筆，status=open，owner_skill=rapt-verify

建議下一步：執行 /rapt-verify。
```

---

## 輔助偵測

未來若要在 verify 前做輕量檢查，可執行：

```powershell
python RAPTor/.agents/skills/rapt-human-sync/scripts/detect_unsynced.py --root .
```

此腳本只讀取 git diff 與既有 HSYNC fingerprints；不寫任何檔案。

