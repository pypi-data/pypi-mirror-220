from setuptools import setup, find_packages

setup(
    name="monkeywork",
    version="0.1",
    packages=find_packages(),
    author="Pylomatic",
    author_email="pylomatic@conelab.ch",
    description="Write and edit random files in a given directory",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/pylomatic/monkeywork",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
