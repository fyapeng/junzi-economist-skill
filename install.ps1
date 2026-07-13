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
$TransactionId = [Guid]::NewGuid().ToString('N')
$Targets = foreach ($Platform in $Platforms) {
    $SkillsRoot = if ($DestinationRoot) {
        Join-Path $DestinationRoot ".$Platform\skills"
    } else {
        Join-Path $HOME ".$Platform\skills"
    }
    [PSCustomObject]@{
        Platform = $Platform
        SkillsRoot = $SkillsRoot
        Destination = Join-Path $SkillsRoot 'junzi-economist'
        Stage = Join-Path $SkillsRoot ".junzi-economist.install-$TransactionId"
        Backup = Join-Path $SkillsRoot ".junzi-economist.backup-$TransactionId"
        Installed = $false
        HadOriginal = $false
    }
}

# Preflight every destination before changing any of them.
if (-not $Force) {
    $Conflicts = @($Targets | Where-Object { Test-Path -LiteralPath $_.Destination })
    if ($Conflicts.Count) {
        $Paths = ($Conflicts.Destination -join ', ')
        throw "Destination already exists: $Paths. Re-run with -Force after reviewing it."
    }
}

try {
    # Stage and verify every copy before replacing an installed skill.
    foreach ($Item in $Targets) {
        New-Item -ItemType Directory -Force -Path $Item.SkillsRoot | Out-Null
        Copy-Item -LiteralPath $Source -Destination $Item.Stage -Recurse
        foreach ($Required in @('SKILL.md', 'LICENSE.txt', 'scripts\validate.py')) {
            if (-not (Test-Path -LiteralPath (Join-Path $Item.Stage $Required))) {
                throw "Staged package is incomplete for $($Item.Platform): $Required"
            }
        }
    }

    foreach ($Item in $Targets) {
        if (Test-Path -LiteralPath $Item.Destination) {
            Move-Item -LiteralPath $Item.Destination -Destination $Item.Backup
            $Item.HadOriginal = $true
        }
        Move-Item -LiteralPath $Item.Stage -Destination $Item.Destination
        $Item.Installed = $true
    }
} catch {
    # Roll back every target to its pre-install state.
    foreach ($Item in @($Targets)[-1..-$Targets.Count]) {
        if ($Item.Installed -and (Test-Path -LiteralPath $Item.Destination)) {
            Remove-Item -LiteralPath $Item.Destination -Recurse -Force
        }
        if ($Item.HadOriginal -and (Test-Path -LiteralPath $Item.Backup)) {
            Move-Item -LiteralPath $Item.Backup -Destination $Item.Destination
        }
        if (Test-Path -LiteralPath $Item.Stage) {
            Remove-Item -LiteralPath $Item.Stage -Recurse -Force
        }
    }
    throw
}

foreach ($Item in $Targets) {
    if (Test-Path -LiteralPath $Item.Backup) {
        Remove-Item -LiteralPath $Item.Backup -Recurse -Force
    }
    Write-Host "Installed Junzi Economist for $($Item.Platform) at $($Item.Destination)"
}
