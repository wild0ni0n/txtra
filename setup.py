from setuptools import setup
import os

def readme():
    with open('README.md', 'r', encoding='utf-8') as f:
        return f.read()

def strip_comments(l):
    return l.split('#', 1)[0].strip()

def reqs(*f):
    with open(os.path.join(os.getcwd(), *f), encoding='utf-8') as f:
        return [strip_comments(L) for L in f if strip_comments(L)]

setup(
    long_description=readme(),
    install_requires=reqs('requirements.txt'),
    include_package_data=True,
)