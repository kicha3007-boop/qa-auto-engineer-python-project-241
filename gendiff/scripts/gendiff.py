import argparse
import sys

from gendiff import generate_diff


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.'
    )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument(
        '-f', '--format',
        default='stylish',
        help='set format of output (stylish, plain, json)',
    )
    args = parser.parse_args()
    try:
        diff = generate_diff(args.first_file, args.second_file, args.format)
    except (OSError, ValueError) as error:
        print(f'gendiff: {error}', file=sys.stderr)
        sys.exit(1)
    print(diff)


if __name__ == '__main__':
    main()
