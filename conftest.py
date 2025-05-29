# conftest.py
import sys
from pathlib import Path

# Добавляем корень проекта в системный путь, чтобы "import app" работал
root = Path(__file__).parent.resolve()
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
