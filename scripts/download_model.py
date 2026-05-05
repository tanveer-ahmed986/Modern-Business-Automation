#!/usr/bin/env python3
"""
MBAS AI Model Downloader

Downloads the Phi-3-mini-4k-instruct quantized model for offline AI features.
This model is required for Premium tier AI capabilities.
"""

import urllib.request
import sys
from pathlib import Path
from typing import Optional


# Model configuration
MODEL_NAME = "Phi-3-mini-4k-instruct"
MODEL_VARIANT = "q4"  # Quantized 4-bit for CPU efficiency
MODEL_URL = "https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf/resolve/main/Phi-3-mini-4k-instruct-q4.gguf"
MODEL_SIZE_MB = 2300  # Approximate size in MB

# Installation paths
MODELS_DIR = Path(__file__).parent.parent / "models"
TAURI_MODELS_DIR = Path(__file__).parent.parent / "tauri-app" / "resources" / "models"
MODEL_FILENAME = f"{MODEL_NAME}.{MODEL_VARIANT}.gguf"


def format_bytes(bytes_count: int) -> str:
    """Format bytes to human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_count < 1024.0:
            return f"{bytes_count:.2f} {unit}"
        bytes_count /= 1024.0
    return f"{bytes_count:.2f} TB"


def download_progress_hook(block_count: int, block_size: int, total_size: int):
    """Progress callback for urllib download."""
    downloaded = block_count * block_size

    if total_size > 0:
        percent = min(100, downloaded * 100 / total_size)
        downloaded_mb = downloaded / (1024 * 1024)
        total_mb = total_size / (1024 * 1024)

        # Progress bar
        bar_length = 50
        filled = int(bar_length * percent / 100)
        bar = '=' * filled + '-' * (bar_length - filled)

        print(f'\r[{bar}] {percent:.1f}% ({downloaded_mb:.1f}/{total_mb:.1f} MB)', end='', flush=True)
    else:
        # Unknown size
        downloaded_mb = downloaded / (1024 * 1024)
        print(f'\rDownloaded: {downloaded_mb:.1f} MB', end='', flush=True)


def download_model(target_dir: Path) -> Optional[Path]:
    """
    Download the AI model from HuggingFace.

    Args:
        target_dir: Directory to save the model

    Returns:
        Path to downloaded model, or None if failed
    """
    model_path = target_dir / MODEL_FILENAME

    # Create directory if it doesn't exist
    target_dir.mkdir(parents=True, exist_ok=True)

    # Check if already downloaded
    if model_path.exists():
        file_size = model_path.stat().st_size
        print(f"[OK] Model already exists: {model_path}")
        print(f"     Size: {format_bytes(file_size)}")
        return model_path

    print(f"Downloading {MODEL_NAME} model...")
    print(f"Source: {MODEL_URL}")
    print(f"Target: {model_path}")
    print(f"Expected size: ~{MODEL_SIZE_MB} MB")
    print()
    print("This may take 5-30 minutes depending on your internet connection...")
    print()

    try:
        # Download with progress
        urllib.request.urlretrieve(MODEL_URL, model_path, reporthook=download_progress_hook)
        print()  # New line after progress bar

        # Verify download
        file_size = model_path.stat().st_size
        print()
        print(f"[OK] Download complete!")
        print(f"     Location: {model_path}")
        print(f"     Size: {format_bytes(file_size)}")

        return model_path

    except KeyboardInterrupt:
        print()
        print()
        print("[!] Download cancelled by user")

        # Clean up partial download
        if model_path.exists():
            model_path.unlink()
            print(f"[!] Removed partial download: {model_path}")

        return None

    except Exception as e:
        print()
        print()
        print(f"[ERROR] Download failed: {e}")

        # Clean up partial download
        if model_path.exists():
            model_path.unlink()
            print(f"[!] Removed partial download: {model_path}")

        return None


def verify_model(model_path: Path) -> bool:
    """
    Verify the downloaded model is valid.

    Args:
        model_path: Path to model file

    Returns:
        True if valid, False otherwise
    """
    if not model_path.exists():
        print(f"[ERROR] Model file not found: {model_path}")
        return False

    file_size = model_path.stat().st_size

    # Check minimum size (should be at least 1GB for a valid model)
    if file_size < 1_000_000_000:
        print(f"[ERROR] Model file too small ({format_bytes(file_size)}). Download may be corrupted.")
        return False

    # Check file extension
    if not model_path.suffix == '.gguf':
        print(f"[ERROR] Invalid file extension. Expected .gguf, got {model_path.suffix}")
        return False

    print(f"[OK] Model verification passed")
    return True


def main():
    print("=" * 70)
    print("  MBAS AI Model Downloader")
    print("=" * 70)
    print()

    # Choose installation location
    print("Select installation location:")
    print("  1. Development mode (models/)")
    print("  2. Production mode (tauri-app/resources/models/)")
    print("  3. Both locations")
    print()

    choice = input("Enter choice (1-3) [default: 3]: ").strip() or "3"
    print()

    success = True

    if choice in ["1", "3"]:
        print("Downloading to development location...")
        print("-" * 70)
        dev_model = download_model(MODELS_DIR)
        if dev_model and verify_model(dev_model):
            print("[OK] Development model ready")
        else:
            print("[FAIL] Development model download failed")
            success = False
        print()

    if choice in ["2", "3"]:
        print("Downloading to production location...")
        print("-" * 70)
        prod_model = download_model(TAURI_MODELS_DIR)
        if prod_model and verify_model(prod_model):
            print("[OK] Production model ready")
        else:
            print("[FAIL] Production model download failed")
            success = False
        print()

    if success:
        print("=" * 70)
        print("  MODEL DOWNLOAD COMPLETE!")
        print("=" * 70)
        print()
        print("Next steps:")
        print("  1. The AI model is now available for Premium tier users")
        print("  2. Ensure llama-cpp-python is installed:")
        print("     pip install llama-cpp-python")
        print("  3. Test the AI features:")
        print("     - Start backend: cd backend && python -m src.main")
        print("     - Access AI endpoints: /ai/predict, /ai/query")
        print("  4. For production builds:")
        print("     - Model will be bundled in Tauri installer")
        print("     - Installer size will be ~2.5-3 GB")
        print()
    else:
        print("=" * 70)
        print("  MODEL DOWNLOAD FAILED")
        print("=" * 70)
        print()
        print("Troubleshooting:")
        print("  - Check your internet connection")
        print("  - Ensure you have ~2.5 GB free disk space")
        print("  - Try downloading manually from:")
        print(f"    {MODEL_URL}")
        print("  - Save to: models/ or tauri-app/resources/models/")
        print()
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("[!] Download cancelled by user")
        sys.exit(1)
