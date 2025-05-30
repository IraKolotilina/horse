import os
import re
from pydantic import ConfigDict

def update_pydantic_files(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.py'):
                filepath = os.path.join(subdir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                new_content = content

                # 1. Импорт ConfigDict, если есть BaseModel (и нет ещё ConfigDict)
                if ('from pydantic import BaseModel' in new_content and
                    'ConfigDict' not in new_content):
                    new_content = re.sub(
                        r'(from pydantic import BaseModel(?:, *[^\n]*)?)',
                        r'\1, ConfigDict',
                        new_content
                    )

                # 2. Замена class Config с orm_mode
                # Вырезать class Config с orm_mode = True, заменить на model_config = ConfigDict(from_attributes=True)
                new_content = re.sub(
                    r'\n\s*class Config:\s*\n\s*orm_mode\s*=\s*True',
                    '\n    model_config = ConfigDict(from_attributes=True)',
                    new_content
                )
                # Аналогично, если class Config без orm_mode — просто убрать class Config
                new_content = re.sub(
                    r'\n\s*class Config:\s*\n\s*pass',
                    '',
                    new_content
                )
                # Если есть просто orm_mode = True вне class Config, тоже заменяем
                new_content = re.sub(
                    r'\n\s*orm_mode\s*=\s*True',
                    '\n    model_config = ConfigDict(from_attributes=True)',
                    new_content
                )

                # 3. Замена импорта BaseSettings
                new_content = re.sub(
                    r'from pydantic_settings import BaseSettings',
                    'from pydantic_settings import BaseSettings',
                    new_content
                )

                # 4. Замена Config внутри BaseSettings на model_config (для settings.py)
                new_content = re.sub(
                    r'class Config:\s*\n\s*env_file\s*=\s*[\'"][^\'"]+[\'"]',
                    "model_config = ConfigDict(env_file='.env')",
                    new_content
                )

                if content != new_content:
                    print(f'Обновлено: {filepath}')
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == '__main__':
    update_pydantic_files('.')
    print('Замены завершены!')
