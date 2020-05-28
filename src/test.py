#!/usr/bin/env python3
# vim: set fileencoding=utf-8 tw=0:

import os
import smtplib
import sys

from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SERVER = ('127.0.0.1', 1025)

FROM = 'alice@example.com'

TO = sys.argv[1] if len(sys.argv) > 1 else 'bob@example.com'

text = "You're next."

html = "<html><body><p>You're next, Bob.</p></body></html>"

msg = MIMEMultipart('alternative')
msg['Subject'] = 'Hello bob, ага.'
msg['From'] = 'Алиса <%s>' % FROM
msg['To'] = '%s (Bob)' % TO

msg.attach(MIMEText(text, 'plain'))
msg.attach(MIMEText(html, 'html'))

with open(__file__, 'rb') as f:
    att = MIMEBase('text', 'x-python')
    att.set_payload(f.read())
    att['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(__file__)
    msg.attach(att)

s = smtplib.SMTP(SERVER[0], SERVER[1])
s.sendmail(FROM, TO, msg.as_string().encode('utf-8'))
s.quit()

print('Message sent.')
