[CmdletBinding()]
param(
    [switch]$Force,
    [string]$DestinationRoot = ''
)

$ErrorActionPreference = 'Stop'
$Source = Join-Path $PSScriptRoot 'skills\junzi-economist'
if (-not (Test-Path -LiteralPath (Join-Path $Source 'SKILL.md'))) {
    throw "Runtime package not found: $Source"
}

$SkillsRoot = if ($DestinationRoot) {
    Join-Path $DestinationRoot '.codex\skills'
} else {
    Join-Path $HOME '.codex\skills'
}
$JunziCandidates = if ($DestinationRoot) {
    @(
        (Join-Path $DestinationRoot '.codex\skills\junzi\SKILL.md'),
        (Join-Path $DestinationRoot '.agents\skills\junzi\SKILL.md')
    )
} else {
    @(
        (Join-Path $HOME '.codex\skills\junzi\SKILL.md'),
        (Join-Path $HOME '.agents\skills\junzi\SKILL.md')
    )
}
if (-not ($JunziCandidates | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1)) {
    Write-Warning 'Upstream Junzi was not found. For the full configuration, install it first: npx -y skills add fyapeng/junzi-skill --skill junzi -g -a codex --copy -y'
}
$Destination = Join-Path $SkillsRoot 'junzi-economist'
$TransactionId = [Guid]::NewGuid().ToString('N')
$Stage = Join-Path $SkillsRoot ".junzi-economist.install-$TransactionId"
$Backup = Join-Path $SkillsRoot ".junzi-economist.backup-$TransactionId"
$Installed = $false
$HadOriginal = $false

if ((Test-Path -LiteralPath $Destination) -and -not $Force) {
    throw "Destination already exists: $Destination. Re-run with -Force after reviewing it."
}

try {
    New-Item -ItemType Directory -Force -Path $SkillsRoot | Out-Null
    Copy-Item -LiteralPath $Source -Destination $Stage -Recurse
    foreach ($Required in @('SKILL.md', 'LICENSE.txt', 'scripts\validate.py')) {
        if (-not (Test-Path -LiteralPath (Join-Path $Stage $Required))) {
            throw "Staged package is incomplete: $Required"
        }
    }
    if (Test-Path -LiteralPath $Destination) {
        Move-Item -LiteralPath $Destination -Destination $Backup
        $HadOriginal = $true
    }
    Move-Item -LiteralPath $Stage -Destination $Destination
    $Installed = $true
} catch {
    if ($Installed -and (Test-Path -LiteralPath $Destination)) {
        Remove-Item -LiteralPath $Destination -Recurse -Force
    }
    if ($HadOriginal -and (Test-Path -LiteralPath $Backup)) {
        Move-Item -LiteralPath $Backup -Destination $Destination
    }
    if (Test-Path -LiteralPath $Stage) {
        Remove-Item -LiteralPath $Stage -Recurse -Force
    }
    throw
}

if (Test-Path -LiteralPath $Backup) {
    Remove-Item -LiteralPath $Backup -Recurse -Force
}
Write-Host "Installed Junzi Economist for Codex at $Destination"
