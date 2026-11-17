"""Stage 1 test: makes sure the basic settings are sane."""
import config


def test_class_names():
    assert config.CLASS_NAMES == ["NORMAL", "PNEUMONIA"]


def test_no_hardcoded_api_key():
    # The key must come from the environment, never be written in code.
    import inspect
    assert "xai-" not in inspect.getsource(config)


def test_disclaimer_says_not_diagnostic():
    assert "NOT a diagnostic tool" in config.MEDICAL_DISCLAIMER
