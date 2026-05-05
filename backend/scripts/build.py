# This script would be responsible for configuring and running Nuitka
# to compile the Python backend into a standalone executable.
# The actual Nuitka command will vary based on project structure,
# required modules, and target OS.

import os
import subprocess
import sys

def build_with_nuitka():
    print("=" * 60)
    print("  MBAS Backend - Nuitka Build")
    print("=" * 60)
    print()

    # Define paths
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    main_script = os.path.join(backend_dir, "src", "main.py")
    output_dir = os.path.join(backend_dir, "build")

    # Verify main script exists
    if not os.path.exists(main_script):
        print(f"[ERROR] Main script not found: {main_script}")
        sys.exit(1)

    print(f"[1/4] Backend directory: {backend_dir}")
    print(f"[2/4] Main script: {main_script}")
    print(f"[3/4] Output directory: {output_dir}")
    print()

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Nuitka command - simplified example
    # In a real scenario, you'd add many options:
    # --onefile (for a single executable)
    # --standalone (for a self-contained executable)
    # --include-package (for packages like sqlmodel, fastapi, uvicorn, sklearn etc.)
    # --include-data-dir (for database files, static assets if any)
    # --plugin-enable=pyside6 (if using Qt, for example)
    # --windows-disable-console (for GUI apps)
    # --output-filename (to specify the name)
    # --mingw64 (for Windows builds with MinGW)
    # --python-flag=no_dla (for faster startup)

    # Find embedded resources
    embedded_dir = os.path.join(backend_dir, "src", "embedded")
    public_key_path = os.path.join(embedded_dir, "public_key.pem")

    nuitka_cmd = [
        sys.executable,  # Use the current Python interpreter for Nuitka
        "-m", "nuitka",
        "--standalone",  # Create a self-contained executable
        "--onefile",     # Create a single file executable
        "--output-dir=" + output_dir,
        "--output-filename=mbas-backend.exe",
        "--windows-console-mode=disable",  # Hide console window (GUI mode)
        "--follow-imports",  # Follow all imports

        # Include all required packages
        "--include-package=fastapi",
        "--include-package=uvicorn",
        "--include-package=sqlmodel",
        "--include-package=pydantic",
        "--include-package=pydantic_settings",
        "--include-package=jose",
        "--include-package=passlib",
        "--include-package=python-multipart",
        "--include-package=pandas",
        "--include-package=numpy",
        "--include-package=sklearn",
        "--include-package=cryptography",

        # Include embedded resources (license public key)
        f"--include-data-file={public_key_path}=embedded/public_key.pem",

        # Enable numpy plugin for better compatibility
        "--plugin-enable=numpy",

        # Windows-specific icon (optional, if icon file exists)
        # "--windows-icon-from-ico=../tauri-app/src-tauri/icons/icon.ico",

        main_script
    ]
    
    # Only try to include llama_cpp if it's actually installed and needed
    # if "llama_cpp" in sys.modules: # This check might be too late
    #     nuitka_cmd.append("--include-package=llama_cpp")
    #     nuitka_cmd.append("--include-data-dir=./models=models") # For GGUF models

    print("[4/4] Starting Nuitka compilation...")
    print("      This may take several minutes (5-15 min depending on system)...")
    print()

    try:
        result = subprocess.run(nuitka_cmd, check=True, cwd=backend_dir, capture_output=False)

        print()
        print("=" * 60)
        print("  BUILD SUCCESSFUL!")
        print("=" * 60)

        # Verify output file exists
        output_exe = os.path.join(output_dir, "mbas-backend.exe")
        if os.path.exists(output_exe):
            file_size_mb = os.path.getsize(output_exe) / (1024 * 1024)
            print(f"Executable: {output_exe}")
            print(f"Size: {file_size_mb:.1f} MB")
            print()
            print("Next steps:")
            print("  1. Test the executable: cd build && mbas-backend.exe")
            print("  2. Copy to Tauri: copy build\\mbas-backend.exe ..\\tauri-app\\src-tauri\\binaries\\")
            print("  3. Build Tauri installer: cd ..\\tauri-app && npm run tauri build")
        else:
            print(f"[WARNING] Expected output file not found: {output_exe}")

        print()

    except subprocess.CalledProcessError as e:
        print()
        print("=" * 60)
        print("  BUILD FAILED!")
        print("=" * 60)
        print(f"Error: {e}")
        print()
        print("Troubleshooting:")
        print("  1. Ensure Nuitka is installed: pip install nuitka")
        print("  2. Install C compiler (Windows: MinGW-w64 or MSVC)")
        print("  3. Check that all dependencies are installed")
        print()
        sys.exit(1)
    except FileNotFoundError:
        print()
        print("=" * 60)
        print("  ERROR: Nuitka not found")
        print("=" * 60)
        print()
        print("Please install Nuitka: pip install nuitka")
        print()
        sys.exit(1)

if __name__ == "__main__":
    build_with_nuitka()
