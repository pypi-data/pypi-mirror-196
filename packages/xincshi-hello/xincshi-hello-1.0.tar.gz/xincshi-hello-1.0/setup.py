from distutils.core import  setup
import setuptools
packages = ['xincshi']# 唯一的包名，自己取名
setup(name='xincshi-hello',
	version='1.0',
	author='xincshi',
    packages=packages,
    package_dir={'requests': 'requests'},)
