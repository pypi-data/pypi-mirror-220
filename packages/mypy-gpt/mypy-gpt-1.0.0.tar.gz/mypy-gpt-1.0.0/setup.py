from setuptools import setup
with open('requirements.txt') as f:
    requirements = f.read().splitlines()
import pkg_resources
import setuptools
import pathlib

with pathlib.Path('requirements.txt').open() as requirements_txt:
    install_requires = [
        str(requirement)
        for requirement
        in pkg_resources.parse_requirements(requirements_txt)
    ]

setup(
    name='mypy-gpt',
    version='1.0.0',
    packages=['mypy_gpt'],
    url='https://github.com/eyalk11/mypy-gpt',
    license=' AGPL-3.0 license',
    author='ekarni',
    author_email='',
    description='Python minor issue resolver (mypy) using gpt by openai! ',
    install_requires=install_requires
)
