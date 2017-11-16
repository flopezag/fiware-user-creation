# fiware-user-creation
[![License badge](https://img.shields.io/badge/license-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Script to create automatically FIWARE Lab users taking the information from

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
