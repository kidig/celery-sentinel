#!/usr/bin/env python

from setuptools import setup, find_packages
import pathlib

from celery_sentinel import __author__, __version__

here = pathlib.Path(__file__).parent.resolve()
requirements = (here / 'requirements.txt').read_text().splitlines() + ["setuptools"]
long_description = (here / 'README.md').read_text(encoding='utf-8')



setup(
    name='celery-sentinel',
    author=__author__,
    version=__version__,
    url='https://github.com/kidig/celery-sentinel',
    description='Redis-Sentinel transport for Celery',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    install_requires=requirements,
    keywords=' '.join([
        'celery',
        'redis',
        'sentinel',
        'broker',
    ]),
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 2 - Pre-Alpha',
    ],
)