from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='scriptax',
    packages=find_packages(),
    version='0.0.4',
    description='Scriptax is a powerful driver for the Apitax framework which exposes an automation first language used to quickly script together automation.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Shawn Clake',
    author_email='shawn.clake@gmail.com',
    url='https://github.com/Apitax/Scriptax',
    keywords=['restful', 'api', 'commandtax', 'scriptax', 'apitax', 'drivers', 'plugins'],
    include_package_data=True,
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'antlr4-python3-runtime',
        'apitaxcore==3.0.6',
        'commandtax==0.0.8',
    ],
)
