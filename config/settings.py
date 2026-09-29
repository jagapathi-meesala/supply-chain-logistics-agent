import os

# Deterministic settings. Avoid relying on environment variables for core logic.
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
