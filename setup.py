from setuptools import setup
import sys
import json

with open('metadata.json', 'r', encoding='utf-8') as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_walworthpolynesian',
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_walworthpolynesian'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'walworthpolynesian=lexibank_walworthpolynesian:Dataset',
        ]
    },
    install_requires=[
        'pylexibank>=2.1',
    ],
    extras_require={
        'test': [
            'pytest-cldf',
        ],
    },
)
