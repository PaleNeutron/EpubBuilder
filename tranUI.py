__author__ = 'PaleNeutron'
import os
import subprocess
import importlib
import sys
# from distutils.sysconfig import get_python_lib
PySide_path = os.path.dirname(importlib.find_loader("PySide").path)
uic_path = sys.exec_prefix + os.sep + "bin" + os.sep + "pyside-uic"
rcc_path = PySide_path + os.sep + "pyside-rcc"

for root, dirs, files in os.walk('.'):
    for file in files:
        path = root + os.sep + file
        path = os.path.abspath(path)
        if file.endswith('.ui'):
            subprocess.call(
                [uic_path, path, '-o', os.path.splitext(path)[0] + '.py'])
            print(os.path.splitext(path)[0] + '.py', "created")
        elif file.endswith('.qrc'):
            subprocess.call([rcc_path, path, '-o',
                             os.path.splitext(path)[0] + '_rc.py'])
            print(os.path.splitext(path)[0] + '_rc.py', "created")
