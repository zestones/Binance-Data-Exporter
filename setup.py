from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='binance_data_exporter',
    version='0.1.6',
    description='A tool for exporting in JSON format the historical data of a symbol from Binance',
    author='zestones',
    author_email='idrissbenguezzou@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'binance_data_exporter=binance_data_exporter:main'
        ]
    },
    install_requires=[
        'requests',
        'colorama',
        'tabulate',
    ],

    long_description=long_description,
    long_description_content_type="text/markdown"
)