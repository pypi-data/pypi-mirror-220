from setuptools import setup, find_packages


setup(
    name="zonesmart-utils",
    version="0.3.7",
    author="Zonesmart",
    author_email="kamil@zonesmart.ru",
    packages=find_packages(include=["zs_utils", "zs_utils.*"]),
)
