# install_mcp.ps1
# Script to automatically register Takon MCP Core in thClaws settings

$ConfigPath = "$env:USERPROFILE\.config\thclaws\settings.json"
$ProjectPath = "C:\Users\takon\OneDrive\Desktop\da\25_takon-mcp-core"
$UvPath = "C:\Users\takon\.local\bin\uv.exe"

# 1. Define MCP Server configuration
$NewMcpServers = @{
    "takon-construction" = @{
        "command" = $UvPath
        "args" = @("--directory", $ProjectPath, "run", "takon-construction")
        "env" = @{ "AI_STRATEGY" = "local" }
    }
    "takon-cad" = @{
        "command" = $UvPath
        "args" = @("--directory", $ProjectPath, "run", "takon-cad")
    }
}

# 2. Check and Create Config Directory
$ConfigDir = Split-Path $ConfigPath
if (!(Test-Path $ConfigDir)) {
    Write-Host "Creating config directory: $ConfigDir" -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $ConfigDir -Force | Out-Null
}

# 3. Load or Initialize Settings
if (Test-Path $ConfigPath) {
    Write-Host "Loading existing settings from: $ConfigPath" -ForegroundColor Cyan
    $Settings = Get-Content $ConfigPath -Raw | ConvertFrom-Json
} else {
    Write-Host "Creating new settings file." -ForegroundColor Yellow
    $Settings = @{ "mcpServers" = @{} } | ConvertTo-Json | ConvertFrom-Json
}

# Ensure mcpServers property exists
if (-not $Settings.PSObject.Properties['mcpServers']) {
    $Settings | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value @{}
}

# 4. Inject New Servers
Write-Host "Injecting Takon MCP servers..." -ForegroundColor Green
foreach ($key in $NewMcpServers.Keys) {
    $Settings.mcpServers | Add-Member -MemberType NoteProperty -Name $key -Value $NewMcpServers[$key] -Force
}

# 5. Save back to file
Write-Host "Saving updated settings..." -ForegroundColor Green
$SettingsJson = $Settings | ConvertTo-Json -Depth 10
$SettingsJson | Set-Content $ConfigPath -Encoding UTF8

Write-Host "`nSUCCESS! Takon MCP Core has been registered in thClaws." -ForegroundColor Green
Write-Host "Please restart thClaws to apply changes." -ForegroundColor Yellow
pause
