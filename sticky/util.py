"""
This module contains pure functions.
"""
#- rev: v1 -
#- hash: BUOUL+ -

import os
from hashlib import sha1
from inspect import stack as stacks
from binascii import b2a_base64 as base64
from .constant import MARKER_A, MARKER_Z, HASH_LEN


__all__ = ('locate_file', 'iter_files', 'hash_text', 'increment_rev',
           'is_hot_comment', 'split_py_source_file', 'extract_head_info')


def locate_file():
    """
    Search the upper stacks for the first Python file different
    than the current file.
    """
    for upper_stack in stacks()[1:]:
        fname = upper_stack.filename
        if fname != __file__ and fname[-3:] == '.py':
            return fname


def iter_files(source):
    # WARNING: Stickyfying a folder with photos, or documents
    # will DESTROY your photos and documents!!
    # Not a good idea to stickyfy other types of files
    exts = ['.py']

    if os.path.isfile(source):
        yield source
    elif os.path.isdir(source):
        for root, dirs, files in os.walk(source):
            for src in files:
                if os.path.splitext(src)[-1] not in exts:
                    continue
                fname = os.path.join(root, src)
                if not os.path.getsize(fname):
                    continue
                yield fname
            # Ignore known cache folders
            if '__pycache__' in dirs:
                dirs.remove('__pycache__')


def hash_text(text, hash_len=HASH_LEN):
    """
    Hash text and return the first characters.
    """
    sha = sha1(text.encode('utf')).digest()
    raw = base64(sha).decode('utf')
    return raw[:hash_len].upper()


def increment_rev(text):
    """
    Increment revision number.
    """
    if text[0].isalpha():
        rev = int(text[1:])
        return text[0] + str(rev + 1)
    else:
        return str(int(text) + 1)


def is_shebang_comment(line):
    return line.startswith('#!') and '/usr/bin/' in line


def is_encoding_comment(line):
    return line.startswith('#') and 'coding' in line


def is_hot_comment(line, marker_a=MARKER_A, marker_z=MARKER_Z):
    """
    Does this line contain a hot comment?
    """
    maybe = ':' in line and \
        line.startswith('#' + marker_a) and line.endswith(marker_z)
    return maybe and not is_shebang_comment(line) and \
        not is_encoding_comment(line)


def split_py_source_file(text):
    """
    Split Python source file in head and tail;
    The head ends where the actual Python code starts, with imports or defines;
    The tail is the rest of the text.
    """
    found = []
    comm = False
    for line in text.splitlines(True):
        if line.strip():
            if line.startswith('#'):
                found.append(line)
                continue
            if line.startswith('"""') or line.startswith("'''"):
                comm = not comm
                found.append(line)
                continue
            if not comm:
                break
        found.append(line)
    head = ''.join(found)
    return head, text[len(head):]


def extract_line_info(line, marker_a=MARKER_A, marker_z=MARKER_Z):
    """
    Extract the data from a line containing a hot comment.
    """
    a_len = len(marker_a) + 1
    b_len = 0 - len(marker_z)
    info = line[a_len:b_len].strip().split(':')
    key = info[0]
    val = ':'.join(i.strip() for i in info[1:])
    return {key: val}


def extract_head_info(head, marker_a=MARKER_A, marker_z=MARKER_Z):
    """
    Extract all relevant info from the hot comments of a Python source file.
    """
    info = {}
    text = []
    for line in head.rstrip().split('\n'):
        if is_hot_comment(line, marker_a, marker_z):
            info.update(extract_line_info(line, marker_a, marker_z))
        else:
            text.append(line)
    return '\n'.join(text), info
