import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pygradethis",
    version="0.1.0",
    author="Nischal Shrestha",
    author_email="nsrocker92@gmail.com",
    description="Python autograder to facilitate code output and static code checking.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='autograder education',
    url="https://github.com/nischalshrestha/pygradethis",
    packages=setuptools.find_packages(exclude=("tests")),
    install_requires=[
        "asttokens==2.0.4", 
        "numpy>=1.17.4",
        "pandas>=1.0.3", 
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Education",
    ],
    python_requires='>=3.6',
)
