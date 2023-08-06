from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="enigma_lib_insper",
    version="1.0.0",
    author="Alan e Esdras",
    author_email="alanm2@al.insper.edu.br",
    description="Uma biblioteca para encriptar e decriptar mensagens com o Enigma",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alanmath/ENIGMA",
    packages=['enigma_lib_insper'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy>=1.19.3"
    ]
)