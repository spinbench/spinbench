from setuptools import setup, find_packages

setup(
    name="spinbench",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "open-spiel==1.5",
        "diplomacy==1.1.2",
        "pettingzoo==1.24.3",
    ],
)