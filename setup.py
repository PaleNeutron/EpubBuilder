from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(packages = ["lxml._elementpath"], excludes = [],
                    include_files=['LICENSE','libEGL.dll'])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None
# base = 'Console'
executables = [
    Executable('BuilderUI.py', base=base, targetName = 'Builder.exe',
               icon="Builder.ico",
               compress=True)
]

setup(name='EpubBuilder',
      version = '1.1',
      description = 'a tool to build epub from txt file',
      options = dict(build_exe = buildOptions),
      executables = executables)
