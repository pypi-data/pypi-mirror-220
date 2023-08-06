from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='pwvalid',
    version='0.3',
    description='Validate Emails with ease',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vinay Chaudhary',
    packages=['pwvalid'],
    install_requires=['requests']
)
