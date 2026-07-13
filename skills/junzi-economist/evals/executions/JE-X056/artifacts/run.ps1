$ErrorActionPreference = 'Stop'
$Python = 'C:\Users\ENAN\miniforge3\envs\codex\python.exe'
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location -LiteralPath $Here
try {
    & $Python 'simulate.py'; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & $Python 'estimate_profile.py'; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & $Python 'independent_verify.py'; if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & $Python 'audit.py'; exit $LASTEXITCODE
} finally { Pop-Location }
