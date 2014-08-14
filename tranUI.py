__author__ = 'PaleNeutron'
import os
import subprocess

for root, dirs, files in os.walk('.'):
    for file in files:
        path = root + os.sep + file
        if file.endswith('.ui'):
            subprocess.call(
                [r'C:\Python34\Scripts\pyside-uic.exe', path, '-o', os.path.splitext(path)[0] + '.py'])
        elif file.endswith('.qrc'):
            subprocess.call([r"C:\Python34\Lib\site-packages\PySide\pyside-rcc.exe", '-py3', path, '-o',
                             os.path.splitext(path)[0] + '_rc.py'])
