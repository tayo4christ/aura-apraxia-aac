from utils.config import settings


def test_config_defaults():
    assert isinstance(settings.DEMO_MODE, bool)
    assert settings.LOG_LEVEL in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
