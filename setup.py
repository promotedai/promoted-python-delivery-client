# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="promoted-python-delivery-client",
    version="2.0.0",
    description="Promoted.ai Python Delivery Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/promotedai/promoted-python-delivery-client",
    author="Scott McMaster",
    author_email="scott@promoted.ai",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["promoted_python_delivery_client", "promoted_python_delivery_client.client", "promoted_python_delivery_client.model"],
    include_package_data=True,
    install_requires=["dataclasses_json", "requests", "ujson"],
    setup_requires=["pytest-runner", "pytest-mock"],
    tests_require=["pytest", "nose", "nose-timer"],
    test_suite="tests",
)
