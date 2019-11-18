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
import logging
from os.path import join, exists
from os import makedirs
from config.settings import LOG_HOME, LOG_LEVEL
from config.constants import LOG_FILE

__author__ = 'Fernando López'


filename = join(LOG_HOME, LOG_FILE)

if not exists(LOG_HOME):
    makedirs(LOG_HOME)

logging.basicConfig(filename=filename,
                    format='%(asctime)s|%(levelname)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=LOG_LEVEL)

logger = logging.getLogger(__name__)
