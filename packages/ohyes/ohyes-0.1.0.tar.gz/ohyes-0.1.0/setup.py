from setuptools import setup, find_packages

# Package metadata
name = "ohyes"
version = "0.1.0"
description = "Your package description."
author = "Oh no"
author_email = "dontshaves@havesnots.nothaves"
url = ""
license = "MIT"

# Package dependencies
install_requires = [
    # Add your package dependencies here
]

# Other configurations
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

# Call setup() to configure the package
setup(
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    classifiers=classifiers,
    packages=find_packages(),
    install_requires=install_requires,
)
