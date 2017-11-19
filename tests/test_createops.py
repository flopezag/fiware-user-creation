# -*- encoding: utf-8 -*-
#
# Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
#
# This file is part of FI-WARE project.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#
# You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For those usages not covered by the Apache version 2.0 License please
# contact with opensource@tid.es
#

from unittest import TestCase
from kernel.createops import CreateOps
import re

__author__ = 'fla'

""" Class to test the interaction with redis
"""


class TestCreateOps(TestCase):
    def testFilterGoogleSheetMix(self):
        initial_value = [[u'08/11/2017 19:57:52', u'Juyyyy Uyyyy Foooo', u'jufoo.fffoooo@gmail.com', u'SaoPaulo',
                          u'1w0zkcHMFayk0wiYfdXyX2VhawoHNlnsU8DODXfdTiksOLCi', u'1'],
                         [u'09/11/2017 11:28:00', u'Wang Win Win', u'www@gmail.com', u'Spain2',
                          u'pzHX4B5jLfKyvy3xbDsHQB8230hF8P2kLbikZMDsPNRg3Ln5', u'1'],
                         [u'09/11/2017 12:55:33', u'Will Smith', u'wsmith@kepa.org', u'Spain2',
                          u'CH16cvkZTgJwtZOsv8cUNTmiiZ22fRFzWf4dHDEf0xORZ5wR', u'0'],
                         [u'09/11/2017 15:57:34', u'William Gill', u'wgil@foo.foo', u'Senegal',
                          u'wFLMy42bPG2n0hnIFcYQsQLVr8qweWCc8IOP8LuUSeUmt0PQ', u'0'],
                         [u'10/11/2017 10:41:43', u'Mauro Marin', u'mmarin@guerrilla.mail',
                          u'Lannion', u'Zs7568zrNJZRvVcpYztxZkacddKSthsepi8ZLOf6ujdgUIz4', u'1'],
                         [u'16/11/2017 12:44:36', u'caterina2', u'caterina2.tormo@ite.es',
                          u'Spain22', u'------', u'1'],
                         [u'16/11/2017 12:44:36', u'caterina3', u'caterina3.tormo@ite.es',
                          u'Spain2233', u'------', u'1'],
                         [u'17/11/2017 10:45:16', u'H\xe9ctor Porta Albentosa', u'1smrt.hporta@gmail.com',
                          u'Spain2', u'pZwf5NtzxFmV8MPZ3KjbAFxCV7nbMl4DtJrdHA8F8OcKEN9k', u'0'],
                         [u'17/11/2017 12:40:44', u'Ciprian', u'ciprian.biscovan@energobit.com', u'Budapest3',
                          u'QUe8eqjo4kxk5DM1iSjvbMunA3gUuQkFEvaSIaDyU8nNCwny', u'0']]

        expected_value = [[u'Juyyyy Uyyyy Foooo', u'jufoo.fffoooo@gmail.com', u'SaoPaulo'],
                          [u'Wang Win Win', u'www@gmail.com', u'Spain2'],
                          [u'Mauro Marin', u'mmarin@guerrilla.mail', u'Lannion'],
                          [u'caterina2', u'caterina2.tormo@ite.es', u'Spain22'],
                          [u'caterina3', u'caterina3.tormo@ite.es', u'Spain2233']]

        result = CreateOps.filter_google_sheet(initial_value)

        self.assertEqual(expected_value, result)

    def testExtractDescriptionInfo(self):
        initial_value = u'User name: Alberto Albertini\r\nemail: alberto_albertini@party.com\r\nregion: Spain2'

        expected_value = [u'Alberto Albertini', u'alberto_albertini@party.com', u'Spain2']

        pattern = r".*:[ ]*(.*)"
        compiled_re = re.compile(pattern)

        result = CreateOps.extract_description_info(compiled_re, initial_value)

        self.assertEqual(expected_value, result)
