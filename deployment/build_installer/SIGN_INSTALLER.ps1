# SIGN_INSTALLER.ps1
# Signs the MBAS installer EXE with the Z&T Technologies code signing certificate
# Usage: powershell -ExecutionPolicy Bypass -File SIGN_INSTALLER.ps1 [-ExePath "path\to\exe"]

param(
    [string]$ExePath = "",
    [string]$CertPassword = "ZTTech2026!Secure",
    [string]$PfxPath = ""
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Z&T Technologies - Installer Signer       " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$certDir = Join-Path $PSScriptRoot "certificates"

# Find PFX file
if (-not $PfxPath) {
    $PfxPath = Join-Path $certDir "ZT_Technologies_CodeSign.pfx"
}

if (-not (Test-Path $PfxPath)) {
    Write-Host "ERROR: Certificate PFX not found at: $PfxPath" -ForegroundColor Red
    Write-Host "Run CREATE_CERTIFICATE.ps1 first to generate the certificate." -ForegroundColor Yellow
    exit 1
}

# Find EXE to sign
if (-not $ExePath) {
    # Auto-detect the latest installer in output folder
    $outputDir = Join-Path $PSScriptRoot "output"
    if (Test-Path $outputDir) {
        $latestExe = Get-ChildItem -Path $outputDir -Filter "MBAS_Professional_Setup_*.exe" |
                     Sort-Object LastWriteTime -Descending |
                     Select-Object -First 1
        if ($latestExe) {
            $ExePath = $latestExe.FullName
        }
    }
}

if (-not $ExePath -or -not (Test-Path $ExePath)) {
    Write-Host "ERROR: No installer EXE found to sign." -ForegroundColor Red
    Write-Host "Usage: .\SIGN_INSTALLER.ps1 -ExePath 'path\to\installer.exe'" -ForegroundColor Yellow
    exit 1
}

Write-Host "Signing: $ExePath" -ForegroundColor White
Write-Host "Using certificate: $PfxPath" -ForegroundColor Gray
Write-Host ""

# Load the PFX certificate
Write-Host "[1/3] Loading certificate..." -ForegroundColor Yellow
$securePassword = ConvertTo-SecureString -String $CertPassword -Force -AsPlainText
$cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($PfxPath, $securePassword)

if (-not $cert) {
    Write-Host "ERROR: Failed to load certificate from PFX." -ForegroundColor Red
    exit 1
}
Write-Host "  Certificate loaded: $($cert.Subject)" -ForegroundColor Green
Write-Host "  Thumbprint: $($cert.Thumbprint)" -ForegroundColor Gray

# Sign the EXE
Write-Host ""
Write-Host "[2/3] Applying Authenticode signature..." -ForegroundColor Yellow

$result = Set-AuthenticodeSignature `
    -FilePath $ExePath `
    -Certificate $cert `
    -HashAlgorithm SHA256 `
    -TimestampServer "http://timestamp.digicert.com"

if ($result.Status -eq "Valid") {
    Write-Host "  Signature applied successfully! Status: $($result.Status)" -ForegroundColor Green
} elseif ($result.Status -eq "UnknownError" -or $result.Status -ne "Valid") {
    # Try without timestamp server (in case of network issues)
    Write-Host "  Timestamp server unavailable, signing without timestamp..." -ForegroundColor Yellow
    $result = Set-AuthenticodeSignature `
        -FilePath $ExePath `
        -Certificate $cert `
        -HashAlgorithm SHA256

    if ($result.Status -eq "Valid") {
        Write-Host "  Signature applied successfully (no timestamp)! Status: $($result.Status)" -ForegroundColor Green
    } else {
        Write-Host "  WARNING: Signature status: $($result.Status)" -ForegroundColor Yellow
        Write-Host "  Message: $($result.StatusMessage)" -ForegroundColor Gray
    }
}

# Verify the signature
Write-Host ""
Write-Host "[3/3] Verifying signature..." -ForegroundColor Yellow

$sig = Get-AuthenticodeSignature -FilePath $ExePath
Write-Host "  Status: $($sig.Status)" -ForegroundColor $(if ($sig.Status -eq "Valid") { "Green" } else { "Yellow" })
Write-Host "  Signer: $($sig.SignerCertificate.Subject)" -ForegroundColor Gray
Write-Host "  Thumbprint: $($sig.SignerCertificate.Thumbprint)" -ForegroundColor Gray

# Summary
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Signing Complete!                         " -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Signed file: $ExePath" -ForegroundColor White
Write-Host "File size: $([math]::Round((Get-Item $ExePath).Length / 1MB, 2)) MB" -ForegroundColor Gray
Write-Host ""

if ($sig.Status -eq "Valid") {
    Write-Host "The installer is now digitally signed by Z&T Technologies." -ForegroundColor Green
    Write-Host ""
    Write-Host "DISTRIBUTION:" -ForegroundColor Cyan
    Write-Host "  Send BOTH files to the client:" -ForegroundColor White
    Write-Host "  1. $(Split-Path $ExePath -Leaf)  (the signed installer)" -ForegroundColor Gray
    Write-Host "  2. ZT_Technologies_CodeSign.cer  (the trust certificate)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  Client installs the .cer file FIRST, then runs the installer." -ForegroundColor White
} else {
    Write-Host "NOTE: Signature shows '$($sig.Status)' because this is a self-signed certificate." -ForegroundColor Yellow
    Write-Host "The client must install ZT_Technologies_CodeSign.cer to trust it." -ForegroundColor Yellow
}
Write-Host ""
