
import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from sticky import *
from sticky.constant import HASH_LEN


def test_locate_file():
    fname = '/test_functions.py'
    assert locate_file().endswith(fname)
    def wrap1():
        return locate_file()
    assert wrap1().endswith(fname)
    def wrap2():
        return wrap1()
    assert wrap2().endswith(fname)


def test_hash_text():
    h = hash_text('a')
    assert h.isupper()
    assert len(h) == HASH_LEN
    h = hash_text('qwertyuiop ASDFGHJKL')
    assert h.isupper()
    assert len(h) == HASH_LEN


def test_increment_rev():
    assert increment_rev('1') == '2'
    assert increment_rev('r2') == 'r3'
    assert increment_rev('v3') == 'v4'


def test_is_hot_comment():
    assert is_hot_comment('#-ab: y-')
    assert is_hot_comment('#- ab: n -')
    assert not is_hot_comment('x')
    assert not is_hot_comment('#')
    assert not is_hot_comment('#-*- coding: ascii -*-')


def test_extract_info():
    txt = "#- rev: 1 -\n#- hash: QWE -\n\n"
    hd, nfo = extract_head_info(txt)
    assert hd == ''
    assert nfo == {'rev': '1', 'hash': 'QWE'}


def test_split_script():
    txt = "#- rev: 1 -\n#- hash: QWE -\n\nimport sticky\nsticky.icky()\n\n#- rev: 2 -\n\nprint('Aha')\n"
    head, tail = split_py_source_file(txt)
    assert head + tail == txt
    assert head.startswith('#- ')
    assert tail.startswith('import ')
