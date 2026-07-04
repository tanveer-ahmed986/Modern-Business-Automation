# MBAS License Generator - Interactive PowerShell Script
# Generates cryptographically signed licenses with RSA-4096
# Run with: powershell -ExecutionPolicy Bypass -File GENERATE_LICENSE.ps1

function Start-LicenseGenerator {
    Clear-Host

    Write-Host ""
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host "         MBAS LICENSE GENERATOR - INTERACTIVE" -ForegroundColor Cyan
    Write-Host "          Cryptographically Signed Licenses" -ForegroundColor Cyan
    Write-Host "================================================================" -ForegroundColor Cyan
    Write-Host ""

    # Check if Python is installed
    try {
        $pythonVersion = & python --version 2>&1
        Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
        Write-Host ""
    } catch {
        Write-Host "[ERROR] Python is not installed!" -ForegroundColor Red
        Write-Host "Please install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }

    # STEP 1: License Tier
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host "   STEP 1: SELECT LICENSE TIER" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1. Basic Edition" -ForegroundColor White
    Write-Host "     - Dashboard, Inventory, Billing, Reports" -ForegroundColor Gray
    Write-Host "     - Customer & Supplier Management" -ForegroundColor Gray
    Write-Host "     - Backup & Restore" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. Standard Edition" -ForegroundColor White
    Write-Host "     - All Basic features +" -ForegroundColor Gray
    Write-Host "     - Advanced Reports & Analytics" -ForegroundColor Gray
    Write-Host "     - Multi-user Support" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  3. Premium Edition" -ForegroundColor White
    Write-Host "     - All Standard features +" -ForegroundColor Gray
    Write-Host "     - AI Sales Forecasting" -ForegroundColor Gray
    Write-Host "     - Premium Analytics Dashboard" -ForegroundColor Gray
    Write-Host "     - Priority Support" -ForegroundColor Gray
    Write-Host ""

    do {
        $tierChoice = Read-Host "Enter choice (1-3)"
    } while ($tierChoice -notin @("1", "2", "3"))

    $tiers = @{
        "1" = @{ name = "basic"; display = "Basic" }
        "2" = @{ name = "standard"; display = "Standard" }
        "3" = @{ name = "premium"; display = "Premium" }
    }

    $tier = $tiers[$tierChoice].name
    $tierDisplay = $tiers[$tierChoice].display

    # STEP 2: License Type
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host "   STEP 2: SELECT LICENSE TYPE" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1. Perpetual (Lifetime)" -ForegroundColor White
    Write-Host "     - One-time payment" -ForegroundColor Gray
    Write-Host "     - No expiration date" -ForegroundColor Gray
    Write-Host "     - Customer owns license forever" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  2. Subscription (Recurring)" -ForegroundColor White
    Write-Host "     - Monthly, Quarterly, or Annual" -ForegroundColor Gray
    Write-Host "     - Expires after duration" -ForegroundColor Gray
    Write-Host "     - Requires renewal" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  3. Trial (Free Trial)" -ForegroundColor White
    Write-Host "     - 14 days by default" -ForegroundColor Gray
    Write-Host "     - Full features, limited time" -ForegroundColor Gray
    Write-Host "     - Perfect for demos" -ForegroundColor Gray
    Write-Host ""

    do {
        $typeChoice = Read-Host "Enter choice (1-3)"
    } while ($typeChoice -notin @("1", "2", "3"))

    $types = @{
        "1" = @{ name = "perpetual"; display = "Perpetual" }
        "2" = @{ name = "subscription"; display = "Subscription" }
        "3" = @{ name = "trial"; display = "Trial" }
    }

    $type = $types[$typeChoice].name
    $typeDisplay = $types[$typeChoice].display
    $duration = $null

    # Ask for duration if subscription or trial
    if ($type -eq "subscription") {
        Write-Host ""
        Write-Host "============================================" -ForegroundColor Yellow
        Write-Host "   SUBSCRIPTION DURATION" -ForegroundColor Yellow
        Write-Host "============================================" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "  1. Monthly (30 days)" -ForegroundColor White
        Write-Host "  2. Quarterly (90 days)" -ForegroundColor White
        Write-Host "  3. Semi-Annual (180 days)" -ForegroundColor White
        Write-Host "  4. Annual (365 days)" -ForegroundColor White
        Write-Host "  5. Custom duration" -ForegroundColor White
        Write-Host ""

        do {
            $durationChoice = Read-Host "Enter choice (1-5)"
        } while ($durationChoice -notin @("1", "2", "3", "4", "5"))

        $durations = @{
            "1" = 30
            "2" = 90
            "3" = 180
            "4" = 365
        }

        if ($durationChoice -eq "5") {
            do {
                $duration = Read-Host "Enter number of days (1-3650)"
            } while (-not ($duration -match '^\d+$') -or [int]$duration -lt 1 -or [int]$duration -gt 3650)
        } else {
            $duration = $durations[$durationChoice]
        }
    } elseif ($type -eq "trial") {
        $duration = 14
    }

    # STEP 3: Business Information
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host "   STEP 3: BUSINESS INFORMATION" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Enter the customer's business name." -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Gray
    Write-Host "  - ABC Pharmacy" -ForegroundColor Gray
    Write-Host "  - XYZ Electronics Shop" -ForegroundColor Gray
    Write-Host "  - Premium Medical Store" -ForegroundColor Gray
    Write-Host "  - City Retail Center" -ForegroundColor Gray
    Write-Host ""

    do {
        $businessName = Read-Host "Business name"
    } while ([string]::IsNullOrWhiteSpace($businessName))

    # STEP 4: Hardware Lock
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host "   STEP 4: HARDWARE LOCK (OPTIONAL)" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Lock license to specific computer?" -ForegroundColor White
    Write-Host "(Prevents license from being used on other computers)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Press Y to lock to hardware, or N to skip" -ForegroundColor White
    Write-Host ""

    $lockChoice = Read-Host "Your choice (Y/N)"
    $machineId = $null

    if ($lockChoice -eq "Y" -or $lockChoice -eq "y") {
        Write-Host ""
        Write-Host "Enter machine ID hash (or press Enter to skip):" -ForegroundColor White
        Write-Host ""
        Write-Host "Note: Customer can get their machine ID by running:" -ForegroundColor Gray
        Write-Host "  python -c `"from src.core.license import LicenseValidator; print(LicenseValidator.get_machine_id())`"" -ForegroundColor Gray
        Write-Host ""
        $machineId = Read-Host "Machine ID (optional)"

        if ([string]::IsNullOrWhiteSpace($machineId)) {
            $machineId = $null
        }
    }

    # Confirmation
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host "   CONFIRMATION" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "License Details:" -ForegroundColor Cyan
    Write-Host "  Business Name: $businessName" -ForegroundColor White
    Write-Host "  Tier:          $tierDisplay" -ForegroundColor White
    Write-Host "  Type:          $typeDisplay" -ForegroundColor White
    if ($duration) {
        Write-Host "  Duration:      $duration days" -ForegroundColor White
    }
    if ($machineId) {
        Write-Host "  Machine Lock:  $machineId" -ForegroundColor White
    }
    Write-Host ""
    Write-Host "Output file: license\mbas.license" -ForegroundColor Yellow
    Write-Host ""

    $confirm = Read-Host "Generate license? (Y/N)"

    if ($confirm -ne "Y" -and $confirm -ne "y") {
        Write-Host ""
        Write-Host "License generation cancelled." -ForegroundColor Yellow
        Write-Host ""
        Read-Host "Press Enter to exit"
        return
    }

    # Generate License
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host "   GENERATING SIGNED LICENSE..." -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Yellow
    Write-Host ""

    # Change to project root
    $projectRoot = Split-Path -Parent $PSScriptRoot
    Set-Location $projectRoot

    # Build the command
    $cmd = "python tools/sign_license.py --licensee `"$businessName`" --tier $tier --type $type"

    if ($duration) {
        $cmd += " --duration $duration"
    }

    if ($machineId) {
        $cmd += " --machine-id `"$machineId`""
    }

    $cmd += " --output license/mbas.license"

    # Execute the command
    Write-Host "[*] Signing license with RSA-4096 private key..." -ForegroundColor Cyan
    Write-Host ""

    try {
        Invoke-Expression $cmd

        if ($LASTEXITCODE -ne 0) {
            throw "License generation failed with exit code $LASTEXITCODE"
        }

        Write-Host ""
        Write-Host "============================================" -ForegroundColor Green
        Write-Host "   SUCCESS!" -ForegroundColor Green
        Write-Host "============================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "License file created: license\mbas.license" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Next steps:" -ForegroundColor Yellow
        Write-Host "  1. Review the license file (license\mbas.license)" -ForegroundColor White
        Write-Host "  2. Copy mbas.license to the deployment package" -ForegroundColor White
        Write-Host "  3. Or send mbas.license to customer via secure email" -ForegroundColor White
        Write-Host "  4. Customer places it in their MBAS installation folder" -ForegroundColor White
        Write-Host "  5. Customer starts MBAS and enjoys $tierDisplay features!" -ForegroundColor White
        Write-Host ""

        # Copy to deployment package if it exists
        $deploymentPath = Join-Path $projectRoot "deployment\MBAS_Package\mbas.license"
        if (Test-Path (Split-Path $deploymentPath -Parent)) {
            Copy-Item "license\mbas.license" $deploymentPath -Force -ErrorAction SilentlyContinue
            if ($?) {
                Write-Host "[+] License copied to deployment package" -ForegroundColor Green
                Write-Host "    Location: $deploymentPath" -ForegroundColor Gray
                Write-Host ""
            }
        }

        # Ask if user wants to view the license
        $view = Read-Host "View license file? (Y/N)"
        if ($view -eq "Y" -or $view -eq "y") {
            Write-Host ""
            Write-Host "--- LICENSE FILE CONTENTS ---" -ForegroundColor Cyan
            Get-Content "license\mbas.license"
            Write-Host ""
            Write-Host "--- END OF FILE ---" -ForegroundColor Cyan
            Write-Host ""
        }

        # Create a summary file
        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $summary = @"
License Generation Summary
==========================
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

Business Name: $businessName
Tier: $tierDisplay
Type: $typeDisplay
$(if ($duration) { "Duration: $duration days" } else { "" })
$(if ($machineId) { "Machine ID: $machineId" } else { "" })

Output File: license\mbas.license
Signature: RSA-4096 Cryptographic Signature

IMPORTANT:
- This license is cryptographically signed and tamper-proof
- Customer must place it in their MBAS installation folder
- License will be validated on every MBAS startup
- Keep a backup copy of this license for customer support
"@

        $summaryFile = "license\license_summary_$timestamp.txt"
        $summary | Out-File -FilePath $summaryFile -Encoding UTF8
        Write-Host "Summary saved to: $summaryFile" -ForegroundColor Green
        Write-Host ""

        # Ask if user wants to generate another license
        $another = Read-Host "Generate another license? (Y/N)"
        if ($another -eq "Y" -or $another -eq "y") {
            Start-LicenseGenerator
        }

    } catch {
        Write-Host ""
        Write-Host "============================================" -ForegroundColor Red
        Write-Host "[ERROR] License generation failed!" -ForegroundColor Red
        Write-Host "============================================" -ForegroundColor Red
        Write-Host ""
        Write-Host $_.Exception.Message -ForegroundColor Red
        Write-Host ""
        Write-Host "Possible issues:" -ForegroundColor Yellow
        Write-Host "  - Private key not found in tools/keys/" -ForegroundColor White
        Write-Host "  - Python dependencies missing (cryptography)" -ForegroundColor White
        Write-Host "  - Invalid input parameters" -ForegroundColor White
        Write-Host ""
        Write-Host "To install dependencies:" -ForegroundColor Yellow
        Write-Host "  pip install cryptography" -ForegroundColor White
        Write-Host ""
        Read-Host "Press Enter to exit"
        exit 1
    }

    Write-Host ""
    Write-Host "Thank you for using MBAS License Generator!" -ForegroundColor Cyan
    Write-Host ""
    Read-Host "Press Enter to exit"
}

# Start the generator
Start-LicenseGenerator
