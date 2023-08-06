import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="datacreator",
    version="0.0.1",
    author="BACS_group1",
    author_email="fausyndata@gmail.com",
    description="A synthetic data creator package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fau-syn-data/synthetic-data.git",
    #packages=setuptools.find_packages(),
    packages=['datacreator'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
