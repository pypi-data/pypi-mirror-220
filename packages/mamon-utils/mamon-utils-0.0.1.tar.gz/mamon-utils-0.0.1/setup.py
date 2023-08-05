from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

with codecs.open(os.path.join(here, "requirements.txt"), encoding="utf-8") as fh:
    requirements = fh.read().splitlines()


VERSION = '0.0.1'
DESCRIPTION = 'Common tools and utilities'

# Setting up
setup(
    name="mamon-utils",
    version=VERSION,
    author="WessCoby",
    author_email="<wc@wesscoby.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=requirements,
)
