from setuptools import setup, find_packages
import sys

minpyver = (3, 7)
if sys.version_info < minpyver:
    sys.exit(f'Sorry, Python < {".".join(minpyver)} is not supported')

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='multitoeter',
    version='2',
    description='Send out messages to Mastodon and Twitter using one simplistic unified API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Thomas Phil',
    author_email='thomas@tphil.nl',
    url='https://github.com/Sikerdebaard/MultiToeter',
    python_requires=">=3.7",
    packages=find_packages(),  # same as name
    install_requires=[
        'Mastodon.py>=1.8.0',
        'tweepy>=4.12.1',
        'python-decouple>=3.8',
    ],
)
