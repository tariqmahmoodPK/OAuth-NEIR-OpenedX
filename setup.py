from setuptools import setup, find_packages

setup(
    name="neir-auth",
    version="0.1.7",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "openedx.core.djangoapps": [
            "neir_auth = neir_auth",
        ],
    },
)

