
#- rev: v1 -
#- hash: 94IARZ -

import argparse
from .source import Source
from .util import iter_files


def main(args=None):
    parser = argparse.ArgumentParser('sticky', description='Add headers to source files.')
    parser.add_argument('-s', '--source', help='A folder with source files', required=True)
    argv = parser.parse_args(args)
    for src in iter_files(argv.source):
        # print('Stickyfy ::', src)
        Source(src).save_header()


if __name__ == '__main__':
    main()
