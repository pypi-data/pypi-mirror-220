# python3 setup.py sdist bdist_wheel
import src
import setuptools

with open("README.md", "r") as file:
    long_description = file.read()

setuptools.setup(
    name="PipPackageCustomInstaller",
    version="1.0.0",
    author="Jorge Cardona",
    description="Descripción del paquete",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JorgeCardona/PipPackageInstaller",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)