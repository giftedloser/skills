param([switch]$Check)

$ErrorActionPreference = "Stop"
$repoRoot = Split-Path -Parent $PSScriptRoot
$distDir = Join-Path $repoRoot "dist"

$archives = @(
    @{
        Name = "GiftedLoser-Project-Start.zip"
        Sources = @((Join-Path $repoRoot "packs/project-start/skills"))
    },
    @{
        Name = "GiftedLoser-Project-Checks.zip"
        Sources = @((Join-Path $repoRoot "packs/project-checks/skills"))
    },
    @{
        Name = "GiftedLoser-Skills-Complete.zip"
        Sources = @(
            (Join-Path $repoRoot "packs/project-start/skills"),
            (Join-Path $repoRoot "packs/project-checks/skills")
        )
    }
)

function New-SkillsArchive {
    param([string[]]$Sources, [string]$Destination)

    Add-Type -AssemblyName System.IO.Compression
    $stream = [System.IO.File]::Open($Destination, [System.IO.FileMode]::Create)
    try {
        $zip = [System.IO.Compression.ZipArchive]::new(
            $stream,
            [System.IO.Compression.ZipArchiveMode]::Create,
            $false
        )
        try {
            $files = foreach ($source in $Sources) {
                Get-ChildItem -LiteralPath $source -File -Recurse -Force | ForEach-Object {
                    [pscustomobject]@{
                        File = $_
                        Entry = $_.FullName.Substring($source.Length).TrimStart("\", "/").Replace("\", "/")
                    }
                }
            }

            foreach ($item in ($files | Sort-Object Entry)) {
                $entry = $zip.CreateEntry($item.Entry, [System.IO.Compression.CompressionLevel]::Optimal)
                $input = $item.File.OpenRead()
                $output = $entry.Open()
                try { $input.CopyTo($output) }
                finally { $output.Dispose(); $input.Dispose() }
            }
        }
        finally { $zip.Dispose() }
    }
    finally { $stream.Dispose() }
}

function Get-ArchiveManifest {
    param([string]$Path)

    $stream = [System.IO.File]::OpenRead($Path)
    try {
        $zip = [System.IO.Compression.ZipArchive]::new(
            $stream,
            [System.IO.Compression.ZipArchiveMode]::Read,
            $false
        )
        try {
            foreach ($entry in ($zip.Entries | Sort-Object FullName)) {
                $entryStream = $entry.Open()
                try {
                    $sha256 = [System.Security.Cryptography.SHA256]::Create()
                    try { $hash = $sha256.ComputeHash($entryStream) }
                    finally { $sha256.Dispose() }
                    "{0}|{1}" -f $entry.FullName, [BitConverter]::ToString($hash).Replace("-", "")
                }
                finally { $entryStream.Dispose() }
            }
        }
        finally { $zip.Dispose() }
    }
    finally { $stream.Dispose() }
}

New-Item -ItemType Directory -Force -Path $distDir | Out-Null

foreach ($archive in $archives) {
    $destination = Join-Path $distDir $archive.Name
    $temporary = [System.IO.Path]::GetTempFileName()
    try {
        New-SkillsArchive -Sources $archive.Sources -Destination $temporary

        if ($Check) {
            if (-not (Test-Path -LiteralPath $destination)) {
                throw "Missing distribution archive: $($archive.Name)"
            }

            $difference = Compare-Object `
                (Get-ArchiveManifest -Path $destination) `
                (Get-ArchiveManifest -Path $temporary)
            if ($difference) {
                throw "Stale distribution archive: $($archive.Name)"
            }

            Write-Host "Verified $($archive.Name)"
        }
        else {
            Copy-Item -LiteralPath $temporary -Destination $destination -Force
            Write-Host "Built $($archive.Name)"
        }
    }
    finally {
        Remove-Item -LiteralPath $temporary -Force -ErrorAction SilentlyContinue
    }
}
