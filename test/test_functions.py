
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
    h = hash_text(b'a')
    assert h.isupper()
    assert len(h) == HASH_LENGTH
    h = hash_text(b'qwertyuiop ASDFGHJKL')
    assert h.isupper()
    assert len(h) == HASH_LENGTH


def test_is_hot_comment():
    assert is_hot_comment(b'#-ab: y-')
    assert is_hot_comment(b'#- ab: n -')
    assert not is_hot_comment(b'x')
    assert not is_hot_comment(b'#')
    assert not is_hot_comment(b'#-*- coding: ascii -*-')


def test_is_stop_line():
    assert is_stop_line(b'import sys')
    assert is_stop_line(b'from os import path')
    assert not is_stop_line(b'x')
    assert not is_stop_line(b'#')


def test_extract_info():
    txt = b"#- rev: 1 -\n#- hash: QWE -\n\nimport sticky\nsticky.icky()\n\n#- rev: 2 -\n\nprint('Aha')\n"
    nfo = extract_text_info(txt)
    assert nfo == {b'rev': b'1', b'hash': b'QWE'}


def test_split_script():
    txt = b"#- rev: 1 -\n#- hash: QWE -\n\nimport sticky\nsticky.icky()\n\n#- rev: 2 -\n\nprint('Aha')\n"
    head, tail = split_py_source_file(txt)
    assert head + tail == txt
    assert head.startswith(b'#- ')
    assert tail.startswith(b'import ')


# def test_icky():
#     txt = b'#!/usr/bin/python\n\nimport os\n\nprint("Aha")\n'
#     info = extract_text_info(txt)
#     fin = inject_sticky_info(txt, info)
