from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='hackerhelp',
    version='0.1',
    author='Mr. Robot',
    author_email='alertsontwitter@gmail.com',
    description='A tool to help hackers',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/AIMadeScripts/reminder',
    py_modules=['hackerhelp'],
    entry_points={
        'console_scripts': [
            'hackerhelp=hackerhelp:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
