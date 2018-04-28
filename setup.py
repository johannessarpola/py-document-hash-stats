#!/usr/bin/env python

from setuptools import setup
import unittest


def test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite


setup(name='clustering_cli',
      version='0.1',
      description='Clustering CLI',
      author='Johannes Sarpola',
      author_email='johannes.sarpola@gmail.com',
      url='https://gitlab.com/johannessarpola/',
      packages=['app'],
      setup_requires=['pytest-runner', 'numpy', 'scikit-learn', 'scipy'],
      tests_require=['pytest'], install_requires=['hdbscan']
      )
