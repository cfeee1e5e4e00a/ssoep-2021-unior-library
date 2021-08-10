from setuptools import setup, find_packages

setup(
  name='unior',
  version='0.2.0',
  description='a python library providing api for пак юниор sensors',
  url='https://github.com/cfeee1e5e4e00a/ssoep-2021-unior-library',
  author='cfeee1e5e4e00a',
  packages=find_packages(where='src'),
  python_requires='>=3.6',
  install_requires=['bleak']
)