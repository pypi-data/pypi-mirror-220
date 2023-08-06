from setuptools import setup, find_packages
import os

setup(
    name='promptsec-sdk',
    version=os.environ.get('VERSION', 'unknown-version'),
    author='PromptSec Team',
    author_email='team@prompt-security.com',
    description='PromptSec SDK Library',
    url='https://github.com/promptsec/promptsec-sdk',
    packages=find_packages(),
    install_requires=[
        'langchain',
        'openai',
    ],
)
