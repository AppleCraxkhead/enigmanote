from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(

    name='enigmanote',  
    version='0.0.1', 
    description='encodes notes with the enigma machine',
    url='https://github.com/AppleCraxkhead/enigmanote',
    author='AppleCraxkhead',
    author_email='applecraxkhead@gmail.com',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],


    keywords='notes, encoding, enigma, fun', 
    packages=find_packages(include=['enigmanote.py']),
    python_requires='>=3.6, <4',

    #install_requires=[''], requires nothing as of now