from setuptools import setup, find_packages

setup(
    name="neir-auth",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "social-auth-core>=4.0.0",
        "requests>=2.25.0",
    ],
)
