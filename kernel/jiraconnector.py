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

from jira import JIRA
from config.settings import JIRA_SERVER, JIRA_USER, JIRA_PASSWORD
from config.constants import START_PROGRESS, FINISH, TRANSACTION_ID_FIELD_NAME, TRANSACTION_NAME_FIELD_NAME, JIRA_QUERY

__author__ = 'Fernando López'


class MyJiraConnector(object):
    def __init__(self):
        options = {
            'server': JIRA_SERVER
        }

        self.jira = JIRA(options, basic_auth=(JIRA_USER, JIRA_PASSWORD))

    def get_data(self):
        issues_in_project = self.jira.search_issues(JIRA_QUERY)

        return issues_in_project

    def close_jira_ticket(self, issue_ticket):
        issue = self.jira.issue(issue_ticket)

        # Note:
        # Only the transitions available to the currently authenticated user will be returned!
        transitions = self.jira.transitions(issue)

        transition_id = self.__search_list_tuples(transitions, START_PROGRESS)
        self.jira.transition_issue(issue, transition_id)

        transitions = self.jira.transitions(issue)

        transition_id = self.__search_list_tuples(transitions, FINISH)
        self.jira.transition_issue(issue, transition_id)

    @staticmethod
    def __search_list_tuples(list_tuples, name):
        aux = [item[TRANSACTION_ID_FIELD_NAME] for item in list_tuples if item[TRANSACTION_NAME_FIELD_NAME] == name]

        return aux[0]
