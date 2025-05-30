import os
import re

ROOT = '.'  # Корень вашего проекта

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Если в файле есть "ConfigDict(" и нет уже импорта
    if any('ConfigDict(' in line for line in lines):
        has_import = any('from pydantic import ConfigDict' in line for line in lines)
        if not has_import:
            # Найдём место после первых импортов
            insert_at = 0
            for i, line in enumerate(lines):
                if line.strip().startswith('import') or line.strip().startswith('from'):
                    insert_at = i + 1

            # Вставим импорт после всех других импортов
            lines.insert(insert_at, 'from pydantic import ConfigDict\n')

            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            print(f'Импорт добавлен в {filepath}')

def walk_py_files(root):
    for dirpath, _, filenames in os.walk(root):
        for fname in filenames:
            if fname.endswith('.py'):
                process_file(os.path.join(dirpath, fname))

if __name__ == '__main__':
    walk_py_files(ROOT)
    print('Готово!')
