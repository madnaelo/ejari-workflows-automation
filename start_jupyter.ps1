param(
    [int]$Port = 8888
)

$ErrorActionPreference = "Stop"

$venvPath = Join-Path $PSScriptRoot ".venv"
$venvPython = Join-Path $venvPath "Scripts\python.exe"

if (-not (Test-Path $venvPython)) {
    python -m venv $venvPath
    & $venvPython -m pip install --upgrade pip
    & $venvPython -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")
}

& $venvPython -m jupyter lab --notebook-dir $PSScriptRoot --port $Port
