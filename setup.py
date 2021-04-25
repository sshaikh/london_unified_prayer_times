#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click',
                'click-default-group',
                'jsonschema',
                'python-dateutil',
                'appdirs',
                'tzlocal',
                'humanize',
                'beautifulsoup4']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Shakil Shaikh",
    author_email='sshaikh@users.noreply.github.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="A library for retrieving data from The London Unified Prayer Timetable.",
    entry_points={
        'console_scripts': [
            'lupt=london_unified_prayer_times.cli:main',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='london_unified_prayer_times',
    name='london_unified_prayer_times',
    packages=find_packages(include=['london_unified_prayer_times', 'london_unified_prayer_times.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/sshaikh/london_unified_prayer_times',
    version='1.1.0',
    zip_safe=False,
)
