import os
import sys

from dotenv import load_dotenv

from config.paths import PROJECT_DIR

load_dotenv(
    dotenv_path=PROJECT_DIR / ".env.local",
)

BACKEND_URL = os.getenv("BACKEND_URL", "localhost:8000")
if "http://" in BACKEND_URL:
    BACKEND_URL = BACKEND_URL.replace("http://", "")
HOST, PORT = BACKEND_URL.split(":")


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if sys.argv[1] == "runserver":
        sys.argv[2:3] = [f"{HOST}:{PORT}"]

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
