import setuptools

with open("../README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="loq0",
    version="0.0.1",
    author="seorii",
    author_email="me@seorii.page",
    description="League of Quoridor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dastyinc/loq0",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
