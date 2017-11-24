
#- rev: v1 -
#- hash: 94IARZ -

import argparse
from .source import Source
from .util import iter_files


def main(args=None):
    """
    Add sticky headers to all source files from the specified folder.

    *DANGER*: Adding headers to files like: photos, or documents
        will DESTROY the photos, or documents!!

    To prevent this, 2 types of checks are made:
        * the extension of the file must be ".py" (this is a fast check)
        * the file is compiled to see if it has a valid syntax (slow check)
    """
    parser = argparse.ArgumentParser('sticky', description='Add headers to source files.')
    parser.add_argument('-s', '--source', help='A folder with source files', required=True)
    parser.add_argument('-i', '--ignore', help='A list of patterns of files to ignore')
    argv = parser.parse_args(args)
    ignore_list = argv.ignore.split(',') if argv.ignore else []
    for src in iter_files(argv.source, ignore_list):
        Source(src).save_header()


if __name__ == '__main__':
    main()
