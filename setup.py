#!/usr/bin/env python3

from setuptools import setup

with open('VERSION','r') as _f:
    __version__ = _f.read().strip()

setup(
    name='pydm',
    version=__version__,
    author='lnls-sirius',
    description='LNLS Fork of pydm',
    url='https://github.com/lnls-sirius/pydm',
    download_url='https://github.com/lnls-sirius/pydm',
    license='Custom License',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering'
    ],
    packages=['pydm',],
    package_data={'pydm': ['VERSION', ]},
    scripts=['pydm_run.py',],
    zip_safe=False
)
