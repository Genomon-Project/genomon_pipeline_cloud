#!/usr/bin/env python

from setuptools import setup, find_packages
from codecs import open
from os import path
from genomon_pipeline_cloud import __version__

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name = 'genomon_pipeline_cloud',
    version = __version__,
    description = 'Python tools for executing Genomon pipeline in cloud environments.',
    url = 'https://github.com/Genomon-Project/genomon_pipeline_cloud',
    author = 'Yuichi Shiraishi, Ai Okada, Kenichi Chiba',
    author_email = 'genomon.devel@gmail.com',
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
    package_data={'genomon_pipeline_cloud': ['script/*']},
    # install_requires = ['dsub'],

    entry_points = {'console_scripts': ['genomon_pipeline_cloud = genomon_pipeline_cloud:main']}

)

