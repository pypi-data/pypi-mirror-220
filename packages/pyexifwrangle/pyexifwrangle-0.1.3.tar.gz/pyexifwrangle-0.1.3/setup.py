from setuptools import setup, find_packages
from pathlib import Path
from pyexifwrangle import __version__

# read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

extra_test = [
    'pytest>=4',
    'pytest-cov>=2',
]

extra_dev = [
    *extra_test,
]

setup(
    name='pyexifwrangle',
    version=__version__,
    description='A helper package for wrangling image EXIF data',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/stephaniereinders/pyexifwrangle',
    author='Stephanie Reinders',
    author_email='reinders.stephanie@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests', 'tests.*']),

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python'
    ],

    install_requires=[
        'pandas',
    ],

    extras_require={
        'dev': extra_dev,
    },
)
