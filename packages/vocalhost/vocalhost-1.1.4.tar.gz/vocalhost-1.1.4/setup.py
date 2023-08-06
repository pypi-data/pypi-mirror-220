from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='vocalhost',
    version='1.1.4',
    py_modules=['vocalhost'],
    install_requires=[
        'websockets',
        'certifi',
        'requests'
    ],
    description='Localhost to Vocalhost, run functions from anywhere',
    long_description=long_description,
    long_description_content_type='text/markdown',
)