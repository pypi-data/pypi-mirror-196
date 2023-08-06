from setuptools import setup, find_packages


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="poncipher",
    version="1.0",
    author="Its-MatriX",
    description="PonCipher is library for encoding data (include your Python projects)",
    long_description=readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ],
    keywords="cipher encoder encoder-decoder",
    python_requires=">=3",
)
