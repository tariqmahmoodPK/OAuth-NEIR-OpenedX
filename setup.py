from setuptools import setup, find_packages

setup(
    name="neir-auth",
    version="0.2.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        # Open edX already provides these, but declaring them makes the package self-describing.
        "social-auth-core>=4.0.0",
        "social-auth-app-django>=5.0.0",
    ],
    entry_points={
        "openedx.core.djangoapps": [
            "neir_auth = neir_auth",
        ],
    },
)
