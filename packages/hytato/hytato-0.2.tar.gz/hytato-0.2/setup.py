import setuptools; import re

setuptools.setup(
    name='hytato',
    description='Module for storing python dictionaries in a different format.',
    version='0.2',
    long_description='https://github.com/Hypurrnating/potato#readme',
    author='Hypurrnating',
    url='https://github.com/Hypurrnating/potato',
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[   "Programming Language :: Python :: 3",
                    "License :: OSI Approved :: MIT License",
                    "Operating System :: OS Independent"],
    python_requires=">=3.2",
    install_requires=[],
    include_package_data=True,
)