from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name="simplejsondb",
    version="0.1.0",
    description="Create a simple JSON database with just one line of code!",
    long_description=readme(),
    long_description_content_type='text/markdown',

    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Database",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    url="https://github.com/RealA10N/simplejsondb",

    author="RealA10N",
    author_email="downtown2u@gmail.com",

    keywords="database json csv data simple easy db",
    license="MIT",

    packages=find_packages(),
)
