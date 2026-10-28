from pathlib import Path

from gendiff.diff_tree import build_diff
from gendiff.formatters import format_diff
from gendiff.parser import parse

DATA_FORMATS = {
    '.json': 'json',
    '.yml': 'yaml',
    '.yaml': 'yaml',
}


def get_data(file_path):
    path = Path(file_path).resolve()
    data_format = DATA_FORMATS.get(path.suffix.lower())
    if data_format is None:
        raise ValueError(f'Unsupported file format: {path.name}')
    with path.open(encoding='utf-8') as file:
        return parse(file.read(), data_format, path.name)


def generate_diff(file_path1, file_path2, format_name='stylish'):
    tree = build_diff(get_data(file_path1), get_data(file_path2))
    return format_diff(tree, format_name)
