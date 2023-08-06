import subprocess
import os

from setuptools import setup, find_packages
from setuptools.command.install import install

current_directory = os.path.dirname(os.path.abspath(__file__))


class BlpapiInstall(install):
    """Customized setuptools install command which uses pip to install the bloomberg .whl file."""
    def run(self):
        subprocess.check_call(['pip', 'install', r"C:\Users\maidorn\IdeaProjects\bb-connector\blpapi\win32\blpapi-3.19.3-cp311-cp311-win_amd64.whl"])
        install.run(self)


with open(r'C:\Users\maidorn\IdeaProjects\bb-connector\main\requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bb-connector",
    version="0.0.1",
    author='Richard Maidorn',
    author_email="maidorn@orcacapital.de",
    description="This project is a flask-service for calculating Bloomberg query's as a REST service.",
    python_requires='>=3.11',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=required,
    cmdclass={
                 'install': BlpapiInstall
    },
    entry_points={
        'console_scripts': [
            "bb-connector=main.main:main",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        'License :: OSI Approved :: MIT License',
        "Operating System :: Microsoft :: Windows",
    ],
    project_urls={
        "Source Code": "https://gitlab.com/orca-capital/algo-trading/python/bb-connector"
    }
)
