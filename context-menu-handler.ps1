# Git-SVN Merge Context Menu Handler
# This script is called by the Windows context menu
# It validates that the folder is a git-svn repository before running the merge script

param(
    [Parameter(Mandatory=$true)]
    [string]$RepositoryPath
)

# Change to the repository directory
try {
    Set-Location -Path $RepositoryPath -ErrorAction Stop
} catch {
    Write-Host "Error: Cannot access directory: $RepositoryPath" -ForegroundColor Red
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Git-SVN Merge - Context Menu Handler" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "Repository path: $RepositoryPath" -ForegroundColor Yellow
Write-Host ""

# Check if Git is installed
$gitInstalled = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitInstalled) {
    Write-Host "Error: Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git from https://git-scm.com/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "Checking repository..." -ForegroundColor Cyan

# Check if it's a Git repository
$isGitRepo = Test-Path ".git"
if (-not $isGitRepo) {
    Write-Host "Error: This is not a Git repository!" -ForegroundColor Red
    Write-Host "The .git folder was not found in: $RepositoryPath" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "[OK] Git repository found" -ForegroundColor Green

# Check if it's a git-svn repository
try {
    $gitSvnInfo = git config --get-regexp svn-remote 2>$null
    if (-not $gitSvnInfo) {
        Write-Host "Warning: This appears to be a regular Git repository, not git-svn" -ForegroundColor Yellow
        Write-Host "The script is designed for git-svn repositories." -ForegroundColor Yellow
        Write-Host ""
        $continue = Read-Host "Do you want to continue anyway? (y/n)"
        if ($continue -ne "y" -and $continue -ne "Y") {
            Write-Host "Operation cancelled." -ForegroundColor Yellow
            Write-Host "Press any key to exit..."
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 0
        }
    } else {
        Write-Host "[OK] git-svn repository detected" -ForegroundColor Green
    }
} catch {
    Write-Host "Warning: Could not verify git-svn configuration" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host "Starting merge script..." -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
$pythonInstalled = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonInstalled) {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://www.python.org/" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

# Find the merge script
$scriptLocations = @(
    "C:\Tools\git-svn-merge\merge_to_svn.py",
    "$env:USERPROFILE\Tools\git-svn-merge\merge_to_svn.py",
    "C:\Program Files\git-svn-merge\merge_to_svn.py"
)

$scriptPath = $null
foreach ($location in $scriptLocations) {
    if (Test-Path $location) {
        $scriptPath = $location
        break
    }
}

if (-not $scriptPath) {
    Write-Host "Error: merge_to_svn.py script not found!" -ForegroundColor Red
    Write-Host "Searched locations:" -ForegroundColor Yellow
    foreach ($location in $scriptLocations) {
        Write-Host "  - $location" -ForegroundColor Gray
    }
    Write-Host ""
    Write-Host "Please ensure the script is installed in one of these locations." -ForegroundColor Yellow
    Write-Host "See INSTALL.md for installation instructions." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "Using script: $scriptPath" -ForegroundColor Green
Write-Host ""

# Run the merge script
try {
    python $scriptPath $RepositoryPath
    $exitCode = $LASTEXITCODE
    
    Write-Host ""
    if ($exitCode -eq 0) {
        Write-Host "Script completed successfully!" -ForegroundColor Green
    } else {
        Write-Host "Script exited with code: $exitCode" -ForegroundColor Yellow
    }
} catch {
    Write-Host "Error running merge script: $_" -ForegroundColor Red
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
