param(
    [int]$Port = 8888,
    [string]$VenvRoot = "E:\codex_work\venvs"
)

$ErrorActionPreference = "Stop"

$envName = "DLD-Ejari-CheckUserDataAutomation"
$venvPath = Join-Path $VenvRoot $envName
$venvPython = Join-Path $venvPath "Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    New-Item -ItemType Directory -Force -Path $VenvRoot | Out-Null
    python -m venv $venvPath
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")
}

& $venvPython -m jupyter lab --notebook-dir $PSScriptRoot --port $Port
