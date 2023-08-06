from setuptools import setup, find_packages


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='encorelib',
    version='0.0.1',
    author='Encore Ecosystem',
    author_email='meshushkevich.work@gmail.com',
    description='This library contains several utilities for ecosystem products',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/encore-ecosystem/speclib',
    packages=find_packages(),
    install_requires=[
      'termcolor~=2.2.0',
      'colorama~=0.4.6',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='cli menu terminal python encore',
    project_urls={
        'Documentation': 'https://github.com/encore-ecosystem/speclib'
    },
    python_requires='>=3.6'
)
