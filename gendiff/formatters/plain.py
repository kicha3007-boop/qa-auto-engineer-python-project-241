def to_str(value):
    if isinstance(value, dict | list):
        return '[complex value]'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if value is None:
        return 'null'
    if isinstance(value, str):
        return f"'{value}'"
    return str(value)


def format_node(node, path):
    property_path = f"{path}{node['key']}"
    match node['type']:
        case 'nested':
            return format_nodes(node['children'], f'{property_path}.')
        case 'added':
            return [
                f"Property '{property_path}' was added "
                f"with value: {to_str(node['value'])}"
            ]
        case 'removed':
            return [f"Property '{property_path}' was removed"]
        case 'changed':
            return [
                f"Property '{property_path}' was updated. "
                f"From {to_str(node['value1'])} to {to_str(node['value2'])}"
            ]
        case 'unchanged':
            return []


def format_nodes(nodes, path=''):
    return [line for node in nodes for line in format_node(node, path)]


def format_plain(tree):
    return '\n'.join(format_nodes(tree))
