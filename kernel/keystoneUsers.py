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

from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client
from keystoneauth1.exceptions.http import NotFound
from config.settings import OS_AUTH_URL, OS_USERNAME, OS_PASSWORD, OS_PROJECT_NAME, \
    OS_USER_DOMAIN_ID, OS_PROJECT_DOMAIN_ID, OS_PROJECT_ID
from datetime import datetime
from kernel.mailer import Mailer
from kernel.log import logger
from os import environ
from string import ascii_lowercase, digits
from random import choice
from sys import argv


__author__ = 'José Ignacio Carretero'


class KeystoneConfig:
    def __init__(self):
        d = {"auth_url": environ.get('OS_AUTH_URL'),
             "username": environ.get('OS_USERNAME'),
             "password": environ.get('OS_PASSWORD'),
             "project_name": environ.get('OS_PROJECT_NAME'),
             "user_domain_id": environ.get('OS_USER_DOMAIN_ID'),
             "project_id": environ.get('OS_PROJECT_ID'),
             "project_domain_id": environ.get('OS_PROJECT_DOMAIN_ID')}
        self.__dict__.update(d)


class KeystoneUsers:
    def __init__(self, config=None):
        if config is None:
            config = KeystoneConfig()

        self.auth_url = config['auth_url']
        self.username = config['username']
        self.password = config['password']
        self.project_name = config['project_name']
        self.user_domain_id = config['user_domain_id']
        self.project_domain_id = config['project_domain_id']
        self.project_id = config['project_id']

        self.__connect_keystone_lib__()

        logger.info("KeystoneUsers created")

    def __connect_keystone_lib__(self):
        self.auth = v3.Password(auth_url=self.auth_url, username=self.username,
                                password=self.password, project_name=self.project_name,
                                user_domain_id=self.user_domain_id, project_domain_id=self.project_domain_id,
                                project_id=self.project_id)

        self.session = session.Session(auth=self.auth)
        self.keystone = client.Client(session=self.session)

    @staticmethod
    def __get_resource__(manager, resource_name_or_id):
        result = None
        try:
            result = manager.get(resource_name_or_id)
        except NotFound:
            try:
                result = manager.find(name=resource_name_or_id)
            except NotFound:
                pass
        return result

    def get_user(self, user_id_or_name):
        return self.__get_resource__(self.keystone.users, user_id_or_name)

    def get_project(self, project_id_or_name):
        return self.__get_resource__(self.keystone.projects, project_id_or_name)

    def get_role(self, role_id_or_name):
        return self.__get_resource__(self.keystone.roles, role_id_or_name)

    def create_project(self, name, description):
        return self.keystone.projects.create(name=name, description=description,
                                             enabled=True, domain=self.project_domain_id)

    def create_user(self, name, project, password):
        description = name + ' cloud user'
        email = name
        trial_started_at = datetime.now().strftime("%Y-%m-%d")
        trial_duration = '15'

        return self.keystone.users.create(name, domain=self.user_domain_id, project=project, password=password,
                                          description=description, enabled=True, email=email,
                                          cloud_project_id=project,
                                          trial_duration=trial_duration, trial_started_at=trial_started_at)

    def get_role_assignments_for_project(self, project_id):
        return self.keystone.role_assignments.list(project=project_id)

    def get_role_assignments_for_user(self, user_id):
        return self.keystone.role_assignments.list(user=user_id)

    def set_role_assignments_for_user(self, user_id):
        user = self.get_user(user_id)
        member_role = self.get_role("member")
        trial_role = self.get_role("trial")
        self.keystone.roles.grant(role=trial_role.id, user=user_id, domain=self.project_domain_id)
        self.keystone.roles.grant(role=member_role.id, user=user_id, project=user.cloud_project_id)

    def get_endpoint_group_for_region(self, region_name):
        endpoint_groups = self.keystone.endpoint_groups.list()
        return [x for x in endpoint_groups if 'region_id' in x.filters and x.filters['region_id'] == region_name]

    def add_user_to_region(self, user_data, region_name):
        endpoint_groups = self.get_endpoint_group_for_region(region_name)
        for endpoint_group in endpoint_groups:
            project_id = user_data.cloud_project_id
            self.keystone.endpoint_filter.add_endpoint_group_to_project(endpoint_group.id, project_id)


class TrialUser:
    def __init__(self, trial_user_name, trial_region):
        self.user_name = trial_user_name
        self.region = trial_region
        self.password = ''.join([choice(ascii_lowercase + digits) for _ in range(20)])

    def new_user(self):
        user_data = self.__create_user__()
        if user_data is not None:
            self.__send_mail__()
        return user_data

    def __create_user__(self):
        config_data = {
            "auth_url": OS_AUTH_URL,
            "username": OS_USERNAME,
            "password": OS_PASSWORD,
            "project_name": OS_PROJECT_NAME,
            "user_domain_id": OS_USER_DOMAIN_ID,
            "project_id": OS_PROJECT_ID,
            "project_domain_id": OS_PROJECT_DOMAIN_ID
        }

        keystone_users = KeystoneUsers(config=config_data)

        existing_user = keystone_users.get_user(self.user_name)

        if existing_user is not None:
            logger.warn("USER ALREADY EXISTS!!")
            return None

        region_filters = keystone_users.get_endpoint_group_for_region(self.region)
        if len(region_filters) == 0:
            logger.warn("NO FILTERS FOR REGION " + self.region)
            return None

        project_name = self.user_name + " cloud"
        project_data = keystone_users.create_project(project_name, 'Generated project')
        user_data = keystone_users.create_user(self.user_name, project_data.id, self.password)
        keystone_users.set_role_assignments_for_user(user_data.id)
        keystone_users.add_user_to_region(user_data, self.region)

        logger.info("user %s created in region %s" % (self.user_name, self.region))
        return user_data

    def __send_mail__(self):
        mailer = Mailer()
        mailer.send(self.user_name, self.password)


if __name__ == "__main__":
    if len(argv) != 3:
        user_name = input("User name: ")
        region = input("Region: ")
    else:
        user_name = argv[1]
        region = argv[2]

    TrialUser(user_name, region).new_user()
