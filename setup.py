# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='obeach',
    version='0.1.0',
    description='A framework for RGBD Objec Segmentation',
    long_description=readme,
    author='Luiz Eduardo Zis',
    author_email='zisluiz@gmail.com',
    url='https://github.com/zisluiz',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

