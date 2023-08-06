from setuptools import setup, find_packages

setup(
    name='my_email_parser',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'win32com',
        'openpyxl'
    ],
 
)
