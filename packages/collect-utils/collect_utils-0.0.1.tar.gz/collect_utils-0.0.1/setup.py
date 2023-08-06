# -*- coding: UTF-8 -*-

"""
Author: Henry Wang
Date: 2023-07-20 14:03
Short Description:

Change History:

"""

from setuptools import setup, find_packages


setup(
    name = "collect_utils",
    version = '0.0.1',
    keywords = ("pip3", "collect_utils",'henry'),
    description = "utils for collect program.",
    long_description = "utils for collect program.",
    license = "MIT Licence",
    url = "https://github.com/yunsansheng/collect-utils",
    author = "henry.wang",
    author_email = "shanandone@qq.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = []
)

