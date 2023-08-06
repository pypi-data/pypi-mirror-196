from setuptools import setup, find_packages

setup(
    name="vertsplitNN_saf",
    version="0.1.0",
    description="This is a vertical spkit neural network using numpy only",
    author="HIllary Murefu",
    author_email="hillarywang2005@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
