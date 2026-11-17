from io import BytesIO

from PIL import Image

import backend


def image_upload(name="sample.png", image_format="PNG"):
    image = Image.new("RGB", (16, 16), color="white")
    stream = BytesIO()
    image.save(stream, format=image_format)
    stream.seek(0)
    return stream, name


def test_health_reports_model_unavailable():
    response = backend.app.test_client().get("/api/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"
    assert response.json["model_available"] is False


def test_screen_rejects_missing_image():
    response = backend.app.test_client().post("/api/screen")

    assert response.status_code == 400
    assert response.json["error"] == "image_required"


def test_screen_rejects_unsupported_extension():
    response = backend.app.test_client().post(
        "/api/screen",
        data={"image": (BytesIO(b"not an image"), "sample.gif")},
    )

    assert response.status_code == 415
    assert response.json["error"] == "unsupported_file_type"


def test_screen_validates_image_and_reports_missing_model():
    stream, filename = image_upload()
    response = backend.app.test_client().post(
        "/api/screen",
        data={"image": (stream, filename)},
        content_type="multipart/form-data",
    )

    assert response.status_code == 503
    assert response.json["error"] == "model_not_configured"
    assert "No screening result was produced" in response.json["message"]


def test_screen_rejects_mismatched_extension():
    stream, _ = image_upload(image_format="PNG")
    response = backend.app.test_client().post(
        "/api/screen",
        data={"image": (stream, "sample.jpg")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.json["error"] == "file_extension_mismatch"


def test_screen_rejects_upload_over_configured_limit():
    response = backend.app.test_client().post(
        "/api/screen",
        data={
            "image": (
                BytesIO(b"x" * (backend.MAX_UPLOAD_BYTES + 1)),
                "sample.png",
            )
        },
        content_type="multipart/form-data",
    )

    assert response.status_code == 413
    assert response.json["error"] == "file_too_large"


def test_frontend_is_served():
    response = backend.app.test_client().get("/")

    assert response.status_code == 200
    assert b"/api/screen" in response.data
