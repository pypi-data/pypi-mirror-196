from typing import List

from setuptools import find_packages, setup

import textmentations


def get_version() -> str:
    version = textmentations.__version__
    return version


def get_install_requires(file_path: str = "requirements.txt") -> List[str]:
    with open(file_path) as f:
        install_requires = f.read().splitlines()
    return install_requires


setup(
    name="textmentations",
    version=get_version(),
    description="A Python library for text augmentation that is specialized for Korean.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Jaesu Han",
    author_email="gkswotn9753@gmail.com",
    url="https://github.com/Jaesu26/textmentations",
    packages=find_packages(),
    license="MIT",
    include_package_data=True,
    zip_safe=False,
    install_requires=get_install_requires(),
    python_requires=">=3.6",
)
