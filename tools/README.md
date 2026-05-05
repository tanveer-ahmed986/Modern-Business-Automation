# MBAS License Generator Tools

## Setup Instructions

### 1. Install Required Library

```bash
pip install cryptography
```

### 2. Create License Generator Script

The complete `license_generator.py` script is documented in:
`docs/SALES_AND_LICENSING_GUIDE.md` (Section 6 & Appendix C)

Copy the script from the guide to this directory.

### 3. Generate Keys (First Time Only)

```bash
cd tools
python license_generator.py --generate-keys
```

This creates:
- `private_key.pem` (KEEP SECRET - backup securely!)
- `backend/src/embedded/public_key.pem` (embedded in application)

### 4. Generate Customer Licenses

**Basic Perpetual:**
```bash
python license_generator.py --licensee "ABC Store" --tier basic --type perpetual
```

**Standard Annual:**
```bash
python license_generator.py --licensee "XYZ Shop" --tier standard --type subscription --duration 365
```

**Premium Monthly:**
```bash
python license_generator.py --licensee "MegaMart" --tier premium --type subscription --duration 30
```

### 5. Deliver to Customer

Send the generated `.license` file to customer with instructions to place it at:
`C:\ProgramData\MBAS\mbas.license`

## Security Notes

⚠️ **NEVER share `private_key.pem`**
- Backup to encrypted USB drive
- Store in password manager
- Keep offline backup in safe location

## Support

See `docs/SALES_AND_LICENSING_GUIDE.md` for complete documentation.
