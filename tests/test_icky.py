
import re
import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from sticky import *


def replace_hash(text):
    return re.sub('hash: .{6} ', 'hash: H ', text)


@pytest.fixture(scope='module', params=[
    ('# flake8: noqa\nfrom os import *\nprint("Aha")',
     '# flake8: noqa\n#- rev: v1 -\n#- hash: H -\n\nfrom os import *\nprint("Aha")'),
    ('import os\n\nprint("Aha")',
     '\n#- rev: v1 -\n#- hash: H -\n\nimport os\n\nprint("Aha")'),
    ('#!/usr/bin/python\n\nimport os\n\nprint("Aha")\n',
     '#!/usr/bin/python\n#- rev: v1 -\n#- hash: H -\n\nimport os\n\nprint("Aha")\n'),
    ('#! /usr/bin/python\n\nimport os\n\nprint("Aha")\n',
     '#! /usr/bin/python\n#- rev: v1 -\n#- hash: H -\n\nimport os\n\nprint("Aha")\n'),
    ('#!/usr/bin/env python\n\nimport os\n\nprint("Aha")\n',
     '#!/usr/bin/env python\n#- rev: v1 -\n#- hash: H -\n\nimport os\n\nprint("Aha")\n'),
    ('#!/usr/bin/python\n# coding: latin-1\n\nimport os\n\nprint("Aha")\n',
     '#!/usr/bin/python\n# coding: latin-1\n#- rev: v1 -\n#- hash: H -\n\nimport os\n\nprint("Aha")\n'),
    ('\n# -*- coding: ascii -*-\n\nimport os\n\nprint("Aha")\n',
     '\n# -*- coding: ascii -*-\n#- rev: v1 -\n#- hash: H -\n\nimport os\n\nprint("Aha")\n'),
    ('\n#- rev: 6 -\nimport os\n\nprint("Aha")',
     '\n#- rev: 7 -\n#- hash: H -\n\nimport os\n\nprint("Aha")'),
    ('\n#- rev: v8 -\n#- hash: H -\nimport os\n\nprint("Aha")',
     '\n#- rev: v9 -\n#- hash: H -\n\nimport os\n\nprint("Aha")'),
    ('\n# -*- coding: ascii -*-\n\n#- rev: r2 -\n#- hash: H -\nimport os\n\nprint("Aha")',
     '\n# -*- coding: ascii -*-\n#- rev: r3 -\n#- hash: H -\n\nimport os\n\nprint("Aha")'),
])
def test_pairs(request):
    """
    Fixture that yields pairs of input and expected values.
    """
    return request.param


def test_icky(test_pairs):
    src = Source(text=test_pairs[0])
    fin = src.inject_sticky_info()
    assert replace_hash(fin) == test_pairs[1]
