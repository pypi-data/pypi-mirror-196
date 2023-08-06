from setuptools import setup, find_packages

setup(
    name="vector2Dim",
    version="0.1",
    author="Pasquale Mainolfi",
    description="Vector2Dim is a python library to manage operations between vectors in 2D in a simple and intuitive way",
    keywords=["vector", "2D", "numpy", "development"],
    python_requires=">=3.10",
    packages=find_packages(exclude=("v2d_test.py")),
    license="LICENSE.txt"
)
