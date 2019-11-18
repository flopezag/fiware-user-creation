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

from re import compile
from kernel.google import get_service
from kernel.keystoneUsers import TrialUser
from kernel.log import logger

__author__ = 'Fernando López'


class CreateOps(object):
    def __init__(self, jira_server):
        self.jira_server = jira_server

    @staticmethod
    def get_spreadsheet_data(id_sheet):
        service = get_service('sheets')

        range_data = 'Confirmation!A2:F'
        result_data = service.spreadsheets().values().get(spreadsheetId=id_sheet, range=range_data).execute()
        values = result_data.get('values', [])

        filter_values = CreateOps.filter_google_sheet(data=values)

        return filter_values

    @staticmethod
    def filter_google_sheet(data):
        aux = list(map(lambda x: [x[1], x[2], x[3], x[5]], data))

        aux1 = list(filter(lambda x: x[len(x) - 1] == u'1', aux))

        filter_values = list(map(lambda x: [x[0], x[1], x[2]], aux1))

        return filter_values

    @staticmethod
    def get_jira_data(issues_in_project):
        issue_list = []

        pattern = r".*:[ ]*(.*)"
        compiled_re = compile(pattern)

        for issue in issues_in_project:
            # temp = map(lambda x: compiled_re.search(x).group(1), issue.fields.description.split('\r\n'))
            temp = CreateOps.extract_description_info(compiled_re=compiled_re, description=issue.fields.description)

            issue_list.append([issue.key, temp])

        return issue_list

    @staticmethod
    def extract_description_info(compiled_re, description):
        result = list(map(lambda x: compiled_re.search(x).group(1), description.split('\r\n')))

        return result

    @staticmethod
    def filter_lists(list1, list2):
        result_data = list()

        for aux in list2:
            value = aux[1]
            temp = list(filter(lambda x: x == value, list1))

            if temp:
                result_data.append([aux[0], temp[0]])

        return result_data

    def create_user(self, element):
        issue_ticket = element[0]

        issue_data = element[1]

        logger.info("Detected a ticket ({}) with an user ({}) and a region ({}) to be resolved"
                    .format(issue_ticket, issue_data[1], issue_data[2]))

        TrialUser(issue_data[1], issue_data[2]).new_user()

        self.jira_server.close_jira_ticket(issue_ticket)
