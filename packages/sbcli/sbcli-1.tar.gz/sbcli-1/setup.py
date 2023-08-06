from pkg_resources import parse_requirements
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sbcli',
    version='1',
    packages=find_packages(),
    package_dir={'api': ''},
    url='https://github.com/simplyblock-io/ultra',
    author='Hamdy Khader',
    author_email='hamdy.khader@gmail.com',
    description='CLI for managing SimplyBlock cluster',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_reqs=parse_requirements('requirements.txt'),
    entry_points={
            'console_scripts': [
                'sbcli=api.main',
            ]
        }
)
