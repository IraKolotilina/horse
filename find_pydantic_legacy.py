import os
import re

DEPRECATED_PATTERNS = [
    # BaseSettings moved to pydantic_settings
    (r'from\s+pydantic\s+import\s+BaseSettings', 'BaseSettings импортируется из pydantic (требуется pydantic_settings)'),
    # orm_mode deprecated
    (r'orm_mode\s*=\s*True', "'orm_mode' устарел (используй 'from_attributes=True')"),
    # class Config: deprecated (часто указывали orm_mode здесь)
    (r'class\s+Config\s*:', "class Config: устарел (используй ConfigDict/from_attributes)"),
    # BaseModel import (не ошибка, но для заметки)
    (r'from\s+pydantic\s+import\s+BaseModel', 'BaseModel импортируется из pydantic (ok, если используешь v2)'),
    # validator старого синтаксиса
    (r'@validator', '@validator (убедись, что используешь pydantic.v1 compatible синтаксис или мигрируй на field_validator)'),
    # root_validator
    (r'@root_validator', '@root_validator (заменить на model_validator в v2)'),
    # Field(..., example=...)
    (r'example\s*=', 'Параметр example в Field устарел (используй examples в Schema)'),
]

def scan_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        for idx, line in enumerate(f, 1):
            for pattern, desc in DEPRECATED_PATTERNS:
                if re.search(pattern, line):
                    print(f"{filepath}:{idx}: {desc}")
                    print(f"    {line.strip()}")

def scan_dir(root='.'):
    for dirpath, dirs, files in os.walk(root):
        for file in files:
            if file.endswith('.py'):
                scan_file(os.path.join(dirpath, file))

if __name__ == "__main__":
    print('Ищу устаревшие конструкции Pydantic...')
    scan_dir('./app')
    scan_dir('./tests')
    print('Проверка завершена.')
