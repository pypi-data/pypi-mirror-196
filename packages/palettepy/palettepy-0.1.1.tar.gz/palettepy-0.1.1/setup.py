from setuptools import setup, find_packages
from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="palettepy",
    version="0.1.1",
    description="This library helps you to print colored text in easy way and has support to rgb colors",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.linkedin.com/in/mario-nageh-744b67116/",
    author="Mario Nageh",
    author_email="marionageh7@gmail.com",
    license="MIT",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    packages=["palettepy"],
    keywords=['COLORS', 'PRINTING', 'STYLES'],
    download_url='https://github.com/user/reponame/archive/v_01.tar.gz',
    include_package_data=True,
    install_requires=[]
)
