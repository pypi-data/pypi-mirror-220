from __future__ import annotations

def config_loader(log_level: str = "INFO") -> dict:
    _settings: dict = {"LOG_LEVEL": log_level}

    return _settings
