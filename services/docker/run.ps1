$ErrorActionPreference = "Stop"

$DEBUG = $env:DEBUG
if (-not $DEBUG) {
    $DEBUG = "false"
}
$DEBUG = $DEBUG.ToLowerInvariant()

function Run($cmd, $cmdArgs) {
    if ($DEBUG -eq "true") {
        Write-Host "+ $cmd $($cmdArgs -join ' ')"
    }

    & $cmd @cmdArgs

    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
}

if ($args.Count -ne 1) {
    Write-Host "Error: MODE is required."
    Write-Host "Usage: ./run.ps1 {dev|prod}"
    exit 1
}

$MODE = $args[0].ToLowerInvariant()

if ($MODE -notin @("dev", "prod")) {
    Write-Host "Error: Invalid mode '$MODE'"
    Write-Host "Usage: ./run.ps1 {dev|prod}"
    exit 1
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "Docker not found"
    exit 1
}

$SCRIPT_DIR = $PSScriptRoot
$COMPOSE_FILE = Join-Path `
    $SCRIPT_DIR `
    "docker-compose.$MODE.yml"

if (-not (Test-Path $COMPOSE_FILE -PathType Leaf)) {
    Write-Host "Compose file not found: $COMPOSE_FILE"
    exit 1
}

$COMPOSE_UP_ARGS = @(
    "-d",
    "--build"
)

if ($MODE -eq "prod") {
    $COMPOSE_UP_ARGS += @(
        "--force-recreate",
        "--pull",
        "always"
    )
}

$COMPOSE_ARGS = @(
    "compose",
    "--project-directory",
    $SCRIPT_DIR,
    "-f",
    $COMPOSE_FILE,
    "up"
) + $COMPOSE_UP_ARGS

Run "docker" $COMPOSE_ARGS