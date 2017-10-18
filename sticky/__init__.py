
import re
from hashlib import sha1
from inspect import stack as stacks
from binascii import b2a_base64 as base64

HASH_LENGTH = 6
ICKY_MARKER_START = '-'
ICKY_MARKER_FINIS = '-'

MATCHER = re.compile('^([\s\S]+?)(?:from \w|import \w|class \w|def \w)')


def locate_file():
    """
    Search the upper stacks for the first Python file different
    than the current file.
    """
    for upper_stack in stacks()[1:]:
        fname = upper_stack.filename
        if fname != __file__ and fname[-3:] == '.py':
            return fname


def hash_text(text):
    """
    Hash text and return the first characters.
    """
    sha = sha1(text.encode('utf')).digest()
    raw = base64(sha).decode('utf')
    return raw[:HASH_LENGTH].upper()


def increment_rev(text):
    """
    Increment revision number.
    """
    if text[0].isalpha():
        rev = int(text[1:])
    else:
        rev = int(text)
    return rev + 1


def is_shebang_comment(line):
    return line.startswith('#!') and '/usr/bin/' in line


def is_encoding_comment(line):
    return line.startswith('#') and 'coding' in line


def is_hot_comment(line):
    """
    Does this line contain a hot comment?
    """
    maybe = ':' in line and \
        line.endswith(ICKY_MARKER_FINIS) and \
        line.startswith('#' + ICKY_MARKER_START)
    return maybe and not is_shebang_comment(line) and \
        not is_encoding_comment(line)


def is_stop_line(line):
    """
    Does this line contain an import, a class, or a function definition?
    """
    if line.startswith('from '):
        return True
    if line.startswith('import '):
        return True
    if line.startswith('class '):
        return True
    if line.startswith('def '):
        return True
    return False


def extract_line_info(line):
    """
    Extract the data from a line containing a hot comment.
    """
    a_len = len(ICKY_MARKER_START) + 1
    b_len = 0 - len(ICKY_MARKER_FINIS)
    info = line[a_len:b_len].strip().split(':')
    key = info[0]
    val = ':'.join(i.strip() for i in info[1:])
    return {key: val}


def extract_text_info(text):
    """
    Extract all relevant info from the hot comments of a Python source file.
    """
    info = {}
    for line in text.split('\n'):
        if is_hot_comment(line):
            info.update(extract_line_info(line))
        elif is_stop_line(line):
            break
    return info


def split_py_source_file(text):
    """
    Split Python source file in head and tail;
    The head ends where the actual Python code starts, with imports or defines;
    The tail is the rest of the text.
    """
    match = re.match(MATCHER, text)
    if not match:
        return '', text
    found = match.groups()[0]
    return text[:len(found)], text[len(found):]


def inject_sticky_info(text, old):
    """
    Merge text with the info and write the result in output file.
    """
    head, tail = split_py_source_file(text)
    hash = hash_text(text)
    if hash != old.get('hash'):
        rev = increment_rev(old.get('rev', 'v0'))
    info = {
        'rev': rev,
        'hash': hash,
        'start': ICKY_MARKER_START,
        'finis': ICKY_MARKER_FINIS,
    }
    icky = '\n\n#{start} rev: {rev} {finis}\n' \
           '#{start} hash: {hash} {finis}\n\n'.format(**info)
    return head.rstrip() + icky + tail
