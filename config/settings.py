#!/usr/bin/env python
# -*- encoding: utf-8 -*-
##
# Copyright 2017 FIWARE Foundation, e.V.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
##

from configparser import ConfigParser
import logging
from os import environ
from os.path import dirname, join, abspath

__author__ = 'Fernando López'

__version__ = '1.2.0'


"""
Default configuration.

The configuration `cfg_defaults` are loaded from `cfg_filename`, if file exists in
/etc/fiware.d/user-create.ini

Optionally, user can specify the file location manually using an Environment variable
called USER_CREATE_SETTINGS_FILE.
"""

name = 'user-create'

cfg_dir = "/etc/fiware.d"

cfg_filename = environ.get("USER_CREATE_SETTINGS_FILE")
if cfg_filename:
    cfg_dir = dirname(cfg_filename)
else:
    cfg_filename = join(cfg_dir, '%s.ini' % name)

Config = ConfigParser()

Config.read(cfg_filename)


def config_section_map(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                print("skip: %s" % option)
        except Exception:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1


def check_log_level(loglevel):
    numeric_level = getattr(logging, loglevel.upper(), None)

    if not isinstance(numeric_level, int):
        print('Invalid log level: {}'.format(loglevel))
        exit()

    return numeric_level


if Config.sections():
    # Data from Google section
    google_section = config_section_map("google")

    USER_CREDENTIAL = join(cfg_dir, google_section['usercredential'])
    SHEET_ID = google_section['sheetid']
    SERVICE_ACCOUNT_KEY = google_section['serviceaccountkey']
    GOOGLE_CREDENTIAL = google_section['googlecredential']

    # Log section
    log_section = config_section_map("log")

    LOG_LEVEL = check_log_level(log_section['loglevel'])

    # JIRA section
    jira_section = config_section_map("jira")

    JIRA_USER = jira_section['user']
    JIRA_PASSWORD = jira_section['password']
    JIRA_SERVER = jira_section['server']

    # OpenStack section
    openstack_section = config_section_map("openstack")

    OS_AUTH_URL = openstack_section['os_auth_url']
    OS_USERNAME = openstack_section['os_username']
    OS_PASSWORD = openstack_section['os_password']
    OS_PROJECT_NAME = openstack_section['os_project_name']
    OS_USER_DOMAIN_ID = openstack_section['os_user_domain_id']
    OS_PROJECT_ID = openstack_section['os_project_id']
    OS_PROJECT_DOMAIN_ID = openstack_section['os_project_domain_id']

    # Mailer section
    mailer_section = config_section_map("mailer")

    MAIL_HOST = mailer_section['mail_host']
    MSG_FROM = mailer_section['msg_from']
    FIRST_DEFAULT_MSG_TO = mailer_section['first_default_msg_to']
    SECOND_DEFAULT_MSG_TO = mailer_section['second_default_msg_to']

else:
    msg = '\nERROR: There is not defined USER_CREATE_SETTINGS_FILE environment variable ' \
          '\n       pointing to configuration file or there is no user-create.ini file' \
          '\n       in the /etd/init.d directory.' \
          '\n\n       Please correct at least one of them to execute the program.'
    exit(msg)

# Settings file is inside Basics directory, therefore I have to go back to the parent directory
# to have the Code Home directory
CODE_HOME = dirname(dirname(abspath(__file__)))
LOG_HOME = join(CODE_HOME, 'logs')
SERVICE_ACCOUNT_KEY_HOME = join(CODE_HOME, 'config')
