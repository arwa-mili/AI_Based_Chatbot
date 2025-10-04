import os
import sys
from pathlib import Path
from decouple import Config, RepositoryEnv


def main():
    BASE_DIR = Path(__file__).resolve().parent
    
    env_file = BASE_DIR / "config" / "settings" / ".env"
    config = Config(RepositoryEnv(env_file))
    
    ENV = config("ENV", default="dev")
    
    print(f"Using {ENV} settings...")

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{ENV}")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
