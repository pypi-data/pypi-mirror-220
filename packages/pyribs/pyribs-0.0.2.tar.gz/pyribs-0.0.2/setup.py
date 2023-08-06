"""Warning package for pyribs.

Based on the one for PyTorch: https://pypi.org/project/pytorch/
"""
import sys
from distutils.core import setup

MESSAGE = 'You tried to install "pyribs". The package name for pyribs is "ribs".  Please run "pip install ribs" instead.'

argv = lambda x: x in sys.argv

if (argv('install') or  # pip install
    (argv('--dist-dir') and argv('bdist_egg'))):  # easy_install
    raise Exception(MESSAGE)

if argv('bdist_wheel'):  # modern pip install
    raise Exception(MESSAGE)

setup(
    name='pyribs',
    version='0.0.2',
    maintainer="Bryon Tjanaka",
    maintainer_email="bryon@btjanaka.net",
    url="https://github.com/icaros-usc/pyribs",
    long_description=MESSAGE,
)
