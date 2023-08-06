from setuptools import setup

setup(
    name='aws-key-rotator-project',
    version='1.0.0',
    author='Barton Elles',
    description=('An AWS key rotator. Currently only provides key deletion '
                 'functionality. Rotates based on age and usernames passed. '
                 'Check help of CLI tool with aws-key-rotator -h.'),
    packages=[''],
    install_requires=[
        'boto3==1.28.6',
        'botocore==1.31.6'
    ],
    python_requires='>3.10.0',
    entry_points={
        'console_scripts': [
            'aws-key-rotator=cli:main'
        ]
    },
)