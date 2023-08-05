from setuptools import setup, find_packages

with open('docs/README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Chromify',
    version='1.0.1',
    author='Plaraje',
    author_email='mat.demoya@gmail.com',
    description='Colorful Terminal Prints',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
