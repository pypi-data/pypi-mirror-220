from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='sbcli',
    version='3',
    packages=find_packages(),
    url='https://github.com/simplyblock-io/ultra',
    author='Hamdy Khader',
    author_email='hamdy.khader@gmail.com',
    description='CLI for managing SimplyBlock cluster',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "foundationdb",
        "requests",
        "numpy",
        "typing",
        "prettytable",
        "docker",
        "psutil",
    ],
    entry_points={
        'console_scripts': [
            'sbcli=management.cli:__main__',
        ]
    }
)
