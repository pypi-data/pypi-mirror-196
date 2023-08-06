from setuptools import setup, find_packages
import os

# #Generating requirements.txt 
# os.popen("/usr/local/bin/pipreqs mediaquery").read().splitlines()
# os.popen("dpkg-source --before-build .")

# #Reading it
# with open('mediaquery/requirements.txt', 'r') as f:
#     requirements = f.read().splitlines()

requirements = os.popen("/usr/local/bin/pipreqs mediaquery --print").read().splitlines()
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
setup(
    name='mediaquery',
    version='0.1.6',
    author='Sibidharan',
    author_email='sibi@selfmade.ninja',
    description='MediaQuery is a wrapper for mediainfo tool',
    packages=find_packages(),
    url='https://git.selfmade.ninja/sibidharan/mediaquery-with-mediainfo',
    install_requires=requirements,
    long_description=long_description,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': [
            'mediaquery=mediaquery.mediaquery:main',
        ],
    },
)