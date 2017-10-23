
import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from sticky import *
from sticky.constant import HASH_LEN
from sticky.util import is_shebang_comment, is_encoding_comment, extract_line_info


def test_locate_file():
    fname = '/test_functions.py'
    assert locate_file().endswith(fname)
    def wrap1():
        return locate_file()
    assert wrap1().endswith(fname)
    def wrap2():
        return wrap1()
    assert wrap2().endswith(fname)


def test_iter_files():
    dir = 'sticky'
    assert list(iter_files(dir + '/__init__.py')) == [dir + '/__init__.py']
    assert set(iter_files(dir)) == \
        set(dir + '/' + f for f in os.listdir(dir) if f != '__pycache__')


def test_hash_text():
    h = hash_text('a')
    assert h.isupper()
    assert len(h) == HASH_LEN
    h = hash_text('qwertyuiop ASDFGHJKL')
    assert h.isupper()
    assert len(h) == HASH_LEN
    h = hash_text('a', 12)
    assert len(h) == 12


def test_increment_rev():
    assert increment_rev('1') == '2'
    assert increment_rev('r2') == 'r3'
    assert increment_rev('v3') == 'v4'


def test_boring_comments():
    assert is_shebang_comment('#!/usr/bin/python')
    assert is_shebang_comment('#! /usr/bin/python')
    assert is_shebang_comment('#!/usr/bin/env python')
    assert is_encoding_comment('# coding: latin-1')
    assert is_encoding_comment('# -*- coding: ascii -*-')
    assert is_encoding_comment('# vim: set fileencoding=latin-1 :')


def test_is_hot_comment():
    assert is_hot_comment('#!ab: y!', '!', '!')
    assert is_hot_comment('#<< ab: n >>', '<<', '>>')
    assert not is_hot_comment('x')
    assert not is_hot_comment('#')
    assert not is_hot_comment('#-*- coding: ascii -*-')


def test_extract_line_info():
    assert extract_line_info('#!rev: 1!', '!', '!') == {'rev': '1'}
    assert extract_line_info('#<<  rev: 1  >>', '<<', '>>') == {'rev': '1'}


def test_extract_info():
    txt = "#- rev: 1 -\n#- hash: QWE -\n\n"
    hd, nfo = extract_head_info(txt)
    assert hd == ''
    assert nfo == {'rev': '1', 'hash': 'QWE'}


def test_split_script():
    # Normal
    txt = "#- rev: 1 -\n#- hash: QWE -\n\nimport os\n"
    head, tail = split_py_source_file(txt)
    assert head + tail == txt
    assert head.startswith('#- ')
    assert tail.startswith('import ')
    # Comments and stuff
    txt = '"""\nComment\n"""\n\nimport os'
    head, tail = split_py_source_file(txt)
    assert head + tail == txt
    assert head == '"""\nComment\n"""\n\n'
    assert tail == 'import os'
    # Only variables
    txt = 'x = 1'
    head, tail = split_py_source_file(txt)
    assert head + tail == txt
    assert head == ''
    assert tail == 'x = 1'
