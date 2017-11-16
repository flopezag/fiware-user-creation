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

import re

from jira import JIRA

from config.settings import SHEET_ID, JIRA_USER, JIRA_PASSWORD
from kernel.google import get_service
from kernel.log import logger

__author__ = 'Fernando López'


def get_spreadsheet_data(id_sheet):
    service = get_service('sheets')

    range_data = 'Confirmation!A2:F'
    result_data = service.spreadsheets().values().get(spreadsheetId=id_sheet, range=range_data).execute()
    values = result_data.get('values', [])

    aux = map(lambda x: [x[1], x[2], x[3], x[5]], values)

    aux1 = filter(lambda x: x[len(x) - 1] == u'1', aux)

    filter_values = map(lambda x: [x[0], x[1], x[2]], aux1)

    return filter_values


def get_jira_data():
    options = {
        'server': 'https://jira.fiware.org'
    }

    jira = JIRA(options, basic_auth=(JIRA_USER, JIRA_PASSWORD))

    issues_in_project = \
        jira.search_issues('project = LAB AND resolution = Unresolved AND component = "FIWARE LAB USER CREATION"')

    issue_list = []

    pattern = r".*:[ ]*(.*)"
    compiled_re = re.compile(pattern)

    for issue in issues_in_project:
        temp = map(lambda x: compiled_re.search(x).group(1), issue.fields.description.split('\r\n'))

        issue_list.append([issue.key, temp])

    return issue_list


def filter_lists(list1, list2):
    result_data = list()

    for aux in list2:
        value = aux[1]
        temp = filter(lambda x: x == value, list1)

        if temp:
            result_data.append([aux[0], temp])

    return result_data


if __name__ == "__main__":
    logger.info(SHEET_ID)

    filtered_sheet_data = get_spreadsheet_data(SHEET_ID)
    filtered_jira_data = get_jira_data()

    result = filter_lists(list1=filtered_sheet_data, list2=filtered_jira_data)

    print(result)
