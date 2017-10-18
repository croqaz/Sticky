
import os
import sys
import pytest
sys.path.insert(1, os.getcwd())
from sticky import *


@pytest.fixture(scope='module', params=[
    ('import os\n\nprint("Aha")',
     '\n\n#- rev: 1 -\n#- hash: E/QCEY -\n\nimport os\n\nprint("Aha")'),
    ('#!/usr/bin/python\n\nimport os\n\nprint("Aha")\n',
     '#!/usr/bin/python\n\n#- rev: 1 -\n#- hash: ADVG5T -\n\nimport os\n\nprint("Aha")\n'),
    ('#! /usr/bin/python\n\nimport os\n\nprint("Aha")\n',
     '#! /usr/bin/python\n\n#- rev: 1 -\n#- hash: DJUYSX -\n\nimport os\n\nprint("Aha")\n'),
    ('#!/usr/bin/env python\n\nimport os\n\nprint("Aha")\n',
     '#!/usr/bin/env python\n\n#- rev: 1 -\n#- hash: LX+KQY -\n\nimport os\n\nprint("Aha")\n'),
    ('#!/usr/bin/python\n# coding: latin-1\n\nimport os\n\nprint("Aha")\n',
     '#!/usr/bin/python\n# coding: latin-1\n\n#- rev: 1 -\n#- hash: DVL9Q3 -\n\nimport os\n\nprint("Aha")\n'),
])
def test_pairs(request):
    """
    Fixture that yields pairs of input and expected values.
    """
    return request.param


def test_icky(test_pairs):
    txt = test_pairs[0]
    info = extract_text_info(txt)
    fin = inject_sticky_info(txt, info)
    assert fin == test_pairs[1]
