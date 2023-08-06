from setuptools import setup, find_packages

setup(
    name="my_outlook_parser",
    version="1.2.0",
    packages=find_packages(),
    install_requires=[
        "pywin32",
        "openpyxl"
        # Add other required dependencies here
    ],
    # Add other metadata like author, description, etc.
)
