#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.
Used for running the dev server, migrations, and management commands.
"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Could not import Django. Are you sure it is installed and "
            "available in your virtual environment or Docker container?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
