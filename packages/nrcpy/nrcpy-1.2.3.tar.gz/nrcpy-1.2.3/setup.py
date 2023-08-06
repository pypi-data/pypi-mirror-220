from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "readme.md").read_text()

setup(
    name='nrcpy',
    version='1.2.3',
    description='A package for NRC devices',
    author='Hossein Ghaheri',
    author_email='hosseinghaheri@yahoo.com',
    url='https://github.com/Rebox98/nrcpy',
    packages=['nrcpy'],
    install_requires=[],
    long_description = long_description,
    long_description_content_type="text/markdown"
)
