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

from os.path import join, exists
from os import makedirs
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

from config.constants import APPLICATION_NAME, CREDENTIAL_DIR
from config.settings import USER_CREDENTIAL, GOOGLE_CREDENTIAL, SERVICE_ACCOUNT_KEY, SERVICE_ACCOUNT_KEY_HOME, CODE_HOME
from kernel.log import logger

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

__author__ = 'Fernando López'


def get_credentials(api):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    :param api:
        api - API from which we want to obtain the credentials.

    :return:
        Credentials, the obtained credential.
    """
    logger.info("Get Google credential for API {}".format(api))

    # If modifying these scopes, delete your previously saved credentials
    # at ./.credentials/sheets.googleapis.com.json
    scope = {'sheets': 'https://www.googleapis.com/auth/spreadsheets',
             'analytics': 'https://www.googleapis.com/auth/analytics.readonly',
             'analyticsreporting': 'https://www.googleapis.com/auth/analytics.readonly'}

    credential_folder = join(CODE_HOME, CREDENTIAL_DIR)
    logger.debug("Credential dir: {}".format(credential_folder))

    if not exists(credential_folder):
        try:
            makedirs(credential_folder)
        except OSError as error:
            logger.error("Unable to create the corresponding directory: {}".format(error))

    credential_path = join(credential_folder, GOOGLE_CREDENTIAL)

    if api == 'sheets':
        store = Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(USER_CREDENTIAL, scope[api])
            flow.user_agent = APPLICATION_NAME

            credentials = tools.run_flow(flow, store, flags)
    else:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            join(SERVICE_ACCOUNT_KEY_HOME, SERVICE_ACCOUNT_KEY),
            scopes=scope[api])

    return credentials


def get_service(api_name):
    logger.info("Get Google service for API {}".format(api_name))

    service = {'sheets': 'v4', 'analytics': 'v3', 'analyticsreporting': 'v4'}
    discovery_service_url = {
        'sheets': 'https://sheets.googleapis.com/$discovery/rest?version=v4',
        'analytics': 'none',
        'analyticsreporting': 'https://analyticsreporting.googleapis.com/$discovery/rest'
    }

    try:
        credentials = get_credentials(api=api_name)

    except ValueError:
        raise
    else:
        http_auth = credentials.authorize(Http())

        if api_name is 'analytics':
            result = build(serviceName=api_name,
                           version=service[api_name],
                           http=http_auth,
                           cache_discovery=False)
        else:
            result = build(serviceName=api_name,
                           version=service[api_name],
                           http=http_auth,
                           discoveryServiceUrl=discovery_service_url[api_name],
                           cache_discovery=False)

        return result
