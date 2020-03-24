from setuptools import setup, find_packages

long_description = open("Readme.md").read()

setup(
    name='artifactorium',
    version='0.9.0',
    packages=find_packages(),
    url='https://github.com/csxeba/Artifactorium.git',
    license='MIT',
    author='csxeba',
    author_email='csxeba@gmail.com',
    description='Artifact and path manager',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
