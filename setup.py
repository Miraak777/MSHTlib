from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mshtlib",
    version="0.1.0",
    author="Miraak777",
    author_email="miraakbs@gmail.com",
    description="Library for creating micro services",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Miraak777/MSHTlib",
    packages=find_packages('mshtlib', include=['architecture*', 'scripts.py']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "coverage==7.5.1",
        "black==24.4.2",
        "isort==5.13.2",
        "pylint==3.2.2",
    ],
    entry_points={
        'console_scripts': [
            'msinit=scripts:ms_init',
        ],
    },
)
