from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='customs_tax',
    version='0.0.2',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[],
    python_requires='>=3.11',
    author='Iaaan05',
    author_email='iaaan100500@gmail.com',
    description='A package for calculating customs taxes, duties, and other charges.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/iaaan05/python-customs-tax-package',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11'
    ]
)
