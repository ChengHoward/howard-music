import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

try:
    README = open(os.path.join(here, 'README.rst'), encoding='utf-8').read()
except:
    README = ""

setup(
    name='h_music',
    version='0.1.4',
    description='howard music',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    # long_description="https://github.com/tt20050510/howard-music",
    long_description = README,
    url='https://github.com/tt20050510',
    author='HowardCheng',
    author_email='18071131140telephone@gmail.com',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='music spider setuptools development',
    install_requires=['requests', 'bs4', 'wcwidth', 'hyper', 'pycryptodome'],
    extras_require={},
    package_data={},
    data_files=[],
    entry_points={'console_scripts': "h-music = h_music.__main__:main"},
    project_urls={
        'Bug Reports': 'https://github.com/tt20050510/howard-music/issues',
        'Source': "https://github.com/tt20050510/howard-music",
    },
)
