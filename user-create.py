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

from config.settings import SHEET_ID
from kernel.log import logger
from kernel.jiraconnector import MyJiraConnector
from kernel.createops import CreateOps

__author__ = 'Fernando López'

if __name__ == "__main__":
    jira = MyJiraConnector()
    create_ops = CreateOps(jira_server=jira)

    logger.info(SHEET_ID)

    filtered_sheet_data = CreateOps.get_spreadsheet_data(SHEET_ID)
    filtered_jira_data = CreateOps.get_jira_data(jira.get_data())

    result = CreateOps.filter_lists(list1=filtered_sheet_data, list2=filtered_jira_data)

    list(map(create_ops.create_user, result))
