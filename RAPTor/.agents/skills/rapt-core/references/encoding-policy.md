# Encoding Policy

本文件定義 RAPTor skill 寫入文字檔時的編碼規範。

## 強制規則

- Markdown、YAML、DBML、Gherkin feature、`SKILL.md` 一律使用 UTF-8。
- 讀寫中文內容時必須明確使用 UTF-8。
- 不得因 PowerShell 顯示亂碼就直接重轉碼；必須先確認檔案 bytes 與 terminal encoding。
- `SKILL.md` frontmatter 若含中文 description，修改後必須讀回驗證。
- 不得混用 ANSI / Big5 / 系統預設編碼寫入 RAPTor skill 文件。

## 建議驗證

修改含中文文件後，至少讀回開頭與結尾：

```powershell
Get-Content -Path <file> -Encoding UTF8 | Select-Object -First 20
Get-Content -Path <file> -Encoding UTF8 | Select-Object -Last 20
```

## 亂碼處理

若終端顯示亂碼：

1. 先用 UTF-8 讀回檔案。
2. 檢查是否只有 shell display issue。
3. 若檔案本身已毀損，才以可信來源重寫。
4. 重寫時保留原有 artifact contract 與 SOP 結構。
