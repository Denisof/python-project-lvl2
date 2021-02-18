# -*- coding:utf-8 -*-

"""Gen diff entry point."""

import argparse

from gendiff.module.differ import generate_diff


def main():
    """Run entry function."""
    parser = argparse.ArgumentParser(
        prog='gendiff',
         description='Generate diff.'
         )
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument( 
        '-f',
         '--format',
          metavar='FORMAT',
           help='set format of output'
    )
    args = parser.parse_args()
    difference = generate_diff(args.first_file, args.second_file)
    print(difference)

if __name__ == '__main__':
    main()
