# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hil_general_test",  # 包名
    version="1.0.719",
    author="hil",
    author_email="service@vcarsystem.com",
    description="vcarhilclient",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires = ["vcarhilclient","pytest","allure-pytest","PyMySQL"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

