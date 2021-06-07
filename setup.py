#!/usr/bin/python3
# -*- coding: utf-8 -*-

'''
Created by Anoniji
Library made available under the terms of the license
Attribution-NonCommercial-NoDerivs 3.0 Unported (CC BY-NC-ND 3.0)
https://creativecommons.org/licenses/by-nc-nd/3.0/
'''

import sys
import shutil
import os
from cx_Freeze import setup, Executable

LIBS_PATH = './beep'
version = '1'
sys.path.insert(0, LIBS_PATH)

def copy(source, out):
    if os.path.exists(out):
        shutil.rmtree(out)
    shutil.copytree(source, out)

cible = Executable(script='main.py', base='Console', targetName="tc28bs.exe")

setup(
    name='tc28bs',
    version=version,
    author='Anoniji',
    options={
        'build_exe': {
            'path': sys.path,
            'includes': [],
            'excludes': [],
            'packages': [
                'beep',
                'beep.elements.oscillator',
                'beep.elements.compressor',
                'beep.elements.sequencer',
                'beep.constants',
            ],
            'optimize': 2,
            'silent': True,
            'zip_include_packages': '*',
            'zip_exclude_packages': '',
            'include_msvcr': True,
            'build_exe': './_build/',
        },
    },
    executables=[cible],
)

shutil.copyfile('./sample.twitch', './_build/sample.twitch')
