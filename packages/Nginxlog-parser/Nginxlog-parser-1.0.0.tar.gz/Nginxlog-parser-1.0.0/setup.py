from setuptools import setup

setup(
    name='Nginxlog-parser',
    version='1.0.0',
    packages=[''],
    description='A simple script to parse nginx logs',
    entry_points={
        'console_scripts': [
            'Nginxlog-parser = log_parser:Main'
        ]
    },
    install_requires=[
        'optparse'
    ]
)
