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

import smtplib
from email.mime.text import MIMEText
from jinja2 import Template
from kernel.log import logger
from config.settings import MAIL_HOST, MSG_FROM, FIRST_DEFAULT_MSG_TO, SECOND_DEFAULT_MSG_TO


__author__ = 'José Ignacio Carretero'


class Mailer:
    subject = "Your FIWARE Lab account has been created"
    msg_from = MSG_FROM
    mail_host = MAIL_HOST
    message_text = """
    Your account  in FIWARE Lab -- https://cloud.lab.fiware.org -- has been created

    Username: {{to}}
    Password: {{password}}

    Please, change your password in your 1st access. You can send your questions to  fiware-lab-help@lists.fi-ware.org

    Best Regards,
    FIWARE Lab Team
    """

    def __init__(self):
        pass

    def send(self, to, password):
        template = Template(Mailer.message_text)
        msg = MIMEText(template.render(to=to, password=password))
        msg['Subject'] = Mailer.subject
        msg['From'] = Mailer.msg_from
        msg['To'] = to
        try:
            s = smtplib.SMTP(Mailer.mail_host)
            s.sendmail(Mailer.msg_from,
                       [to, FIRST_DEFAULT_MSG_TO, SECOND_DEFAULT_MSG_TO], msg.as_string())

            s.quit()
            logger.info("Sent mail to %s" % to)
        except Exception:
            logger.warning("Problem sending email to %s" % to)


if __name__ == "__main__":
    Mailer().send(FIRST_DEFAULT_MSG_TO, "passw0rd")
