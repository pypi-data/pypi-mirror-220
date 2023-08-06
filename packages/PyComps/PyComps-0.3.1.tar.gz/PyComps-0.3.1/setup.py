import setuptools
from setuptools import setup

with open('README.md', 'r') as f:
    readme = f.read()
    
setup(
    name='PyComps', 
    version='0.3.1',
    description='A sample Python package',
    author='Edoardo Mancini',
    author_email='edoardo.mancini0@gmail.com',
    classifiers=["License :: OSI Approved :: MIT License"],
    url='https://github.com/edo-147/PyComp',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=['PyComps'],
    
)


