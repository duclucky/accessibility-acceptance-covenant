$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"

& .\.venv\Scripts\genvm-lint.exe check contracts\accessibility_acceptance_covenant.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& .\.venv\Scripts\genvm-lint.exe typecheck contracts\accessibility_acceptance_covenant.py --strict
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& .\.venv\Scripts\python.exe -m pytest tests\direct tests\unit -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& .\.venv\Scripts\python.exe scripts\schema_preflight.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$contractCount = @(Get-ChildItem -LiteralPath contracts -Filter *.py -File).Count
if ($contractCount -ne 1) { throw "Expected exactly one contract, found $contractCount" }
if (Test-Path -LiteralPath frontend) { throw "Intelligent Contracts track forbids frontend/" }
Write-Output "check passed: contract_count=$contractCount"
