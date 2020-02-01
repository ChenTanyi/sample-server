#!/usr/bin/env python3
import requests

import smtplib

from email.message import EmailMessage

sender = 'from@from.com'
receivers = ['to@to.com']

msg = EmailMessage()
msg['Subject'] = "Html"
msg['From'] = sender
msg['To'] = receivers

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = """\
<html>
  <head></head>
  <body>
    <p>Hi!<br>
       How are you?<br>
       Here is the <a href="http://www.python.org">link</a> you wanted.
    </p>
  </body>
</html>
"""

msg.set_content(text)
msg.add_alternative(html, subtype = 'html')

target = '127.0.0.1:9999'
host, port = target.split(':')[:2]

smtpObj = smtplib.SMTP(host = host, port = port)
smtpObj.sendmail(sender, receivers, msg.as_string())
print("Successfully sent email")
