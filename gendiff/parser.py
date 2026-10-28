import json

import yaml

PARSERS = {
    'json': json.loads,
    'yaml': yaml.safe_load,
}


def parse(content, data_format, source='data'):
    """Разбирает содержимое в словарь; битые данные — ValueError."""
    try:
        data = PARSERS[data_format](content)
    except (json.JSONDecodeError, yaml.YAMLError) as error:
        raise ValueError(f'Cannot parse {source}: {error}') from error
    if not isinstance(data, dict):
        raise ValueError(f'Cannot parse {source}: expected key-value pairs')
    return data
