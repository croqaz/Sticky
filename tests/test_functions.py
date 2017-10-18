
import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from sticky import *


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
    assert len(h) == HASH_LENGTH
    h = hash_text('qwertyuiop ASDFGHJKL')
    assert h.isupper()
    assert len(h) == HASH_LENGTH


def test_is_hot_comment():
    assert is_hot_comment('#-ab: y-')
    assert is_hot_comment('#- ab: n -')
    assert not is_hot_comment('x')
    assert not is_hot_comment('#')
    assert not is_hot_comment('#-*- coding: ascii -*-')


def test_is_stop_line():
    assert is_stop_line('import sys')
    assert is_stop_line('from os import path')
    assert not is_stop_line('x')
    assert not is_stop_line('#')


def test_extract_info():
    txt = "#- rev: 1 -\n#- hash: QWE -\n\nimport sticky\nsticky.icky()\n\n#- rev: 2 -\n\nprint('Aha')\n"
    nfo = extract_text_info(txt)
    assert nfo == {'rev': '1', 'hash': 'QWE'}


def test_split_script():
    txt = "#- rev: 1 -\n#- hash: QWE -\n\nimport sticky\nsticky.icky()\n\n#- rev: 2 -\n\nprint('Aha')\n"
    head, tail = split_py_source_file(txt)
    assert head + tail == txt
    assert head.startswith('#- ')
    assert tail.startswith('import ')
