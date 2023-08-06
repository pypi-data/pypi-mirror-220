from setuptools import setup, find_packages

setup(
    name='inscodegpt', 
    version='1.4',
    author='Yanhui',
    author_email='yanhui@csdn.net',
    description='Inscode GPT API python package',
    packages=find_packages(),
    install_requires=['requests'], 
)