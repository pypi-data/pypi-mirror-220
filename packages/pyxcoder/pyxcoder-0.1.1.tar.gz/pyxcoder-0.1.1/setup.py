from setuptools import setup, find_packages

setup(
    name='pyxcoder',
    version='0.1.1',
    author='Chang Jin',
    author_email='cjin98@163.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ]
)