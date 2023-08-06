from setuptools import setup, find_packages

setup(
    name = 'relay_control',
    version = 'V1.0',
    author = 'DCJ',
    description = 'a package to control relay',
    package = find_packages(),
    intall_requires = [
        'pyserial==3.5'
    ]
)