from setuptools import setup, find_packages

VERSION = "1.0.0"
DESCRIPTION = "Utilities with Keycloak"

# Setting up
setup(
    name="py-keycloak-utils",
    version=VERSION,
    author="KE",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "flask>=2.0.0,<=2.2.3",
        "python-keycloak==3.3.0"
    ],
    keywords=["python", "flask", "PyJWT", "decorator", "token", "keycloak"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Unix",
        "Operating System :: MacOS",
    ],
)
