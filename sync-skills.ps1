# sync-skills.ps1 — 放在 RAworkbox/ 根目錄
# 用法: .\sync-skills.ps1
$canonical = "$PSScriptRoot\RAPTor\.agents\skills"
# 定義各專案的 skills 目錄名稱（.agents 或 .claude）
$projects = @{
    "Projects\smallBiz-codex"    = ".agents\skills"
    "Projects\smallBiz-Fable"    = ".claude\skills"
    "Projects\smallBiz"          = ".agents\skills"
    # 新增專案在這裡加一行
}
foreach ($proj in $projects.Keys) {
    $targetDir = "$PSScriptRoot\$proj\$($projects[$proj])"
    $parentDir = Split-Path $targetDir -Parent
    # 確保父目錄存在
    if (-not (Test-Path $parentDir)) {
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
    }
    # 如果已經是 Junction，跳過
    $item = Get-Item $targetDir -ErrorAction SilentlyContinue
    if ($item -and $item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
        Write-Host "[SKIP] $proj — already a junction" -ForegroundColor DarkGray
        continue
    }
    # 如果是真實目錄（舊拷貝），備份後替換
    if (Test-Path $targetDir) {
        $backup = "${targetDir}_backup_$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        Write-Host "[BACKUP] $proj — moving old copy to $backup" -ForegroundColor Yellow
        Rename-Item $targetDir $backup
    }
    # 建立 Junction
    cmd /c mklink /J "$targetDir" "$canonical" 2>&1 | Out-Null
    $ok = Test-Path "$targetDir\rapt-core\SKILL.md"
    if ($ok) {
        Write-Host "[OK] $proj -> canonical" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $proj — junction created but cannot resolve" -ForegroundColor Red
    }
}
Write-Host "`nDone. Canonical source: $canonical"