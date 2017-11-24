
import os
import sys
import shutil
import tempfile
sys.path.insert(1, os.getcwd())
from sticky.cli import main


def test_cli():
    src = 'tests/fixtures/'

    # One file
    main(['-s', src + '/__init__.py'])
    assert open(src + '/__init__.py').read() == ''

    # A folder
    with tempfile.TemporaryDirectory(prefix='sticky_') as tmp:
        dst = tmp + '/fixtures'
        shutil.copytree(src, dst)
        main(['-s', dst, '-i', '__*__.*'])
        assert open(dst + '/__init__.py').read() == ''
        assert open(dst + '/__version__.py').read() == '\nx = 1\ny = 2\n'
        assert '#- rev: v1 -\n#- hash: 4XWL6Y -' in open(dst + '/b.py').read()
        assert '#- rev: v1 -\n#- hash: 4XWL6Y -' in open(dst + '/c.py').read()
        assert '#- rev: v1 -\n#- hash: 4XWL6Y -' in open(dst + '/d.py').read()
