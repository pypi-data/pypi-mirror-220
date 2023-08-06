#!/usr/bin/env python

from setuptools import setup, find_packages, Extension
from codecs import open
import glob
import os

data_files = []
directories = glob.glob('py_tls/dependencies/')
for directory in directories:
    files = glob.glob(directory+'*')
    data_files.append(('py_tls/dependencies', files))

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "py_tls", "__version__.py"), "r", "utf-8") as f:
    exec(f.read(), about)

with open("README.md", "r", "utf-8") as f:
    readme = f.read()


setup(
    name='py-async-tls',
    version='0.1.0',
    description='Python TLS client with async support',
    author='Tyler Kruer',
    author_email='tkruer1@gmail.com',
    packages=find_packages(),
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={
        '': ['*'],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries",
    ],
)