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

from config.settings import SHEET_ID, JIRA_USER, JIRA_PASSWORD
from config.log import logger
from kernel.google import get_service
import re
from jira import JIRA

__author__ = 'Fernando López'


def get_values(alist):
    temp = list()

    temp.append(alist[1])
    temp.append(alist[2])
    temp.append(alist[3])
    temp.append(alist[5])

    return temp


def get_spreadsheet_data(id):
    service = get_service('sheets')

    rangeName = 'Confirmation!A2:F'
    result = service.spreadsheets().values().get(spreadsheetId=id, range=rangeName).execute()
    values = result.get('values', [])

    # filter_values = [get_values2(c) for c in values]

    aux = map(get_values, values)

    filter_values = filter(lambda x: x[len(x) - 1] == u'1', aux)

    return filter_values


def get_jira_data():
    options = {
        'server': 'https://jira.fiware.org'
    }

    jira = JIRA(options, basic_auth=(JIRA_USER, JIRA_PASSWORD))

    issues_in_proj = \
        jira.search_issues('project = LAB AND resolution = Unresolved AND component = "FIWARE LAB USER CREATION"')

    issue_list = []

    pattern = r".*:[ ]*(.*)"
    compiled_re = re.compile(pattern)

    for issue in issues_in_proj:
        temp = map(lambda x: compiled_re.search(x).group(1), issue.fields.description.split('\r\n'))

        issue_list.append(temp)

    return issue_list


if __name__ == "__main__":
    logger.info(SHEET_ID)

    filtered_sheet_data = get_spreadsheet_data(SHEET_ID)
    filtered_jira_data = get_jira_data()

    print(len(filtered_sheet_data))
    print(filtered_sheet_data)

    print(len(filtered_jira_data))
    print(filtered_jira_data)
