from setuptools import setup, find_packages

VERSION = '0.0.0'
DESCRIPTION = 'RNA-seq pipeline from terminal'
LONG_DESCRIPTION = 'Automation of RNA-seq from terminal. This package performs fastqc, generate genome index, aligning the genome and generating count matrix'

# Setting up
setup(
    name="RNA-seq",
    version=VERSION,
    author="Ahmed Ghobashi",
    author_email="<ahmed.ghobashi.ag@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    url='https://github.com/Ahmed-Ghobashi/RNA-seq',
    packages=find_packages(),
    include_package_data=True,
    scripts=['package_runner.py'],
    keywords=['python', 'RNA-seq package'],

)