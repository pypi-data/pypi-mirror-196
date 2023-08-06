from setuptools import setup, find_packages

setup(
    name="python-simple-package-demo",
    version="1.0.0",
    author="Girish B",
    description="Sample package manager",

    packages=find_packages(),
    classifiers=[
        "Operating System :: OS Independent",
    ],
    install_requires=[],
)