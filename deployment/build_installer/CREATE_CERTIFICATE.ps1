# CREATE_CERTIFICATE.ps1
# Creates a self-signed code signing certificate for Z&T Technologies
# Run this script as Administrator in PowerShell

param(
    [string]$CertPassword = "ZTTech2026!Secure",
    [string]$OutputDir = $PSScriptRoot
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Z&T Technologies - Certificate Generator  " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create the self-signed code signing certificate
Write-Host "[1/5] Creating code signing certificate..." -ForegroundColor Yellow

$cert = New-SelfSignedCertificate `
    -Type CodeSigningCert `
    -Subject "CN=Z&T Technologies, O=Z&T Technologies, L=Lahore, S=Punjab, C=PK" `
    -FriendlyName "Z&T Technologies Code Signing Certificate" `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -KeyLength 2048 `
    -KeyAlgorithm RSA `
    -HashAlgorithm SHA256 `
    -KeyExportPolicy Exportable `
    -NotAfter (Get-Date).AddYears(5) `
    -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")

if (-not $cert) {
    Write-Host "ERROR: Failed to create certificate!" -ForegroundColor Red
    exit 1
}

Write-Host "  Certificate created successfully!" -ForegroundColor Green
Write-Host "  Thumbprint: $($cert.Thumbprint)" -ForegroundColor Gray
Write-Host "  Subject: $($cert.Subject)" -ForegroundColor Gray
Write-Host "  Valid until: $($cert.NotAfter)" -ForegroundColor Gray

# Step 2: Export as PFX (private key included - for signing)
Write-Host ""
Write-Host "[2/5] Exporting PFX (private key)..." -ForegroundColor Yellow

$certDir = Join-Path $OutputDir "certificates"
if (-not (Test-Path $certDir)) {
    New-Item -ItemType Directory -Path $certDir -Force | Out-Null
}

$pfxPath = Join-Path $certDir "ZT_Technologies_CodeSign.pfx"
$securePassword = ConvertTo-SecureString -String $CertPassword -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $securePassword | Out-Null
Write-Host "  PFX exported to: $pfxPath" -ForegroundColor Green

# Step 3: Export as CER (public key only - for client distribution)
Write-Host ""
Write-Host "[3/5] Exporting CER (public key for clients)..." -ForegroundColor Yellow

$cerPath = Join-Path $certDir "ZT_Technologies_CodeSign.cer"
Export-Certificate -Cert $cert -FilePath $cerPath | Out-Null
Write-Host "  CER exported to: $cerPath" -ForegroundColor Green

# Step 4: Add certificate to Trusted Root and Trusted Publisher stores (local machine)
Write-Host ""
Write-Host "[4/5] Adding to local Trusted Root & Trusted Publisher stores..." -ForegroundColor Yellow

try {
    # Add to Trusted Root Certification Authorities (CurrentUser)
    $rootStore = New-Object System.Security.Cryptography.X509Certificates.X509Store("Root", "CurrentUser")
    $rootStore.Open("ReadWrite")
    $rootStore.Add($cert)
    $rootStore.Close()
    Write-Host "  Added to Trusted Root (CurrentUser)" -ForegroundColor Green

    # Add to Trusted Publishers (CurrentUser)
    $publisherStore = New-Object System.Security.Cryptography.X509Certificates.X509Store("TrustedPublisher", "CurrentUser")
    $publisherStore.Open("ReadWrite")
    $publisherStore.Add($cert)
    $publisherStore.Close()
    Write-Host "  Added to Trusted Publisher (CurrentUser)" -ForegroundColor Green
} catch {
    Write-Host "  Warning: Could not add to local stores. Run as Administrator for this step." -ForegroundColor Yellow
}

# Step 5: Save thumbprint for build scripts
Write-Host ""
Write-Host "[5/5] Saving certificate info..." -ForegroundColor Yellow

$cert.Thumbprint | Out-File -FilePath (Join-Path $certDir "thumbprint.txt") -NoNewline -Encoding ASCII
Write-Host "  Thumbprint saved to: $(Join-Path $certDir 'thumbprint.txt')" -ForegroundColor Green

# Summary
Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  Certificate Generation Complete!          " -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files created:" -ForegroundColor White
Write-Host "  1. $pfxPath" -ForegroundColor Gray
Write-Host "     (KEEP SECURE - contains private key for signing)" -ForegroundColor DarkYellow
Write-Host "  2. $cerPath" -ForegroundColor Gray
Write-Host "     (DISTRIBUTE - clients install this to trust your apps)" -ForegroundColor DarkYellow
Write-Host ""
Write-Host "Certificate Thumbprint: $($cert.Thumbprint)" -ForegroundColor White
Write-Host "PFX Password: $CertPassword" -ForegroundColor White
Write-Host ""
Write-Host "NEXT STEPS:" -ForegroundColor Cyan
Write-Host "  1. Run SIGN_INSTALLER.ps1 to sign your EXE" -ForegroundColor White
Write-Host "  2. Send ZT_Technologies_CodeSign.cer to clients" -ForegroundColor White
Write-Host "  3. Clients run INSTALL_ZT_CERTIFICATE.bat before installing MBAS" -ForegroundColor White
Write-Host ""
