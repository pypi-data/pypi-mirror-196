from setuptools import setup, find_packages

setup(
    name='hotsos',
    version='1.0.0',
    packages=find_packages(include=['hotsos*']),
    entry_points={
      'console_scripts': [
        'hotsos=hotsos.cli:main']
    }
)
