try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

from fsimport import __version__    

config = {
    'description': 'fsimport - import files from archives using filesets',
    'author': 'Thorsten Huhn',
    'url': 'https://github.com/thorstenhuhn/fsimport.git',
    'download_url': 'https://github.com/thorstenhuhn/fsimport/archive/master.zip',
    'author_email': 'thorstenhuhn@users.noreply.github.com',
    'version': __version__,
    'install_requires': [
        'click',
        'colorlog',
        'formic',
        'hiyapyco',
        'pyyaml',
        'requests',
    ],
    'extra_requires': {
        'testing': [
            'nose',
        ]
    },
    'entry_points': {
        'console_scripts': [
            'fsimport = fsimport.main:cli',
        ]
    },
    'packages': find_packages(),
    'name': 'fsimport',
}

setup(**config)

