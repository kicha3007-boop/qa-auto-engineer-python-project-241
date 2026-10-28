def build_node(key, data1, data2):
    if key not in data1:
        return {'key': key, 'type': 'added', 'value': data2[key]}
    if key not in data2:
        return {'key': key, 'type': 'removed', 'value': data1[key]}

    value1 = data1[key]
    value2 = data2[key]
    if isinstance(value1, dict) and isinstance(value2, dict):
        return {
            'key': key,
            'type': 'nested',
            'children': build_diff(value1, value2),
        }
    if value1 == value2:
        return {'key': key, 'type': 'unchanged', 'value': value1}
    return {
        'key': key,
        'type': 'changed',
        'value1': value1,
        'value2': value2,
    }


def build_diff(data1, data2):
    keys = sorted(data1.keys() | data2.keys())
    return [build_node(key, data1, data2) for key in keys]
