from setuptools import setup, find_packages

setup(
    name="spinbench",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "open-spiel==1.5",
        "diplomacy==1.1.2",
        "pettingzoo==1.24.3",
        "anthropic==0.50.0",
        "opencv-python==4.8.0.74",
        "openai==1.61.0",
        "pygame==2.6.1",
        "regex==2024.9.11",
        "diskcache==5.6.3",
        "tenacity==8.2.3",
        "icecream==2.1.3",
        "triton",
        "transformers>=4.49.0",
        "accelerate==1.1.1",
        "bitsandbytes>=0.44.1",
    ],
)
