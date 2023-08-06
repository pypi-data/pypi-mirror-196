from setuptools import setup, find_packages

with open('mediaquery/requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='mediaquery',
    version='0.1.4',
    author='Sibidharan',
    author_email='sibi@selfmade.ninja',
    description='MediaQuery is a wrapper for mediainfo tool',
    packages=find_packages(),
    url='https://git.selfmade.ninja/sibidharan/mediaquery-with-mediainfo',
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'mediaquery=mediaquery.mediaquery:main',
        ],
    },
)