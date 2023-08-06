from setuptools import setup, find_packages

setup(
    name="inscode_api",
    version="0.1",
    author="yanhui",
    author_email="yanhui@csdn.net",
    description="A library for interacting with the INSCODE API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    packages=find_packages(),
    install_requires=["requests"],
)