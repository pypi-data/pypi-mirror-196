from setuptools import setup, find_packages
import pathlib
setup(
    name='togamemaker',
    version='0.0.1',
    py_modules = ['togamemaker'],
    license='MIT License',
    platforms='any',
    install_requires=['time','random','os']
)