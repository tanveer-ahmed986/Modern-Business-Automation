# This script would be responsible for configuring and running Nuitka
# to compile the Python backend into a standalone executable.
# The actual Nuitka command will vary based on project structure,
# required modules, and target OS.

import os
import subprocess
import sys

def build_with_nuitka():
    print("Starting Nuitka build for the backend...")
    
    # Define paths
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    main_script = os.path.join(backend_dir, "src", "main.py")
    output_dir = os.path.join(backend_dir, "build")
    
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

    nuitka_cmd = [
        sys.executable,  # Use the current Python interpreter for Nuitka
        "-m", "nuitka",
        "--standalone",  # Create a self-contained executable
        "--onefile",     # Create a single file executable
        "--output-dir=" + output_dir,
        "--output-filename=mbas_backend",
        "--enable-plugin=pylint-warnings", # Example plugin
        "--follow-imports", # Follow all imports
        "--include-package=fastapi",
        "--include-package=uvicorn",
        "--include-package=sqlmodel",
        "--include-package=pydantic_settings",
        "--include-package=jose",
        "--include-package=passlib",
        "--include-package=pandas",
        "--include-package=sklearn",
        "--include-package=numpy",
        # Add more packages as needed by your application
        main_script
    ]
    
    # Only try to include llama_cpp if it's actually installed and needed
    # if "llama_cpp" in sys.modules: # This check might be too late
    #     nuitka_cmd.append("--include-package=llama_cpp")
    #     nuitka_cmd.append("--include-data-dir=./models=models") # For GGUF models

    print(f"Running Nuitka command: {' '.join(nuitka_cmd)}")

    try:
        subprocess.run(nuitka_cmd, check=True, cwd=backend_dir)
        print(f"Nuitka build successful! Executable in: {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"Nuitka build failed: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: Nuitka or Python not found. Ensure Nuitka is installed (`pip install nuitka`) and in your PATH.")
        sys.exit(1)

if __name__ == "__main__":
    build_with_nuitka()
