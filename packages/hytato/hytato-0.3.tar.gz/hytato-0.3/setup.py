import setuptools; import re

# https://packaging.python.org/en/latest/guides/making-a-pypi-friendly-readme/
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setuptools.setup(
    name='hytato',
    description='Module for storing python dictionaries in a different format.',
    version='0.3',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Hypurrnating',
    url='https://github.com/Hypurrnating/potato',
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[   "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License",
                    "Operating System :: Microsoft :: Windows",
                    "Operating System :: Unix"],
    python_requires=">=3.2",
    install_requires=[],
    include_package_data=True,
)