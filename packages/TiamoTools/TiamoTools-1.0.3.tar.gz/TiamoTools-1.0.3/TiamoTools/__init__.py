import os
import sys
import platform


__version__ = '1.0.3'
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

if platform.system() == 'Windows':
    __all__ = ['dtime', 'log', 'mongo', 'mysql', 'oracle']
else:
    __all__ = ['dtime', 'log', 'mongo', 'mysql', 'oracle', 'xugu']
