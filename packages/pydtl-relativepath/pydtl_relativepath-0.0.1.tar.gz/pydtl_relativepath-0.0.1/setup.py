import os
from setuptools import setup, find_packages

with open(
    os.path.join(os.path.dirname("__file__"), "README.md"), "r", encoding="utf-8"
) as readme_file:
    readme = readme_file.read()

requirements = []

setup(
    name="pydtl_relativepath",
    version="0.0.1",
    description="python tool to solve many issues with relative paths and imports in your complex framework.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="NanthagopalEswaran",
    author_email="nanthagopaleswaran@gmail.com",
    url="https://github.com/python-dev-tools/pydtl-relativepath",
    packages=find_packages(),
    install_requires=requirements,
    license="MIT",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.9",
    project_urls={
        "Source": "https://github.com/python-dev-tools/pydtl-relativepath",
        "Tracker": "https://github.com/python-dev-tools/pydtl-relativepath/issues",
    },
    keywords="python python-library python-package pydtl relative-path relative-import path-issues root-folder",
)
