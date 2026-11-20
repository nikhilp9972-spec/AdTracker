"""
Configuration module for AdPulse Intelligence.
Loads settings from environment variables and local .env files.
Specially configured for EdTech Competitor Advertising Intelligence.
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "ad_tracker.db"
FRONTEND_DIR = BASE_DIR / "frontend"

def load_env_file():
    """Lightweight .env loader that doesn't require third-party dependencies."""
    env_path = BASE_DIR / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key not in os.environ:
                        os.environ[key] = val

load_env_file()

# Application Branding
APP_NAME = os.environ.get("APP_NAME", "AdPulse Intelligence")
APP_SUBTITLE = os.environ.get("APP_SUBTITLE", "EdTech Competitive Marketing Intelligence")
INDUSTRY = "EdTech"

# Server Settings
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "8000"))

# Scheduler & Automation Settings
# Default: Every Monday at 09:00 AM
SCHEDULE_DAY = os.environ.get("SCHEDULE_DAY", "monday").lower()
SCHEDULE_HOUR = int(os.environ.get("SCHEDULE_HOUR", "9"))
SCHEDULE_MINUTE = int(os.environ.get("SCHEDULE_MINUTE", "0"))
SCHEDULE_ENABLED = os.environ.get("SCHEDULE_ENABLED", "true").lower() == "true"
TIMEZONE = os.environ.get("TIMEZONE", "Asia/Kolkata")

# Slack Configuration
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")

# Email / SMTP Configuration
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")
SMTP_FROM = os.environ.get("SMTP_FROM", "adpulse-intelligence@company.com")
EMAIL_RECIPIENTS = [email.strip() for email in os.environ.get("EMAIL_RECIPIENTS", "").split(",") if email.strip()]

# AI Provider Configuration (Optional OpenAI or Gemini)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
AI_PROVIDER = os.environ.get("AI_PROVIDER", "auto") # auto | openai | gemini | local

# Meta Ad Library API Configuration
META_ACCESS_TOKEN = os.environ.get("META_ACCESS_TOKEN", "")

# Google Ads Transparency API / Credentials (Optional)
GOOGLE_ADS_API_KEY = os.environ.get("GOOGLE_ADS_API_KEY", "")
GOOGLE_CUSTOMER_ID = os.environ.get("GOOGLE_CUSTOMER_ID", "")
