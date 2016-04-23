__author__ = 'PaleNeutron'
import os
import subprocess
import importlib.util
import sys
# from distutils.sysconfig import get_python_lib
PyQt_path = os.path.dirname(importlib.util.find_spec("PyQt5").origin)
# uic_path = sys.exec_prefix + os.sep + "bin" + os.sep + "pyuic5"
uic_path = PyQt_path + os.sep + "pyuic5.bat"
rcc_path = PyQt_path + os.sep + "pyrcc5.exe"

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
