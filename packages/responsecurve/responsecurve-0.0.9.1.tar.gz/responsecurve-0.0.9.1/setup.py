from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='responsecurve',
    version='0.0.9.1',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
        'scikit-learn'
    ],
    author='Ishan Ramrakhiani',
    author_email='ishanramrakhiani@gmail.com',
    description='A library for detecting response curves in time series data.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/himanalot/ResponseCurve'
)