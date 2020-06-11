#!/usr/bin/env python3
# vim: set fileencoding=utf-8 tw=0:

from __future__ import print_function

import asyncore
import base64
import json
import os
import re
import sys
from smtpd import SMTPServer
import mailparser
from xml.sax.saxutils import escape
import requests
import tempfile


API_KEY = os.getenv('EXPERTSENDER_API_KEY')

API_URL = os.getenv('EXPERTSENDER_API_URL', 'https://api3.esv2.com/v2/Api/SystemTransactionals/6')

DUMP_FOLDER = os.getenv('EXPERTSENDER_DUMP_FOLDER', '/var/www/cache/mailwarm')


class Bridge(SMTPServer):
    def process_message(self, peer, sender, recipients, body, mail_options=None, rcpt_options=None):
        """
        Handle incoming message.

        :param tuple peer: Connecting client's IP and port number.
        :param string sender: Sender email address.
        :param string recipients: List or recipient email addresses.
        :param string data: Message body with headers.
        :param list mail_options: Unused.
        :param list rcpt_options: Unused.
        :return: Nothing.
        :rtype: None
        """
        try:
            mail = mailparser.parse_from_bytes(body)
            if DUMP_FOLDER:
                self.dump(mail)
            if API_KEY is not None:
                self.forward(mail)
        except Exception as e:
            return '554 Transaction failed: %s' % e

    def forward(self, mail):
        """
        Send the message to expertsender.
        """
        xml = XML(mail).to_string()

        url = API_URL

        print('Request URL: %s' % url)
        print('Payload: %s' % xml)

        response = requests.request('POST', url, data=xml.encode('utf-8'), headers={
            'content-type': 'text/xml',
        })

        print('Response: %d: %s' % (response.status_code, response.text))

        if response.status_code >= 200 and response.status_code < 300:
            return

        raise RuntimeError(self.get_error_message(response.text))

    def dump(self, mail):
        data = {
            'from': None,
            'to': [],
            'subject': None,
            'text_body': None,
            'html_body': None,
            'files': [],
        }

        data['from'] = {
            'name': mail.from_[0][0],
            'address': mail.from_[0][1],
        }

        for recipient in mail.to:
            data['to'].append({
                'name': recipient[0],
                'address': recipient[1],
            })

        data['subject'] = mail.subject
        data['text_body'] = mail.text_plain[0] if mail.text_plain else None
        data['html_body'] = mail.text_html[0] if mail.text_html else None

        if mail.attachments:
            for att in mail.attachments:
                data['files'].append({
                    'name': att['filename'],
                    'type': att['mail_content_type'],
                    'body': base64.b64encode(att['payload'].encode()).decode('utf-8'),
                })

        tmp = tempfile.mkstemp(suffix='.json', prefix='mail_', dir=DUMP_FOLDER)
        with os.fdopen(tmp[0], 'w') as f:
            f.write(json.dumps(data))

        print(json.dumps(data))

    def get_error_message(self, xml):
        m = re.search(r'<Message>(.+?)</Message>', xml)
        if m is not None:
            return m.group(1)
        else:
            return 'unknown error'


class XML(object):
    def __init__(self, msg):
        self.msg = msg

    def to_string(self):
        xml = '<?xml version="1.0" encoding="utf-8"?>'
        xml += '<ApiRequest xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xs="http://www.w3.org/2001/XMLSchema">'
        xml += '<ApiKey>%s</ApiKey>' % API_KEY
        xml += '<Data>'
        xml += '<ReturnGuid>true</ReturnGuid>'
        xml += self.add_receivers()
        xml += self.add_snippets()
        xml += '</Data></ApiRequest>'
        return xml

    def add_receivers(self):
        xml = ''
        for recipient in self.msg.to:
            xml += '<Receiver>'
            if recipient[0]:
                xml += '<Name>%s</Name>' % escape(recipient[0])
            if recipient[1]:
                xml += '<Email>%s</Email>' % escape(recipient[1])
            xml += '</Receiver>'
            print('to = %s' % recipient[1])
        return xml

    def add_snippets(self):
        xml = '<Snippets>'
        xml += self.add_from_snippet()
        xml += self.add_subject_snippet()
        xml += self.add_text_snippet()
        xml += self.add_html_snippet()
        xml += '</Snippets>'
        xml += self.add_files()
        return xml

    def add_from_snippet(self):
        xml = self.add_snippet('from_name', self.msg.from_[0][0])
        xml += self.add_snippet('from_email', self.msg.from_[0][1])
        print('from = %s' % self.msg.from_[0][1])
        return xml

    def add_subject_snippet(self):
        print('subject = %s' % self.msg.subject)
        return self.add_snippet('subject', self.msg.subject)

    def add_text_snippet(self):
        if self.msg.text_plain:
            return self.add_snippet('plain_text', self.msg.text_plain[0])

    def add_html_snippet(self):
        if self.msg.text_html:
            return self.add_snippet('template', self.msg.text_html[0])

    def add_snippet(self, name, value):
        xml = '<Snippet>'
        xml += '<Name>%s</Name>' % escape(name)
        xml += '<Value>%s</Value>' % escape(value)
        xml += '</Snippet>'
        return xml

    def add_files(self):
        xml = ''

        if self.msg.attachments:
            for att in self.msg.attachments:
                xml += '<Attachment>'
                xml += '<FileName>%s</FileName>' % escape(att['filename'])
                xml += '<MimeType>%s</MimeType>' % escape(att['mail_content_type'])
                xml += '<Content>%s</Content>' % base64.b64encode(att['payload'].encode()).decode('utf-8')
                xml += '</Attachment>'

            xml = '<Attachments>%s</Attachments>' % xml

        return xml


bridge = Bridge(('0.0.0.0', 1025), None)
print('Waiting for messages on *:1025')

if API_KEY is not None:
    print('Using expertsender API key %s' % API_KEY)
    print('API base url is %s' % API_URL)

if DUMP_FOLDER is not None:
    print('Dumping messages to folder %s' % DUMP_FOLDER)

if API_KEY is None and DUMP_FOLDER is None:
    print('Please set either EXPERTSENDER_API_KEY or EXPERTSENDER_DUMP_FOLDER envar.', file=sys.stderr)
    exit(1)

asyncore.loop()
