from setuptools import setup, find_packages

setup(
    name='filelistener',
    version='1.0.0',
    author='Rishabh Pandey',
    author_email='brikjr@outlook.com',
    description='A tool to find duplicate content within a folder and its subdirectories',
    packages=find_packages(),
    install_requires=[
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'listen = Content.duplicate_content:main'
        ],
    },
)