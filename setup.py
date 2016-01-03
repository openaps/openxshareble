# from ez_setup import use_setuptools
# use_setuptools()
from setuptools import setup, find_packages

setup(name              = 'openxshareble',
      version           = '0.0.0',
      author            = 'Ben West',
      author_email      = 'bewest@gmail.com',
      description       = 'Python library for interacting with Dexcom over Bluetooth low energy.',
      license           = 'MIT',
      url               = 'https://github.com/bewest/openxshareble/',
      packages          = find_packages())
