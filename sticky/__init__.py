
import re
from hashlib import sha1
from inspect import stack as stacks
from binascii import b2a_base64 as base64

HASH_LENGTH = 6
ICKY_MARKER = b'-'


def locate_file():
    """
    Search the upper stacks for the first Python file different then the current file.
    """
    for upper_stack in stacks()[1:]:
        fname = upper_stack.filename
        if fname != __file__ and fname[-3:] == '.py':
            return fname


def hash_text(text):
    """
    Hash text and return the first characters.
    """
    raw = base64(sha1(text).digest())
    return raw[:HASH_LENGTH].upper()


def is_hot_comment(line):
    """
    Does this line contain a hot comment?
    """
    return line.startswith(b'#' + ICKY_MARKER)


def is_stop_line(line):
    """
    Does this line contain an import, a class, or a function definition?
    """
    if line.startswith(b'from '):
        return True
    if line.startswith(b'import '):
        return True
    if line.startswith(b'class '):
        return True
    if line.startswith(b'def '):
        return True
    return False


def extract_line_info(line):
    """
    Extract the data from a line containing a hot comment.
    """
    comm_len = len(ICKY_MARKER) + 1
    info = line[comm_len:].strip().split(b':')
    key = info[0]
    val = b':'.join(i.strip() for i in info[1:])
    return {key: val}


def extract_text_info(text):
    """
    Extract all relevant info from the hot comments of a Python source file.
    """
    info = {}
    for line in text.split(b'\n'):
        if is_hot_comment(line):
            info.update(extract_line_info(line))
        elif is_stop_line(line):
            break
    return info


def inject_sticky_info(text, info):
    pass
