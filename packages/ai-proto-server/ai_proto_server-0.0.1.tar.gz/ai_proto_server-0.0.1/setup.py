# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "ai_proto_server"
VERSION = "0.0.1"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = [
    "connexion>=2.0.2",
    "swagger-ui-bundle>=0.0.2",
    "python_dateutil>=2.6.0"
]

setup(
    name=NAME,
    version=VERSION,
    description="ai-proto",
    author_email="panleiming@linksaas.pro",
    url="",
    keywords=["OpenAPI", "ai-proto"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['ai_proto_server=ai_proto_server.__main__:main']},
    long_description="""\
    ai proto for coder
    """
)

