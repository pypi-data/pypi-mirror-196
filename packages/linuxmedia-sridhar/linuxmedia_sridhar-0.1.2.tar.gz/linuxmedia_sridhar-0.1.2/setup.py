from setuptools import setup, find_packages
import os

with open('main/requirements.txt','r') as fi:
    requirements=fi.read()

setup(
    name='linuxmedia_sridhar',
    version='0.1.2',
    author='Sridhar',
    author_email='dcsvsridhar@gmail.com',
    description='Linuxmedia is a wrapper for 60 above 60+ Linux Commands',
    packages=find_packages(),
    url='https://git.selfmade.ninja/SRIDHARDSCV/packaging_own_cli_tool',
    install_requires=requirements,
    # long_description=long_description,
    # long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'linuxmedia=main.main:main',
        ],
    },
)