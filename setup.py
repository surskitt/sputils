#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.readlines()

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Shane Donohoe",
    author_email='shane@donohoe.cc',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description=("A collection of spotify utilities, designed to be used in "
                 "conjunction with other shell utilities."),
    install_requires=requirements,
    dependency_links=[("git+https://git@github.com/plamere/spotipy.git"
                       "@master#egg=spotipy-2.4.4")],
    entry_points={
        'console_scripts': [
            'sputils = sputils.sputils:main'
        ]
    },
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='sputils',
    name='spotify_sputils',
    packages=find_packages(include=['sputils']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/shanedabes/sputils',
    version='0.1.1',
    zip_safe=False,
)
