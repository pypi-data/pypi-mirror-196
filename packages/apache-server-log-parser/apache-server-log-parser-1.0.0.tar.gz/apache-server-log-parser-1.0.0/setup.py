from setuptools import setup

setup(
    name='apache-server-log-parser',
    version='1.0.0',
    packages=[''],
    description='A simple script to parse apache logs',
    entry_points={
        'console_scripts': [
            'apache-server-log-parser = log_parser:Main'
        ]
    },
    install_requires=[
        'optparse'
    ]
)
