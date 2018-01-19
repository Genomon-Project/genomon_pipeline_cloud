#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'genomon_rna_gce',
    version = '0.2.0',
    description = 'Python tools for executing Genomon RNA pipeline in Google Compute Engine.',
    url = 'https://github.com/friend1ws/genomon_rna_gce',
    author = 'Yuichi Shiraishi',
    author_email = 'friend1ws@gmail.com',
    license = 'GPLv3',
    
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Genome Analysis :: RNA-seq',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],

    packages = find_packages(exclude = ['docker']),
    package_data={'genomon_rna_gce': ['script/*']},
    install_requires = ['dsub'],

    entry_points = {'console_scripts': ['genomon_rna_gce = genomon_rna_gce:main']}

)

