<#
.SYNOPSIS
    Reads project files using Get-Content, automatically respecting .gitignore rules via Git, 
    and compiles them into a single Markdown (.md) document.
#>

$SourceDir = Get-Location
$OutputMd = Join-Path $SourceDir "ClinicEase_Combined_Source.md"

# Allowed file extensions to compile
$AllowedExtensions = @(".py", ".html", ".css", ".js", ".sql", ".txt", ".md")

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host " Compiling Source Files (Respecting .gitignore)" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Source Directory: $SourceDir"
Write-Host "Output Markdown:  $OutputMd`n"

# Verify if git is initialized in the folder
if (-not (Test-Path (Join-Path $SourceDir ".git"))) {
    Write-Host "[ERROR] A .git repository was not found in this folder. Please run 'git init' first." -ForegroundColor Red
    exit
}

# Use Git to get all tracked and untracked files while automatically excluding .gitignore patterns
$GitFiles = git ls-files --cached --others --exclude-standard

if (-not $GitFiles) {
    Write-Host "[ERROR] No files found or repository is empty." -ForegroundColor Red
    exit
}

# Initialize the output Markdown file
Set-Content -Path $OutputMd -Value "# ClinicEase Project Source Code Compilation`n`n**Generated on:** $(Get-Date)`n`n---`n" -Encoding utf8

# Process each file returned by Git
foreach ($relativePath in $GitFiles) {
    $fullPath = Join-Path $SourceDir $relativePath
    
    if (Test-Path -Path $fullPath -PathType Leaf) {
        $file = Get-Item $fullPath
        $ext = $file.Extension.ToLower()

        # Filter by allowed extensions and make sure it doesn't compile the output file itself
        if ($AllowedExtensions -contains $ext -and $file.FullName -ne $OutputMd) {
            Write-Host "[COMPILING] $relativePath" -ForegroundColor Green

            # Map extensions to Markdown syntax highlighting identifiers
            $lang = switch ($ext) {
                ".py"   { "python" }
                ".html" { "html" }
                ".css"  { "css" }
                ".js"   { "javascript" }
                ".sql"  { "sql" }
                ".md"   { "markdown" }
                default { "text" }
            }

            # Read file content safely using Get-Content
            $content = Get-Content -Path $fullPath -Raw

            # Append section header and fenced code block to the single Markdown file
            Add-Content -Path $OutputMd -Value "## File: `$relativePath`n`n````$lang`n$content`n`````n`n---`n" -Encoding utf8
        }
    }
}

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host " Compilation Complete! Combined file:    " -ForegroundColor Cyan
Write-Host " $OutputMd                               " -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan