#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from config.paths import PROJECT_DIR
from dotenv import load_dotenv


load_dotenv(
    dotenv_path=PROJECT_DIR / ".env.local",
)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    if sys.argv[1] == 'runserver':
        backend_url = os.getenv('BACKEND_URL', 'localhost:8000')
        if 'http://' in backend_url:
            backend_url = backend_url.replace('http://', '')
        host, port = backend_url.split(':')
        sys.argv[2:3] = [f"{host}:{port}"]

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
