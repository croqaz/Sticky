
import re
import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from sticky import *


def replace_hash(text):
    return re.sub('hash: .{6} ', 'hash: H ', text)

def strip_head(text):
    return re.sub('#< rev: .+ >', '', text.replace('#< hash: H >', ''))


@pytest.fixture(scope='module', params=[
    ('# flake8: noqa\nfrom os import *\nprint("Aha")',
     '# flake8: noqa\n#< rev: v1 >\n#< hash: H >\n\nfrom os import *\nprint("Aha")'),
    ('import os\n\nprint("Aha")',
     '\n#< rev: v1 >\n#< hash: H >\n\nimport os\n\nprint("Aha")'),
    ('#!/usr/bin/python\n\nimport os\n\nprint("Aha")\n',
     '#!/usr/bin/python\n#< rev: v1 >\n#< hash: H >\n\nimport os\n\nprint("Aha")\n'),
    ('#! /usr/bin/python\n\nimport os\n\nprint("Aha")\n',
     '#! /usr/bin/python\n#< rev: v1 >\n#< hash: H >\n\nimport os\n\nprint("Aha")\n'),
    ('#!/usr/bin/env python\n\nimport os\n\nprint("Aha")\n',
     '#!/usr/bin/env python\n#< rev: v1 >\n#< hash: H >\n\nimport os\n\nprint("Aha")\n'),
    ('\n# -*- coding: ascii -*-\n\nimport os\n\n',
     '\n# -*- coding: ascii -*-\n#< rev: v1 >\n#< hash: H >\n\nimport os\n\n'),
    ('\n#< rev: 6 >\nimport os\n\nprint("Aha")',
     '\n#< rev: 7 >\n#< hash: H >\n\nimport os\n\nprint("Aha")'),
    ('\n#< rev: v8 >\n#< hash: H >\nimport os\n\nprint("Aha")',
     '\n#< rev: v9 >\n#< hash: H >\n\nimport os\n\nprint("Aha")'),
    ('\n# -*- coding: ascii -*-\n\n#< rev: r2 >\n#< hash: H >\nimport os\n\n#',
     '\n# -*- coding: ascii -*-\n#< rev: r3 >\n#< hash: H >\n\nimport os\n\n#'),
])
def test_pairs(request):
    """
    Fixture that yields pairs of input and expected values.
    """
    return request.param


def test_crash():
    with pytest.raises(Exception):
        src = Source(text='', fname=None)


def test_inject(test_pairs):
    # Default tmpl
    src = Source(text=test_pairs[0], marker_a='<', marker_z='>')
    fin = src.inject_sticky_info()
    assert replace_hash(fin) == test_pairs[1]
    # Without template, default markers
    src = Source(text=test_pairs[0], marker_a='<', marker_z='>', head_tmpl='\n')
    fin = src.inject_sticky_info()
    assert fin.replace('\n', '') == strip_head(test_pairs[0]).replace('\n', '')


def test_save_header():
    """
    Run save header a few times to see that the revision is stable
    """
    fname = 'tests/fixtures/deep/a.py'
    initial_text = open('tests/fixtures/deep/a.py').read()
    src = Source(fname)
    assert src.head == '#!/usr/bin/python\n\n' and 'Trap' in src.tail
    src.save_header()
    after_text = open('tests/fixtures/deep/a.py').read()
    Source(fname).save_header()
    assert open('tests/fixtures/deep/a.py').read() == after_text
    Source(fname).save_header()
    assert open('tests/fixtures/deep/a.py').read() == after_text
    # Restore
    open('tests/fixtures/deep/a.py', 'w').write(initial_text)


@pytest.fixture(scope='module', params=[
    'tests/fixtures/b.py',
    'tests/fixtures/c.py',
    'tests/fixtures/d.py',
])
def test_file(request):
    """
    Fixture that files to be tested.
    """
    return request.param


def test_sources(test_file):
    """
    All fixture files have the same body, only the header is different
    """
    src = Source(test_file, marker_a='<<', marker_z='>>')
    assert src.head.startswith('#!') and src.head.endswith('\n\n')
    assert src.tail.startswith('import os')
    fin = src.inject_sticky_info()
    assert '#<< hash: 4XWL6Y >>\n' in fin
