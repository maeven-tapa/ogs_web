"""Render build: collect assets and migrate only a configured persistent DB."""
import os
import subprocess
import sys

subprocess.run([sys.executable, "manage.py", "collectstatic", "--noinput"], check=True)
if os.environ.get("DATABASE_URL"):
    subprocess.run([sys.executable, "manage.py", "migrate", "--noinput"], check=True)
