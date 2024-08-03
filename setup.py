from setuptools import setup
import os

def strip_comments(l):
    return l.split('#', 1)[0].strip()

def reqs(*f):
    with open(os.path.join(os.getcwd(), *f), encoding='utf-8') as f:
        return [strip_comments(L) for L in f if strip_comments(L)]

setup(
    name='txtra',
    version='0.0.1',
    install_requires=reqs('requirements.txt'),
    entry_points={
        'console_scripts':[
            'txtra = txtra.__main__:main',
        ],
    },
)