# MBAS Build Instructions

## Prerequisites

### Required Software

1. **Python 3.11+**
   - Download: https://www.python.org/downloads/
   - Ensure `pip` is installed
   - Add Python to PATH

2. **Node.js 18+**
   - Download: https://nodejs.org/
   - npm will be installed automatically

3. **Rust (for Tauri)**
   - Download: https://www.rust-lang.org/tools/install
   - Run: `rustup default stable`

4. **C++ Compiler (for Nuitka)**
   - **Windows**: Install Visual Studio Build Tools or MinGW-w64
   - Download: https://visualstudio.microsoft.com/downloads/
   - Select "Desktop development with C++" workload

### Python Dependencies

Install Nuitka and other build tools:

```bash
pip install nuitka ordered-set zstandard
```

## Build Process

### Option 1: Complete Production Build (Recommended)

Run the automated build pipeline:

```bash
build-all.bat
```

This will:
1. Install backend dependencies
2. Run backend tests
3. Compile backend with Nuitka (~5-15 minutes)
4. Copy backend binary to Tauri
5. Build frontend (React + Vite)
6. Build Tauri MSI installer

**Output**: `tauri-app\src-tauri\target\release\bundle\msi\MBAS_1.0.0_x64.msi`

### Option 2: Quick Development Build

For faster iteration during development:

```bash
build-quick.bat
```

This skips tests and uses debug mode (faster compilation).

### Option 3: Manual Step-by-Step Build

#### Step 1: Build Backend

```bash
cd backend
pip install -r requirements.txt
python scripts/build.py
```

Output: `backend\build\mbas-backend.exe`

#### Step 2: Build Frontend

```bash
cd frontend
npm install
npm run build
```

Output: `frontend\dist\`

#### Step 3: Copy Backend to Tauri

```bash
mkdir tauri-app\src-tauri\binaries
copy backend\build\mbas-backend.exe tauri-app\src-tauri\binaries\
```

#### Step 4: Build Tauri Installer

```bash
cd tauri-app
npm install
npm run tauri build
```

Output: `tauri-app\src-tauri\target\release\bundle\msi\MBAS_1.0.0_x64.msi`

## Verify Build

After building, run the verification script:

```bash
verify-build.bat
```

This checks:
- Backend binary exists and has correct size
- Frontend build is complete
- Tauri installer was created
- All dependencies are bundled

## Build Artifacts

After a successful build, you'll have:

1. **Backend Executable**
   - Location: `backend\build\mbas-backend.exe`
   - Size: ~100-150 MB
   - Standalone FastAPI server

2. **Frontend Bundle**
   - Location: `frontend\dist\`
   - Size: ~2-5 MB
   - Static React application

3. **Tauri Installer**
   - Location: `tauri-app\src-tauri\target\release\bundle\msi\MBAS_1.0.0_x64.msi`
   - Size: ~50-100 MB (without AI model)
   - Size: ~2-3 GB (with AI model)
   - Windows MSI installer

## License Files

Before distributing, generate license files for customers:

```bash
cd tools
python license_generator.py --tier premium --licensee "Customer Name" --duration 365
```

This creates a signed `.mbas-license` file that customers must place in:
- **Development**: Project root
- **Production**: `C:\ProgramData\MBAS\` or app directory

## Distribution

### Package for Customers

1. **Installer**: `MBAS_1.0.0_x64.msi`
2. **License**: `customer-name-tier.mbas-license`
3. **Documentation**: User manual (see `docs/`)

### Installation Instructions for Customers

1. Run `MBAS_1.0.0_x64.msi`
2. Copy `.mbas-license` file to installation directory
3. Launch MBAS application
4. Login with default credentials (admin/admin123)
5. Change default password immediately

## Troubleshooting

### Nuitka Build Fails

**Error**: "C compiler not found"
- **Solution**: Install Visual Studio Build Tools or MinGW-w64

**Error**: "Module not found during compilation"
- **Solution**: Add missing package to `--include-package` in `backend/scripts/build.py`

### Tauri Build Fails

**Error**: "Rust toolchain not found"
- **Solution**: Install Rust from https://rustup.rs/

**Error**: "Frontend dist not found"
- **Solution**: Build frontend first with `cd frontend && npm run build`

### Large Installer Size

**Issue**: Installer is >500 MB
- **Cause**: Likely including AI model or unnecessary files
- **Solution**: Check `.taurignore` and exclude large files

### Backend Won't Start in Production

**Error**: "License file not found"
- **Solution**: Ensure `.mbas-license` file is in the same directory as the executable

**Error**: "SECRET_KEY error"
- **Solution**: Delete `config/secret.key` and restart (will regenerate)

## CI/CD Integration

For automated builds, use:

```bash
build-all.bat
```

Exit codes:
- `0` = Success
- `1` = Build failed

## Build Optimization

### Reduce Build Time

1. **Skip Tests**: Comment out test step in `build-all.bat`
2. **Use Cached Dependencies**: Don't delete `node_modules` or `venv`
3. **Parallel Compilation**: Nuitka uses all CPU cores by default

### Reduce Installer Size

1. **Exclude AI Model**: Don't include `.gguf` files (users download separately)
2. **Strip Debug Symbols**: Use `--strip` flag in Nuitka (already enabled)
3. **Compress Resources**: Tauri automatically compresses assets

## Version Management

To update version number:

1. **Backend**: Update in `backend/scripts/build.py`
2. **Frontend**: Update in `frontend/package.json`
3. **Tauri**: Update in `tauri-app/src-tauri/tauri.conf.json`

Keep all three in sync!

## Testing the Build

### Local Testing

1. Install MSI on local machine
2. Test with different license tiers (Basic/Standard/Premium)
3. Verify all features work correctly
4. Check database creation and persistence

### Clean Machine Testing

1. Use Windows Sandbox or VM
2. Fresh Windows 10/11 installation
3. Install MSI without any development tools
4. Verify application works standalone

### Checklist

- [ ] Application launches without errors
- [ ] Backend starts automatically
- [ ] Login works (admin/admin123)
- [ ] Database initializes correctly
- [ ] License validation works
- [ ] All enabled features accessible
- [ ] Disabled features show upgrade prompt
- [ ] Application uninstalls cleanly

## Support

For build issues:
- Check this documentation
- Review `verify-build.bat` output
- Check GitHub issues: https://github.com/your-repo/issues
- Contact: dev@mbas.local

## Build History

- **v1.0.0** (2026-04-23): Initial production release
  - Backend: Nuitka-compiled FastAPI server
  - Frontend: React + Vite + TailwindCSS
  - Installer: Tauri MSI for Windows
  - Features: Full offline operation, license validation, 3-tier packages
