from setuptools import find_packages, setup

setup(
    name="GPyTree",
    author="Daniel Dodd",
    author_email="daniel_dodd@icloud.com",
    packages=find_packages(".", exclude=["tests"]),
)