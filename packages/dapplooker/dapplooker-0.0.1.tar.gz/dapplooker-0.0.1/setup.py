from setuptools import setup
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now
# 1) we have a top level README file, and 
# 2) it's easier to type in the README file than to put a raw string in below.

def read(*rnames):
    return open(os.path.join(os.path.dirname(os.path.abspath(__file__)), *rnames)).read()
setup(
    name="dapplooker",
    version="0.0.1",
    description="A minimal, complete, python API for DappLooker",
    long_description=read("README.md"),
    url="https://github.com/0xSumitBanik/dapplooker-py-sdk",
    long_description_content_type="text/markdown",
    author="Sumit Banik",
    license="MIT",
    packages=[
        "dapplooker"
    ],
    python_requires='>=3.8',
    install_requires=["requests"],
    include_package_data=True,
    zip_safe=False,
)