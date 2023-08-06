from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="preProcessingGEP",
    version="1.0.5",
    author="Vanshaj Singla",
    author_email="vanshaj.singla@gep.com",
    description="A package for preprocessing text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanshajsingla03/preProcessingGEP",
    packages=["preProcessingGEP"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
