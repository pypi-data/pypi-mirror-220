from setuptools import setup, find_packages

setup(
    name='checktoxicity',
    version='0.1.1',
    description='A package for content moderation using Hugging Face Toxic-BERT model',
    author='Pawan Kumar',
    author_email='pawankumar49871@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
)
