from setuptools import setup, find_packages
from pip.req import parse_requirements

install_reqs = parse_requirements("requirements.txt", session=False)
requirements_list = [str(ir.req) for ir in install_reqs]

setup(
    name='fiware-user-creation',
    version='1.0.0',
    packages=find_packages(exclude=['tests*']),
    install_requires=requirements_list,
    url='https://github.com/flopezag/fiware-user-creation',
    license='Apache 2.0',
    author='Fernando Lopez',
    keywords=['fiware', 'google sheets', 'JIRA', 'OpenStack', 'Keystone'],
    author_email='fernando.lopez@fiware.org',
    description='Script to create automatically FIWARE Lab users account from Google Sheet and Jira issues information',
    classifiers=[
                  "License :: OSI Approved :: Apache Software License", ],
)
