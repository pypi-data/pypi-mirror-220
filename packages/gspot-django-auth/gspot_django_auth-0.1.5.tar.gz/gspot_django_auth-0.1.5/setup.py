from setuptools import setup, find_packages

setup(
    packages=find_packages(["gspot_django_auth", "gspot_django_auth/permissions/"], exclude=["example", "venv"]),
)
