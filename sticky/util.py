"""
This module contains pure functions, dealing with cycling files,
analyzing and building "sticky" headers.
"""
#- rev: v3 -
#- hash: 8YBSJ2 -

import os
from hashlib import sha1
from binascii import b2a_base64 as base64
from .constant import MARKER_A, MARKER_Z, HASH_LEN


__all__ = ('iter_files', 'hash_text', 'increment_rev',
           'split_py_source_file', 'build_head_info')


def is_python_file(fname):
    """
    Check if a specific file is a valid Python source file.
    """
    with open(fname, 'r') as fd:
        try:
            compile(fd.read(), fname, 'exec')
            return True
        except Exception:
            return False


def iter_files(source):
    """
    Lazy iterate a folder in depth and return
    the paths of all Python source files.

    *DANGER*: Adding "sticky" headers to files like: photos, or documents
    will DESTROY the photos and documents!!
    To prevent this, 2 types of checks are made:
    * the extension of the file must be ".py" (this is a fast check)
    * the file is compiled to see if it has a valid sintax (slow check)
    """
    exts = ['.py']

    if os.path.isfile(source):
        yield source
    elif os.path.isdir(source):
        for root, dirs, files in os.walk(source):
            for src in files:
                # Ignore all unknown extensions
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
    Hash text using SHA1 and clip to the desired length.
    """
    sha = sha1(text.encode('utf')).digest()
    raw = base64(sha).decode('utf')
    return raw[:hash_len].upper()


def increment_rev(text):
    """
    Increment revision number.
    The revision consists of 1 caracter followed by numbers,
    or just numbers.

    Examples:
        increment_rev("v1") # v2
        increment_rev("r2") # r3
        increment_rev("9")  # 10
    """
    if text[0].isalpha():
        rev = int(text[1:])
        return text[0] + str(rev + 1)
    else:
        return str(int(text) + 1)


def is_shebang_comment(line):
    """
    Return True if the line is a shebang.
    """
    return line.startswith('#!') and '/usr/bin/' in line


def is_encoding_comment(line):
    """
    Return True if the line declares the encoding of a file.
    """
    return line.startswith('#') and 'coding' in line


def is_hot_comment(line, marker_a=MARKER_A, marker_z=MARKER_Z):
    """
    Return True if the line contains a "hot" comment.
    A "hot" comment is in the form:
        #- key: value -
    For example:
        #- hash: JHSNSV -
    """
    maybe = ':' in line and \
        line.startswith('#' + marker_a) and line.endswith(marker_z)
    return maybe and not is_shebang_comment(line) and \
        not is_encoding_comment(line)


def split_py_source_file(text):
    """
    Split a Python source file into head and tail;
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
    Extract the data from a line containing a "hot" comment.
    The key and value are exploded and returned a dict.
    """
    a_len = len(marker_a) + 1
    b_len = 0 - len(marker_z)
    info = line[a_len:b_len].strip().split(':')
    key = info[0]
    val = ':'.join(i.strip() for i in info[1:])
    return {key: val}


def build_head_info(head, marker_a=MARKER_A, marker_z=MARKER_Z):
    """
    Extract all relevant info from all the hot comments of a Python source file.
    """
    info = {}
    text = []
    for line in head.rstrip().split('\n'):
        if is_hot_comment(line, marker_a, marker_z):
            info.update(extract_line_info(line, marker_a, marker_z))
        else:
            text.append(line)
    return '\n'.join(text), info
