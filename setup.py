from setuptools import setup, find_packages

setup(
    name='betterbeeswarm',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'seaborn',
    ],
    description='Custom implementation of seaborn Beeswarm class',
    author='tvarovski (Jerzy Twarowski)',
    author_email='tvarovski1@gmail.com',
    url='https://github.com/tvarovski/BetterBeeswarm',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)