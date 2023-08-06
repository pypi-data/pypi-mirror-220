from setuptools import setup

setup(
    name='webpy-cli',
    version='1.2',
    author='Tejas Nayak',
    author_email='tejasnayak25@outlook.com',
    description='CLI tool for the python WebPy Framework',
    packages=['webpy_cli'],
    entry_points={
        'console_scripts': [
            'webpy-cli = webpy_cli.cli:main'
        ]
    },
)
