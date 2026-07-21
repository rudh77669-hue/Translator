Param(
    [switch]$Force
)

$RepoUrl = "https://github.com/rudh77669-hue/Translator.git"
$BackendPath = Join-Path $PSScriptRoot "backend"

if (-not (Test-Path $BackendPath)) {
    Write-Error "backend folder not found at $BackendPath"
    exit 1
}

Push-Location -Path $BackendPath
try {
    if (-not (Test-Path ".git")) {
        git init
        git add .
        git commit -m "Add backend"
        git remote add origin $RepoUrl
        git branch -M main
        if ($Force) { git push -u origin main --force } else { git push -u origin main }
    } else {
        git add .
        git commit -m "Update backend" -q
        if ($Force) { git push origin HEAD:main --force } else { git push origin HEAD:main }
    }
}
catch {
    Write-Error "Git operation failed: $_"
    exit 1
}
finally {
    Pop-Location
}
