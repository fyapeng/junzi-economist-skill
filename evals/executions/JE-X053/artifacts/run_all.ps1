$ErrorActionPreference = 'Stop'
$Python = 'C:\Users\ENAN\miniforge3\envs\codex\python.exe'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
& $Python (Join-Path $Root 'model.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$manifest = @()
foreach ($mode in @('simulation','equilibrium','estimation')) {
    & $Python (Join-Path $Root 'failure_modes.py') $mode
    $code = $LASTEXITCODE
    $manifest += [ordered]@{mode=$mode; exit_code=$code; diagnostic_exists=(Test-Path (Join-Path $Root "failure_$mode.json"))}
    if ($code -eq 0) { throw "Forced $mode failure incorrectly exited zero" }
}
$manifest | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $Root 'process_failure_manifest.json') -Encoding utf8
& $Python (Join-Path $Root 'verifier.py')
exit $LASTEXITCODE
