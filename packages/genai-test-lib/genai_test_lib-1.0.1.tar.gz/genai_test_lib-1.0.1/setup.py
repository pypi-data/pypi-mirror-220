from setuptools import setup
from setuptools import setup, find_packages
setup(
    name='genai_test_lib',
    version='1.0.1',
    packages=find_packages(),
    install_requires=[
        'openai','langchain'
    ],
    zip_safe=False
)
