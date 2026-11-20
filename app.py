"""
Competitor Ad Tracker - Root Application Launcher.
Run with: python app.py
"""

import sys
from pathlib import Path

# Force unbuffered output so logs print immediately on Windows
try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from backend.server import start_server

if __name__ == "__main__":
    start_server()
