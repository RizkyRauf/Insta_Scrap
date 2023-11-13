from setuptools import setup

with open("requirements.txt") as file:
    requirements = file.read().splitlines()

setup(
    name="",
    version="0.0.1",
    description="",
    packages=["..."],
    python_requires=">=3.7",
    install_requires=requirements
)
