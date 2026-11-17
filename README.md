# AI-Powered Pneumonia X-ray Screener

An educational research prototype that screens pediatric chest X-rays for signs consistent with pneumonia,
with Grad-CAM explanations. **Not a diagnostic tool. Not for clinical use.**

## Status
- [x] Stage 1: project structure and environment check
- [ ] Stage 2: dataset loading, validation, leakage-safe split
- [ ] Stage 3: preprocessing, models (ResNet18, DenseNet121)
- [ ] Stage 4: training and model comparison
- [ ] Stage 5: evaluation and thresholds
- [ ] Stage 6: Grad-CAM
- [ ] Stage 7: optional Grok integration
- [ ] Stage 8: Streamlit app
- [ ] Stage 9: tests and final review

No model weights or metrics are included. Every number shown by this project must come from your own training run.

## Setup (Windows PowerShell, VS Code terminal)
```powershell
cd pneumonia-xray-screener
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
# CPU-only PyTorch:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
python check_environment.py
python -m pytest tests/test_config.py -v
```
If activation is blocked: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Web frontend and API
Start the local HTML/CSS/JavaScript frontend and upload API from the project root:
```powershell
python backend.py
```
Open `http://127.0.0.1:5000`. The frontend posts image uploads to `/api/screen` and checks `/api/health`.
The backend validates JPG/JPEG/PNG uploads (up to 10 MB). A trained model and prediction pipeline
are not included yet, so valid uploads currently return `503 model_not_configured` rather than a prediction.

## Google Colab (recommended for training)
Runtime > Change runtime type > GPU, then:
```python
from google.colab import drive; drive.mount('/content/drive')
!unzip -q /content/pneumonia-xray-screener.zip -d /content
%cd /content/pneumonia-xray-screener
!pip install -q -r requirements.txt
!python check_environment.py
```

## Folder map
- `src/data`: loading, validation, splits, transforms
- `src/models`: ResNet18 / DenseNet121
- `src/training`: training loop, comparison
- `src/evaluation`: metrics, thresholds
- `src/explainability`: Grad-CAM
- `src/integrations`: optional Grok helper
- `app/`: planned Streamlit pages
- `frontend/index.html`: standalone browser frontend
- `backend.py`: local Flask API and frontend server
- `tests/`: automated tests
