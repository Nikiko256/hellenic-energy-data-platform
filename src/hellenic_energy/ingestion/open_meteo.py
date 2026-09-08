import calendar
from typing import Any

import requests
from tenacity import (
    calendar,
    Any,
    requests,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
    settings,
)

from hellenic_energy.config import settings

class RetryableOpenMeteoError(Exception):
    """Raised when Open-Meteo returns a temporary error. """
    
class OpenMeteoValidationError(ValueError):
    """Raised when Open-Meteo returnsmalformed or inconsistent data."""
    
    
