# Databricks notebook source
import setuptools

setuptools.setup(
    name="module_dataquality",
    version="1.0.2",
    author="Balbir",
    author_email="Balbir250894@gmail.com",
    description="data profiling and basic data quality rules check",
    # packages=setuptools.find_packages(include=['*']),
    packages=['dataqualitycheck', 'dataqualitycheck.datasources'],
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ],
    #.....assuming pyspark, pyarrow is preinstalled 
    install_requires=['polars'],
    python_requires='>=3.8',
)