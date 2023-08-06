import os

from buybackprogram import __version__
from setuptools import find_packages, setup

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="aa-buybackprogram",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description="Buyback program plugin app for Alliance Auth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/paulipa/allianceauth-buyback-program",
    author="Ikarus Cesaille",
    author_email="contact@eve-linknet.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.1",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires="~=3.8",
    install_requires=[
        "allianceauth>=3.0",
        "django-eveuniverse>=1.0.0",
        "allianceauth-app-utils>=1.18.0",
    ],
)
