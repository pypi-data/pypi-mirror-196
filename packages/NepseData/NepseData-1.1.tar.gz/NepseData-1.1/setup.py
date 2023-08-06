from setuptools import setup
long_description = open('README.md').read()
setup(
    name = "NepseData",
    version = "1.1",
    description = "Every information and data in Nepal Share Market are available",
    long_description=long_description,
    author = "Anup Timsina",
    packages = ['NepseData'],
    install_requires = ['requests','bs4']
)
    