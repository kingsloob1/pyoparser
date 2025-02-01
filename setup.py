from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='pyoparser',
    version='1.0.1',
    description='A simple resume parser, JD parser and JD to resume matcher',
    long_description='',
    url='https://github.com/kingsloob1/pyoparser',
    author='Okafor Obinna',
    author_email='kingsloob1@gmail.com',
    license='MIT',
    include_package_data=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    packages=find_packages(),
    install_requires=[
        'datasets>=2.16.0',
        'docx2txt>=0.8',
        'jsonschema>=4.20.0',
        'nltk>=3.8.1',
        'pandas>=2.1.4',
        'pdfminer.six>=20191110',
        'plac>=1.4.2',
        'python-dateutil>=2.8.2',
        'requests>=2.31.0',
        'scikit-learn>=1.3.2',
        'spacy>=3.7.2',
        'tqdm>=4.66.1',
        'urllib3>=2.2.1'
    ],
    zip_safe=False,
    entry_points = {
        'console_scripts': ['pyoparser-resumeparser=pyoparser.command_line:main'],
    }
)
