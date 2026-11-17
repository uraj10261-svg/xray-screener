"""Stage 1 helper: inspects YOUR computer and tells you what is missing.

Run:  python check_environment.py
"""
import importlib
import platform
import shutil
import sys

PACKAGES = ["torch", "torchvision", "numpy", "pandas", "PIL", "sklearn",
            "matplotlib", "cv2", "streamlit", "openai", "pytest"]


def main() -> None:
    print("=== Environment check ===")
    print(f"OS            : {platform.system()} {platform.release()}")
    print(f"Python        : {sys.version.split()[0]}  (need 3.9 - 3.12)")
    print(f"Free disk (GB): {shutil.disk_usage('.').free / 1e9:.1f}  (need ~5+)")

    missing = []
    for name in PACKAGES:
        try:
            mod = importlib.import_module(name)
            print(f"[OK]      {name} {getattr(mod, '__version__', '')}")
        except ImportError:
            print(f"[MISSING] {name}")
            missing.append(name)

    try:
        import torch
        if torch.cuda.is_available():
            print(f"GPU           : {torch.cuda.get_device_name(0)} (CUDA available)")
        else:
            print("GPU           : none found - training will use CPU (slower; Colab GPU recommended)")
    except ImportError:
        print("GPU           : cannot check until torch is installed")

    import config
    print(f"Dataset folder: {config.DATA_DIR} -> {'FOUND' if config.DATA_DIR.exists() else 'NOT FOUND (you will download it in Stage 2)'}")
    print(f"XAI_API_KEY   : {'set' if config.XAI_API_KEY else 'not set (optional - app works without it)'}")
    print("\nMissing packages:", missing if missing else "none")


if __name__ == "__main__":
    main()
