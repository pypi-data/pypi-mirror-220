from __future__ import annotations

from .config import APISettings, AppSettings, LoggingSettings
from .config_utils import config_loader

app_settings = AppSettings()
logging_settings = LoggingSettings()
api_settings = APISettings()
