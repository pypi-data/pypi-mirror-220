from setuptools import setup

with open("READ.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chungus",
    version="0.0.0",
    author="PyModuleDev",
    author_email="pxcom@mail.com",
    description="Chunky Module",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["chungus"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.6"
)
