from setuptools import setup, find_packages
import os

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='odoo_helper',
    version='0.1.1',
    packages=find_packages(),
    url='https://github.com/dharmendrasha/odoo_python',
    license='GNU',
    author='dharmendra',
    author_email='dharmendrashah2002@yahoo.com',
    description='simple helper library for connecting database with odoo',
    keywords="odoo sdk api database package",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Database",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    python_requires='>=3.6',                # Minimum version requirement of the package
    install_requires=[]                     # Install other dependencies if any
) 
