#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

import setuptools
import img2jb2pdf

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    install_requires = fh.read().splitlines()

setuptools.setup(
    name="img2jb2pdf",
    version=img2jb2pdf.__version__,
    url="https://github.com/DracoUnion/img2jb2pdf",
    author=img2jb2pdf.__author__,
    author_email=img2jb2pdf.__email__,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Documentation",
        "Topic :: Scientific/Engineering :: Image Processing",
        "Topic :: Utilities",
    ],
    description="将二值图像转换为 JBIG2Decode 编码的 PDF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=[
        "pdf",
        "image",
        "binarize",
        "jbig2",
    ],
    install_requires=install_requires,
    python_requires=">=3.6",
    packages=setuptools.find_packages(),
    package_data={'': ['*']},
)
