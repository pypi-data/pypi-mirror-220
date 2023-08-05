from setuptools import setup, find_packages ,Extension
import os
with open('LICENSE') as f:
    license_text = f.read()

with open("README.md") as f:
    desc = f.read()

setup(
    author='Pallav',
    name='stockscraper',
    version='0.1.0',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    packages=['stockscraper'],
    install_requires=[
        'tqdm>=4.64.1',
        'beautifulsoup4>=4.9.0',
        'requests>=2.0.0',
    ],
    description='A Tool for collecting stock data, to do fundamental analysis and does not predict or recommend any stock in particular.',
    url='https://github.com/pallav2905-py/stockscraper',
    long_description_content_type='text/markdown',
    long_description=desc,
    license=license_text,
)