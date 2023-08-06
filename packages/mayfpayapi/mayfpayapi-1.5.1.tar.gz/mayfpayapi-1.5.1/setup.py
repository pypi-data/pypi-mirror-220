from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mayfpayapi',
    version='1.5.1',
    author='MayfPay',
    author_email='support@mayfpay.top',
    description='MayfPayApi is a Python library for interacting with the MayfPay payment system API. It provides methods for retrieving kassa balances, creating and checking invoices.',
    url='https://github.com/MAYFPAY/MayfPayApi',
    packages=find_packages(),
    py_modules=['mayfpayapi'],
    project_urls={
        'Source': 'https://github.com/MAYFPAY/MayfPayApi',
        'Documentation': 'https://mayfpay.top/docs',
        'Bug Reports': 'https://github.com/MAYFPAY/MayfPayApi/issues',
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'requests',
    ],
)
