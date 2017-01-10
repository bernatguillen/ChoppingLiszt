from setuptools import setup,find_packages
from codecs import open
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='ChoppingLiszt',

    version='0.01dev',
    description='Database of food at home',
#    long_description = read('README.md'),

    url = 'https://github.com/bernatguillen/ChoppingLiszt',

    author = 'Bernat Guillen',
    author_email = 'bguillen@gmail.com',
    license='GNU GENERAL PUBLIC LICENSE',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities'
        ],
    keywords = 'SQLite Food Storage',
    test_suite =  'nose.collector',
    tests_require = ['nose'],
    packages=find_packages(exclude = ['tests*']),
    #install_requires=['sqlite3']
)
