"""HTTP API and static frontend for the pneumonia X-ray research prototype."""

from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from PIL import Image, UnidentifiedImageError
from werkzeug.exceptions import RequestEntityTooLarge

from config import ALLOWED_EXTENSIONS, MAX_UPLOAD_MB, MEDICAL_DISCLAIMER

PROJECT_ROOT = Path(__file__).resolve().parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"
MAX_UPLOAD_BYTES = MAX_UPLOAD_MB * 1024 * 1024
IMAGE_FORMATS = {
    ".jpg": "JPEG",
    ".jpeg": "JPEG",
    ".png": "PNG",
}

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES + 64 * 1024


@app.get("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


@app.get("/api/health")
def health():
    return jsonify(
        status="ok",
        model_available=False,
        message="The prediction model is not configured.",
    )


@app.errorhandler(RequestEntityTooLarge)
def request_too_large(_error):
    return jsonify(
        error="file_too_large",
        message=f"Upload an image smaller than {MAX_UPLOAD_MB} MB.",
    ), 413


@app.post("/api/screen")
def screen():
    uploaded_file = request.files.get("image")
    if uploaded_file is None or not uploaded_file.filename:
        return jsonify(
            error="image_required",
            message="Choose a chest X-ray image to continue.",
        ), 400

    extension = Path(uploaded_file.filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        return jsonify(
            error="unsupported_file_type",
            message="Use a JPG, JPEG, or PNG image.",
        ), 415

    uploaded_file.stream.seek(0, 2)
    upload_size = uploaded_file.stream.tell()
    uploaded_file.stream.seek(0)
    if upload_size > MAX_UPLOAD_BYTES:
        return jsonify(
            error="file_too_large",
            message=f"Upload an image smaller than {MAX_UPLOAD_MB} MB.",
        ), 413

    try:
        image = Image.open(uploaded_file.stream)
        image_format = image.format
        image.verify()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        return jsonify(
            error="invalid_image",
            message="The selected file is not a valid supported image.",
        ), 400

    if image_format != IMAGE_FORMATS.get(extension):
        return jsonify(
            error="file_extension_mismatch",
            message="The image content does not match its file extension.",
        ), 400

    return jsonify(
        error="model_not_configured",
        message=(
            "The image was received and validated, but no trained model or "
            "prediction pipeline is available yet. No screening result was produced."
        ),
        disclaimer=MEDICAL_DISCLAIMER,
    ), 503


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
