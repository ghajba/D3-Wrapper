# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='d3_api',
    version='0.1',
    description='Python client for Diablo 3 web api',
    author='GHajba',
    url='https://github.com/ghajba/D3-wrapper',
    license='MIT',
    packages=find_packages(exclude=('tests')),
    py_modules=['d3_api'],
    install_requires=['urllib','json']
)