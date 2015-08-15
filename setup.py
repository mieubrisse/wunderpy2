from setuptools import setup, find_packages
from codecs import open
from os import path

script_dir = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
# with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
#     long_description = f.read()

setup(
    name='wunderpy2',
    version='0.1.0',
    description='A Python library for the Wunderlist 2 REST API',
    long_description=long_description,
    url='https://github.com/mieubrisse/wunderpy2',
    author='mieubrisse',
    author_email='mieubrisse@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='wunderpy wunderpy2 wunderlist api cli',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['argparse','requests>=2.7.0'],
)
