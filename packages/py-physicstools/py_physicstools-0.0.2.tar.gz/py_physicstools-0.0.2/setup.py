from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'physicstools'
LONG_DESCRIPTION = '''A package to perform several physics related equations
This can perform several actions like to convert units or to find something. You can use it anywhere and it is useful for those who want to create fast projects'''

# Setting up
setup(
    name="py_physicstools",
    version=VERSION,
    author="M.veeraragavan",
    author_email="ratnabala555@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['arithmetic', 'math', 'mathematics', 'python', 'veer', 'hitech', 'fast', 'hitech_coder', 'physics', 'equations', 'conversions', 'readable'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)