# <a name="top"></a>FIWARE Lab user creation service
[![License badge](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Dependency Status](https://gemnasium.com/badges/github.com/flopezag/fiware-user-creation.svg)](https://gemnasium.com/github.com/flopezag/fiware-user-creation)
[![Build Status](https://travis-ci.org/flopezag/fiware-user-creation.svg?branch=master)](https://travis-ci.org/flopezag/fiware-user-creation)
[![Coverage Status](https://coveralls.io/repos/github/flopezag/fiware-user-creation/badge.svg)](https://coveralls.io/github/flopezag/fiware-user-creation)
[![Documentation Status](https://readthedocs.org/projects/fiware-user-creation/badge/?version=latest)](http://fiware-user-creation.readthedocs.io/en/latest/?badge=latest)

* [Introduction](#introduction)
* [Overall description](#overall_description)
* [Build and Install](#build-and-install)
* [Running](#running)
* [Deployment](#deployment)
* [Testing](#testing)
* [Support](#support)
* [License](#license)


## Introduction

Script to create automatically FIWARE Lab users taking the information from the Google Forms
used yo created new FIWARE Lab user account and the information from the JIRA tickets in order
to contrast the information from two sources previously to create the new account.

[Top](#top)

## Overall description

The procedure to create a new FIWARE Lab user account has been updated after the migration 
from the FIWARE GE Keyrock to the OpenStack Keystone. This means that the use of authentication 
process how it was defined in the previous FIWARE Lab have had redefined.

The new procedure was defined in order to follow with the same level of requirements that 
used previously. It means that we have to check the domain email in order to exclude some 
blacklist of domains. The main purpose of this functionality is to prevent the email engine 
generation mails and use only those email domains in which we could be sure that are used 
only for genuine purpose. The defined system should allow the dynamic definition of new 
excluded emails domain.

A new requirements in included in this procedure. We wanted to check that the email is 
confirmed. It means that the creation of a new FIWARE Lab user account will be only 
available if and only if the user confirm the code that he receives by email after the 
introduction of the corresponding data in a portal. In this way we also prevent possible 
attacks in the creation of email accounts, due to we wait confirmation of the email 
before starting the automatic process of the new user creation.

In order to resolve these requirements, we created a specific [Google Form](https://docs.google.com/forms/d/e/1FAIpQLSfIz2JxJ8zwytwYG9CJpauYPaOkiJEs88SMqBul9x1UWdzh3w/viewform)
with the corresponding Google Spreadsheet and the [Google script code](scripts/README.md)
to cover those requirements.

Although, all the process is almost automatic, there is a special step that is made 
manually. This one is the review of the confirmation email. We decided to do it manually 
due to prevent the automatic user generation account. It that way, at administrator have 
to validate the reception of the request and confirm that the new user has sent the 
corresponding email. After this operation, the administrator will create a specific JIRA 
ticket in our ticketing system with the corresponding information to create the new user 
and assign it to the corresponding FIWARE Lad node administrator in order to create it.

Once that the administrator has confirmed the reception of the email and the creation of 
the corresponding ticket in JIRA, the automatic user creation service start to work. This 
service periodically wake up and see if there is a confirmed email in the Google Spreadsheet 
whose ticket in JIRA is still open. In that case, it means that the user was not created 
and proceed with the creation of the user in the OpenStack Keystone service.

[Top](#top)

## Build and Install

### Requirements

The following software must be installed:

- Python 2.7
- pip
- virtualenv


### Installation

The recommend installation method is using a virtualenv. Actually, the installation
process is only about the python dependencies, because the python code do not need
installation.

1. Clone this repository.
2. Define the configuration file in './config/user-create.ini'
3. Create your Google Credential in the './config/user-credential.json' file.
4. Create your Google service account key in the './config' directory
6. Execute the script 'source config.sh'.
7. With root user, execute the command 'cp ./config/user-create.logrotate /etc/logrotate.d/user-create

[Top](#top)

## Running

Once that you have installed and configured your application, you can run it just 
executing:

    $ python user-create.py

And it will be executed in order to create the corresponding account. Keep in mind 
that you have to be inside a previously defined virtual environment.

The ``config.sh`` file that you can find in the [deploy](deploy) folder is used in 
order to allow the automatic execution of the python script just adding the corresponding 
header to the file:

    #!/usr/bin/env /env/bin/python

Where env is the name of your virtual environment. 

Last but not least, the service is added into the [crontab](https://manpages.debian.org/jessie/cron/crontab.5.en.html) 
service of the machine in order to execute the service each 30 minutes to check if a 
new account is needed to be created.

[Top](#top)

## Deployment

There is a specific option to deploy this service in a host. Take a look to the content
of [deploy](deploy/README.md) directory

[Top](#top)

## Testing

### Unit Tests

It was defined a minimum set of tests to cover the core functionality of the service. 
The ``tests`` target is used for running the unit tests in the component. We use for 
those tests the tox tool. [Tox](https://tox.readthedocs.io/en/latest/) is a generic 
[virtualenv](https://pypi.python.org/pypi/virtualenv) management and test command 
line tool you can use for checking your package installs correctly with different 
Python versions and interpreters running your tests in each of the environments, 
configuring your test tool of choice acting as a frontend to Continuous Integration 
servers, greatly reducing boilerplate and merging CI and shell-based testing.

The configuration file can be found in ``tox.ini`` in which we have defined two 
different environments:
* The first one, to test the service using [nosetests](http://nose.readthedocs.io/en/latest/).
* The second one, to check the python coding style using [pycodestyle](https://pycodestyle.readthedocs.io/en/latest/)

First of all, you need to install the tool with the following commands:

    $ pip install tox

Now, you can run the tests, simply execute the commands:

    $ tox


[Top](#top)

## Support

The support of this service is under github. You can create your [issues](https://github.com/flopezag/fiware-user-creation/issues/new)
and they will be resolved by the development team in the following sprint.

[Top](#top)

## License

\(c) 2017 FIWARE Foundation, e.V., Apache License 2.0

[Top](#top)

