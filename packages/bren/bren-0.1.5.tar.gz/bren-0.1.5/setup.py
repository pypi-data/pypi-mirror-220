from setuptools import setup, find_packages

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="bren",
    version="0.1.5",
    description="A simple numpy based neural network library inspired by Tensorflow/Keras.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Om Panchal",
    author_email="om.panchal2022@gmail.com",
    maintainer="Om Panchal",
    maintainer_email="om.panchal2022@gmail.com",
    license="MIT",
    packages=find_packages(),
    package_data={
        "bren": [
            "keras_LICENCE_copy",
            "tensorflow_LICENCE_copy"
        ]
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
	],
    install_requires=["numpy", "requests"]
)