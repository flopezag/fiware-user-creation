from setuptools import setup, find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


install_reqs = parse_requirements("requirements.txt")

setup(
    name='fiware-user-creation',
    version='1.2.0',
    packages=find_packages(exclude=['tests*']),
    install_requires=install_reqs,
    url='https://github.com/flopezag/fiware-user-creation',
    license='Apache 2.0',
    author='Fernando Lopez',
    author_email='fernando.lopez@fiware.org',
    keywords=['fiware', 'google sheets', 'JIRA', 'OpenStack', 'Keystone'],
    description='Script to create automatically FIWARE Lab users account from Google Sheet and Jira issues information',
    classifiers=[
                  "License :: OSI Approved :: Apache Software License", ],
    zip_safe=True
)
