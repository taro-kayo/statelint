"""Module allowing for ``python -m statelint ...``."""
from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
