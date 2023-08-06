from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="binswap",
    version="0.1.1",
    author="temcr",
    description="A tool to monitor a directory and automatically relaunch a binary.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mt9555/binswap",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "watchdog",
    ],
    entry_points={
        "console_scripts": [
            "binswap=binswap.main:main",
        ],
    },
)
