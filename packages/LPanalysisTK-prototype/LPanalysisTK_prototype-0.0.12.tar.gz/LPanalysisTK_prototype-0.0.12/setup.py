from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.12'
DESCRIPTION = "A protoype of a new package in python for Laplacefintools analysis"
LONG_DESCRIPTION = "A protoype of a new package in python for Laplacefintools analysis"

# Setting up
setup(
    name="LPanalysisTK_prototype",
    version=VERSION,
    author="Nabil Benjaa",
    author_email="nabil.benjaa@laplaceinsights.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    setup_requires=['wheel'],
    install_requires=["pandas","numpy"],
    keywords=["Analysis", "Fintools"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

