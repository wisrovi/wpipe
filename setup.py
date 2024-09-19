from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="wpipe",  # El nombre de tu paquete
    version="0.1.2",  # La versión de tu paquete
    description="Libreria para crear pipelines conectados a una API",
    author="William Steve Rodriguez Villamizar",
    author_email="wisrovi.rodriguez@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "loguru",
        "pandas",
        "pyyaml",
        "rich",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Build Tools",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.6",  # Requiere Python 3.6 o superior
    long_description_content_type="text/markdown",
    long_description=long_description,
    license="MIT",
    url="https://github.com/wisrovi/wpipe",
)
