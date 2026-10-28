from gendiff.formatters.json import format_json
from gendiff.formatters.plain import format_plain
from gendiff.formatters.stylish import format_stylish

FORMATTERS = {
    'stylish': format_stylish,
    'plain': format_plain,
    'json': format_json,
}


def format_diff(tree, format_name):
    formatter = FORMATTERS.get(format_name)
    if formatter is None:
        raise ValueError(f'Unknown output format: {format_name}')
    return formatter(tree)
