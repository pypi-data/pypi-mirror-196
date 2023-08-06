from setuptools import setup, find_packages

# Setting Up
setup(
    name = "dataminds",
    version = "0.0.1",
    author = "ataozarslan (Ata Ozarslan)",
    author_email = "<ataozarslan@hotmail.com>",
    description = "Easily obtain the error metrics related to the problem you are working on",
    packages = find_packages(),
    install_requires=["pandas", "sklearn"],
    keywords=["regression", "classification", "model evaluation", "error metrics"]
)