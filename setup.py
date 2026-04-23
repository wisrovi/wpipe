"""
Setup configuration for the wpipe package.

This module handles the packaging and distribution of the wpipe library,
a tool for creating pipelines connected to an API.
"""

from pathlib import Path
from typing import List
from setuptools import setup, find_packages

def get_long_description() -> str:
    """
    Retrieve the long description from the README.md file.

    Returns:
        str: The content of the README.md file.
    """
    this_directory: Path = Path(__file__).parent
    readme_path: Path = this_directory / "README.md"
    if readme_path.exists():
        return readme_path.read_text(encoding="utf-8")
    return "Libreria para crear pipelines conectados a una API"

def run_setup() -> None:
    """
    Execute the setup process for the package.
    """
    install_requires: List[str] = [
        "requests",
        "loguru",
        "pandas",
        "pyyaml",
        "rich",
    ]

    setup(
        name="wpipe",
        version="2.1.0",
        description="Library for creating pipelines connected to an API",
        author="William Steve Rodriguez Villamizar",
        author_email="wisrovi.rodriguez@gmail.com",
        packages=find_packages(),
        install_requires=install_requires,
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Build Tools",
            "Intended Audience :: Developers",
        ],
        python_requires=">=3.6",
        long_description_content_type="text/markdown",
        long_description=get_long_description(),
        license="MIT",
        url="https://github.com/wisrovi/wpipe",
    )

if __name__ == "__main__":
    run_setup()
