from setuptools import setup, find_packages
import codecs
import os

DESCRIPTION = 'tech_in_seconds'
LONG_DESCRIPTION = 'A package to genral and mathamathical operations'
# https://github.com/Avinash6798/avi_package
# Setting up
setup(
    name="tech_in_seconds",
    author="Aadesh Lokhande",
    author_email="aadeshlokhande11@gmail.com",
    version="1.0.1",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['arithmetic', 'math', 'mathematics', 'tables','barakhadi','mean','contact', 'aadesh lokhande', 'tech in seconds', ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)