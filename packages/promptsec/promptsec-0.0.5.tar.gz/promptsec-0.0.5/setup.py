from setuptools import setup, find_packages
import pkg_version

setup(
    name='promptsec',
    version=pkg_version.__version__,
    author='PromptSec Team',
    author_email='team@prompt-security.com',
    description='PromptSec SDK Library',
    url='https://github.com/promptsec/promptsec-sdk-python',
    packages=find_packages(),
    install_requires=[
        'langchain',
        'openai',
        'requests',
    ],
)
