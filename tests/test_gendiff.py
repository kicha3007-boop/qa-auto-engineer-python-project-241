import json
from pathlib import Path

import pytest

from gendiff import generate_diff

TEST_DATA = Path(__file__).parent / 'test_data'

# Пары входных файлов во всех форматах и их сочетаниях.
INPUT_PAIRS = [
    ('file1.json', 'file2.json'),
    ('file1.yml', 'file2.yaml'),
    ('file1.json', 'file2.yaml'),
]


def get_path(name):
    return TEST_DATA / name


def read_expected(name):
    return get_path(name).read_text(encoding='utf-8').rstrip('\n')


@pytest.mark.parametrize(('file1', 'file2'), INPUT_PAIRS)
@pytest.mark.parametrize(
    ('format_name', 'expected'),
    [('stylish', 'expected_stylish.txt'), ('plain', 'expected_plain.txt')],
)
def test_text_formats_match_expected_output(
    file1, file2, format_name, expected
):
    diff = generate_diff(get_path(file1), get_path(file2), format_name)
    assert diff == read_expected(expected)


@pytest.mark.parametrize(('file1', 'file2'), INPUT_PAIRS)
def test_json_format_is_valid_and_matches_expected(file1, file2):
    diff = generate_diff(get_path(file1), get_path(file2), 'json')
    assert json.loads(diff) == json.loads(read_expected('expected.json'))


def test_stylish_is_default_format():
    diff = generate_diff(get_path('file1.json'), get_path('file2.json'))
    assert diff == read_expected('expected_stylish.txt')


def test_identical_files_have_no_changes():
    path = get_path('identical.json')
    assert generate_diff(path, path) == read_expected(
        'expected_identical_stylish.txt'
    )
    assert generate_diff(path, path, 'plain') == ''


def test_relative_paths_are_resolved(monkeypatch):
    monkeypatch.chdir(TEST_DATA)
    diff = generate_diff('file1.json', 'file2.yaml')
    assert diff == read_expected('expected_stylish.txt')


def test_missing_file_raises_file_not_found():
    with pytest.raises(FileNotFoundError):
        generate_diff(get_path('missing.json'), get_path('file2.json'))


def test_unsupported_input_format_is_rejected():
    with pytest.raises(ValueError, match='Unsupported file format'):
        generate_diff(get_path('unsupported.txt'), get_path('file2.json'))


def test_unknown_output_format_is_rejected():
    with pytest.raises(ValueError, match='Unknown output format: xml'):
        generate_diff(get_path('file1.json'), get_path('file2.json'), 'xml')


@pytest.mark.parametrize('broken', ['broken.json', 'broken.yml', 'list.yml'])
def test_broken_data_is_rejected(broken):
    with pytest.raises(ValueError, match=f'Cannot parse {broken}'):
        generate_diff(get_path(broken), get_path('file2.json'))
