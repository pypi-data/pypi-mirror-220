from setuptools import setup

setup(
    name='webplus',
    version='1.0',
    author='Tejas Nayak',
    author_email='tejasnayak25@outlook.com',
    description='CLI tool for the python WebPlus Framework',
    packages=['webplus'],
    entry_points={
        'console_scripts': [
            'webplus = webplus.cli:main'
        ]
    },
)
