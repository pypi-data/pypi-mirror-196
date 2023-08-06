from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

VERSION = '0.0.1'
DESCRIPTION = 'Interactive python fitting interface'

# Setting up
setup(
    name="pyCftool",
    version=VERSION,
    author="Andreas Forum (TehForum)",
    author_email="<andforum@hotmail.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['PySide6','numpy','scipy','matplotlig',],
    keywords=['python', 'fit','statistics','modelling','science'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)