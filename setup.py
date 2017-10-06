from setuptools import setup, find_packages

setup(
    name="sysdmanager",
    version="0.1.1",
    license="BSD-3",
    author="Aleksandr Aleksandrov",
    author_email="aleksandr.aleksandrov@emlid.com",
    url="https://github.com/emlid/systemd-manager",
    packages=find_packages(exclude=["tests"])
)
