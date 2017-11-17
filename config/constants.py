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

__author__ = 'Fernando López'

GOOGLE_ACCOUNTS_BASE_URL = 'https://accounts.google.com'
APPLICATION_NAME = 'FIWARE Lab User Create'
CREDENTIAL_DIR = '.credentials'
LOG_FILE = 'user-create.log'

# JIRA Transactions
START_PROGRESS = 'Start Progress'
FINISH = 'Finish'
TRANSACTION_ID_FIELD_NAME = 'id'
TRANSACTION_NAME_FIELD_NAME = 'name'

# JIRA Query
JIRA_QUERY = 'project = LAB AND resolution = Unresolved AND component = "FIWARE LAB USER CREATION"'
