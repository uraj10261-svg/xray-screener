"""Central settings for the whole project.

Beginner note: keeping settings in ONE file means you change a value here
(for example the image size) and every other file picks it up automatically.
"""
from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parent

# Dataset location: set the environment variable PNEUMONIA_DATA_DIR, or edit
# the fallback path. We do NOT assume the dataset exists (see check_environment.py).
DATA_DIR = Path(os.environ.get("PNEUMONIA_DATA_DIR", PROJECT_ROOT / "data" / "raw" / "chest_xray"))

CHECKPOINT_DIR = PROJECT_ROOT / "models" / "checkpoints"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
REPORTS_DIR = PROJECT_ROOT / "outputs" / "reports"

CLASS_NAMES = ["NORMAL", "PNEUMONIA"]   # label 0 = NORMAL, label 1 = PNEUMONIA
IMAGE_SIZE = 224
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]

SEED = 42
BATCH_SIZE = 32
MAX_EPOCHS = 20
EARLY_STOP_PATIENCE = 4
LEARNING_RATE = 1e-4
VAL_FRACTION = 0.15            # carved from train, patient-aware (Stage 2)

MODEL_NAMES = ["resnet18", "densenet121"]

# Optional Grok (xAI). The key is read from the environment, never hardcoded.
XAI_API_KEY = os.environ.get("XAI_API_KEY")
XAI_BASE_URL = "https://api.x.ai/v1"

MAX_UPLOAD_MB = 10
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}

MEDICAL_DISCLAIMER = (
    "This is an educational research prototype, NOT a diagnostic tool. "
    "It must not be used for medical decisions. Always consult a qualified clinician."
)
