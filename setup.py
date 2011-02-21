# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from os.path import join as pathjoin

VERSION = '0.3dev'

LONG_DESCRIPTION = "".join([
    open(pathjoin("src","README")).read()])

CLASSIFIERS = [
    "Environment :: Web Environment",
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet',
]

setup(
    name='pyrtm',
    version=VERSION,
    description='Remember The Milk API',
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    author='Sridhar Ratnakumar',
    author_email='srid@nearfar.org',
    url='http://bitbucket.org/srid/pyrtm/',
    license='MIT License',
    packages=find_packages("src"),
    package_dir={'': 'src'},
    package_data = {'': ['buildout.cfg']},
    extras_require=dict(
        test=[
            "Nose",
            "minimock",
            "pep8",
        ],
    ),
    test_suite='nose.collector',
    tests_require=['Nose','minimock','pep8'],
    entry_points="""
       [console_scripts]
       rtm_appsample = rtm.samples.app:main
    """,
)

