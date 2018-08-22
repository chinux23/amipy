#!/usr/bin/env python

from setuptools import setup

import os

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

extra_files = package_files('maui/package_template')

with open('README.md') as f:
    readme = f.read()

setup(
    name='apple-maui',
    version='1.0.35',
    description='Install MacOS programmatically', # short description
    long_description=readme, # long description from the readme file
    license='Apple Internal', # for internal packages
    author='Chen Huang',
    author_email='chen_huang@apple.com',
    url='https://stash.sd.apple.com/projects/BQA/repos/maui/', # wherever your code lives
    packages=['maui', "maui.locallibs"], # or py_modules (see below for more details)
    package_data={'maui': extra_files},
    # data_files=[('package_template', ['*.jpeg'])],
    # include_package_data=True,
    install_requires = [
        "tqdm",                     # Used for local restore - progress bar.
        "requests",                 # Used for heartbeat
        "paramiko>=2.4.1",          # Used for remote SSH
        "scp",                      # Used for remote restore
        "AppleConnectUtils==0.1.0", # Used for appleconnect
        "netifaces",                # Used for heartbeat,
        "setuptools>=40.0.0",       # Used by osascript
    ], # any dependencies internal or world (OPTIONAL)
    entry_points={
        'console_scripts': [
            'maui = maui.maui:main',
            'createuserpkg = maui.createuserpkg:main'
        ]
    }
)
