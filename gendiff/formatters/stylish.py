INDENT_SIZE = 4
MARKER_WIDTH = 2
MARKERS = {
    'added': '+ ',
    'removed': '- ',
    'unchanged': '  ',
    'nested': '  ',
}


def get_indent(depth, shift=0):
    return ' ' * (depth * INDENT_SIZE - shift)


def to_str(value, depth):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if value is None:
        return 'null'
    if not isinstance(value, dict):
        return str(value)

    lines = [
        f'{get_indent(depth + 1)}{key}: {to_str(item, depth + 1)}'
        for key, item in value.items()
    ]
    return '\n'.join(['{', *lines, f'{get_indent(depth)}}}'])


def make_line(depth, marker, key, value):
    indent = get_indent(depth, MARKER_WIDTH)
    return f'{indent}{marker}{key}: {value}'


def format_node(node, depth):
    key = node['key']
    match node['type']:
        case 'nested':
            children = format_nodes(node['children'], depth)
            return [make_line(depth, MARKERS['nested'], key, children)]
        case 'changed':
            return [
                make_line(depth, MARKERS['removed'], key,
                          to_str(node['value1'], depth)),
                make_line(depth, MARKERS['added'], key,
                          to_str(node['value2'], depth)),
            ]
        case node_type:
            value = to_str(node['value'], depth)
            return [make_line(depth, MARKERS[node_type], key, value)]


def format_nodes(nodes, depth):
    lines = [line for node in nodes for line in format_node(node, depth + 1)]
    return '\n'.join(['{', *lines, f'{get_indent(depth)}}}'])


def format_stylish(tree):
    return format_nodes(tree, 0)
