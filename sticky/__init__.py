
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
    info = {}
    for line in text.split(b'\n'):
        if is_hot_comment(line):
            info.update(extract_line_info(line))
    return info
