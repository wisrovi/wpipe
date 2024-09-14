from setuptools import setup, find_packages

setup(
    name="wpipe",
    version="0.1.0",
    description="Una descripción breve de tu librería",
    author="William Steve Rodriguez Villamizar",
    author_email="wisrovi.rodriguez@gmail.com",
    packages=find_packages(),
    install_requires=[
        "requests",
        "loguru",
        "pandas",
        "pyyaml",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Requiere Python 3.6 o superior
)
