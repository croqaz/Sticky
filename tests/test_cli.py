
import os
import sys
import shutil
import tempfile
sys.path.insert(1, os.getcwd())
from sticky.cli import main


def test_cli():
    src = 'tests/fixtures/'
    with tempfile.TemporaryDirectory(prefix='sticky_') as tmp:
        dst = tmp + '/fixtures'
        shutil.copytree(src, dst)
        main(['-s', dst])
        assert open(dst + '/__init__.py').read() == ''
        assert '#- rev: v1 -\n#- hash: 4XWL6Y -' in open(dst + '/b.py').read()
        assert '#- rev: v1 -\n#- hash: 4XWL6Y -' in open(dst + '/c.py').read()
        assert '#- rev: v1 -\n#- hash: 4XWL6Y -' in open(dst + '/d.py').read()
