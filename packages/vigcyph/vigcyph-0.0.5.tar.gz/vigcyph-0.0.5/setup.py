from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'Encodes and Decodes Vigenere Cypher'

# Setting up
setup(
    name="vigcyph",
    version=VERSION,
    author="iguessidothings",
    description=DESCRIPTION,
    long_description='pip install vigcyph, from vigcyph import vigenere, vigcyph.vigenere(encode/decode, msg, key), returns as a string',
    long_description_content_type ='text/plain',
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'encode', 'decode', 'cypher', 'vigenere', 'code'],
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)