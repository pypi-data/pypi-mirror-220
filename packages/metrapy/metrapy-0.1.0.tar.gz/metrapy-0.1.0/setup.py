import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="metrapy",  # This is the name of the package
    version="0.1.0",  # The initial release version
    author="pavittarx",  # Full name of the author
    description="batteries included wrapper utility for MetaTrader5's python integration",
    long_description=long_description,  # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),  # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],  # Information to filter the project on PyPi website
    python_requires=">=3.6",  # Minimum version requirement of the package
    py_modules=["connector", "sync"],  # Name of the python package
    package_dir={"": "metrapy"},  # Directory of the source code of the package
    install_requires=["MetaTrader5"],  # Install other dependencies if any
)
