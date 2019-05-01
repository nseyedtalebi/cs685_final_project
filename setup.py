#Made by Joe Kaninberg
import setuptools
from distutils.core import setup
from Cython.Build import cythonize

setup(name='Test app',
      ext_modules=cythonize("model.pyx"))
