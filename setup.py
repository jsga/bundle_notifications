#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=7.0', 'pandas>=1.0.0','tabulate>=0.8.6']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Javier SG",
    author_email='javiersaezgallego@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7'
    ],
    description="Tool for bundling notifications",
    entry_points={
        'console_scripts': [
            'bundle_notifications=bundle_notifications.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='bundle_notifications',
    name='bundle_notifications',
    packages=find_packages(include=['bundle_notifications', 'bundle_notifications.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jsga/bundle_notifications',
    version='0.1.0',
    zip_safe=False,
)
