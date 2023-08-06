from setuptools import setup, find_packages

setup(
    name='candor-test',
    version='0.0.2',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    author='FroostySnoowman',
    author_email='froostysnoowmanbusiness@gmail.com',
    description='Simple wrapper for the Candor API.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/FroostySnoowman/Candor',
)