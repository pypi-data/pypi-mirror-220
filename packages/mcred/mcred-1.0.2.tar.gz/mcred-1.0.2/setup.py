# read the contents of your README file
from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="mcred",
    version="1.0.2",
    author="Moses Dastmard",
    description="manage credentials from remote server",
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=["mpath", "mclass"]
    
)