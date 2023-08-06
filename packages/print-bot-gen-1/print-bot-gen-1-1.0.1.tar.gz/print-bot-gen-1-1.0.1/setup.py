
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = [line.strip() for line in f.readlines()]

setup(
    name="print-bot-gen-1",
    version="1.0.1",
    packages=find_packages(),
    py_modules=['print_bot_gen_1'],
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'print_bot_gen_1 = print_bot_gen_1:main',
        ],
    },
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',)
