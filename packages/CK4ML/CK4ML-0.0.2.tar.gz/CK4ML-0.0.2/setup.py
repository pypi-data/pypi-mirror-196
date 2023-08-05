import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CK4ML",
    version="0.0.2",
    author="harvin",
    author_email="haowenw98@gmail.com",
    description="causal knowledge for machine learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/whw199833/CK4ML",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)