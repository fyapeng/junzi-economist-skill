[CmdletBinding()]
param(
    [ValidateSet('codex', 'claude', 'both')]
    [string]$Target = 'codex',
    [switch]$Force,
    [string]$DestinationRoot = ''
)

$ErrorActionPreference = 'Stop'
$Source = Join-Path $PSScriptRoot 'skills\junzi-economist'
if (-not (Test-Path -LiteralPath (Join-Path $Source 'SKILL.md'))) {
    throw "Runtime package not found: $Source"
}

$Platforms = if ($Target -eq 'both') { @('codex', 'claude') } else { @($Target) }
foreach ($Platform in $Platforms) {
    $SkillsRoot = if ($DestinationRoot) {
        Join-Path $DestinationRoot ".$Platform\skills"
    } else {
        Join-Path $HOME ".$Platform\skills"
    }
    $Destination = Join-Path $SkillsRoot 'junzi-economist'
    New-Item -ItemType Directory -Force -Path $SkillsRoot | Out-Null
    if (Test-Path -LiteralPath $Destination) {
        if (-not $Force) {
            throw "Destination already exists: $Destination. Re-run with -Force after reviewing it."
        }
        Remove-Item -LiteralPath $Destination -Recurse -Force
    }
    Copy-Item -LiteralPath $Source -Destination $Destination -Recurse
    Write-Host "Installed Junzi Economist for $Platform at $Destination"
}
