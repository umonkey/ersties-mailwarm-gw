#!/usr/bin/env python3
# vim: set fileencoding=utf-8 tw=0:

import asyncore
import base64
import os
from smtpd import SMTPServer
import mailparser
from xml.sax.saxutils import escape
import requests


API_KEY = os.getenv('EXPERTSENDER_API_KEY', 'foobar')

API_URL = os.getenv('EXPERTSENDER_API_URL', 'https://api3.esv2.com/v2/Api/SystemTransactionals/6')


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
        mail = mailparser.parse_from_bytes(body)
        self.forward(mail)

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

        return xml


bridge = Bridge(('0.0.0.0', 1025), None)
print('Waiting for messages on *:1025, using api key %s' % API_KEY)
asyncore.loop()
