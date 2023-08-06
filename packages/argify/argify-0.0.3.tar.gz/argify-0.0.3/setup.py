from setuptools import setup, find_packages

with open('./README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='argify',
    version='0.0.3',
    author='Plaraje',
    author_email='mat.demoya@gmail.com',
    description='Make your script args easier',
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
    url='https://github.com/plaraje/Chromify',
)
