from setuptools import setup, find_packages

setup(
    name='pyxcoder',
    version='0.1.0',
    author='Chang Jin',
    author_email='cjin98@163.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ]
)