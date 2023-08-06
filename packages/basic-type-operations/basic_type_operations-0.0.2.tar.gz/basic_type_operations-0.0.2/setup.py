from setuptools import setup, find_packages

version = '0.0.2'  # Any format you want
DESCRIPTION = 'Easily cut the basic type by basic_type_operations'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='basic_type_operations',
    packages=find_packages(),
    version=version,
    license='MIT',
    description='Short description',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="SkyOceanChen",
    author_email="skyoceanchen@foxmail.com",
    url='https://github.com/SkyOceanchen/basic_type_operations.git',
    keywords=['basic_type', 'python', "str", "list", "numpy", "number", "datetime", "time", 'calendar'],
    install_requires=[
        # All external pip packages you are importing
        'numpy',
        'fuzzywuzzy',
        'pinyin',
        'djangorestframework',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.10',
    ],
)
# python setup.py bdist_wheel sdist