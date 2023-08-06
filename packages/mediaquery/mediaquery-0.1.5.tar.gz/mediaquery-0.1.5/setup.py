from setuptools import setup, find_packages
import os

# #Generating requirements.txt 
# os.popen("/usr/local/bin/pipreqs mediaquery").read().splitlines()
# os.popen("dpkg-source --before-build .")

# #Reading it
# with open('mediaquery/requirements.txt', 'r') as f:
#     requirements = f.read().splitlines()

requirements = os.popen("/usr/local/bin/pipreqs mediaquery --print").read().splitlines()

setup(
    name='mediaquery',
    version='0.1.5',
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