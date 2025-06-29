#!/usr/bin/env python3
"""
Setup script for 2D/3D Asset Downloader
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="2d-3d-asset-downloader",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Ücretsiz 2D ve 3D oyun asset'lerini çeşitli sitelerden indiren Python uygulaması",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/2d-3d-asset-downloader",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "asset-downloader=main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="web scraping, game assets, 2d, 3d, download, automation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/2d-3d-asset-downloader/issues",
        "Source": "https://github.com/yourusername/2d-3d-asset-downloader",
        "Documentation": "https://github.com/yourusername/2d-3d-asset-downloader#readme",
    },
) 