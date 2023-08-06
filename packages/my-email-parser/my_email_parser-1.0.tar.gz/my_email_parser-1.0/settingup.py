from setuptools import setup, find_packages

setup(
    name='my_email_parser',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'win32com',
        'openpyxl'
    ],
    author='Your Name',
    description='A library for parsing Outlook emails and saving data to Excel.',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
