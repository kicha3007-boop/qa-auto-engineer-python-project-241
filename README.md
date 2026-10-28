# Вычислитель отличий (QA Python)

[![hexlet-check](https://github.com/kicha3007-boop/qa-auto-engineer-python-project-241/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/kicha3007-boop/qa-auto-engineer-python-project-241/actions)
[![CI](https://github.com/kicha3007-boop/qa-auto-engineer-python-project-241/actions/workflows/pyci.yml/badge.svg)](https://github.com/kicha3007-boop/qa-auto-engineer-python-project-241/actions/workflows/pyci.yml)

`gendiff` — утилита и библиотека: сравнивает два файла JSON или YAML с парами «ключ — значение» и показывает
разницу в формате stylish, plain или json. Главное в проекте — тесты на pytest с эталонными файлами и порогом
покрытия, при просадке которого падает сборка.

## Установка

Нужен [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/kicha3007-boop/qa-auto-engineer-python-project-241.git
cd qa-auto-engineer-python-project-241
make install          # зависимости
make test             # тесты
make test-coverage    # тесты с порогом покрытия 90%
make lint             # ruff
make build package-install   # команда gendiff в системе
```

## Использование

```bash
gendiff -h
usage: gendiff [-h] [-f FORMAT] first_file second_file

gendiff tests/test_data/file1.json tests/test_data/file2.yaml
{
  - follow: false
    host: hexlet.io
  - proxy: 123.234.53.22
  - timeout: 50
  + timeout: 20
  + verbose: true
}

gendiff -f plain tests/test_data/file1.json tests/test_data/file2.json
Property 'follow' was removed
Property 'proxy' was removed
Property 'timeout' was updated. From 50 to 20
Property 'verbose' was added with value: true

gendiff -f json tests/test_data/file1.json tests/test_data/file2.json   # дерево различий в JSON
```

Формат входного файла определяется по расширению (`.json`, `.yml`, `.yaml`), пути — относительные или абсолютные.
Ошибки (нет файла, неизвестный формат, битые данные) — сообщение в stderr и код выхода `1`.

```python
from gendiff import generate_diff

diff = generate_diff('file1.json', 'file2.yml', 'plain')
```

## Тесты

`tests/test_gendiff.py` проверяет публичную функцию `generate_diff`:

- все форматы вывода и все сочетания входных форматов — параметризацией, с эталонами в `tests/test_data/`;
- формат по умолчанию, одинаковые файлы, относительные пути;
- негативные сценарии: нет файла, неподдерживаемое расширение, неизвестный формат вывода, битые JSON и YAML,
  YAML без пар «ключ — значение».
