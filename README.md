# Mailwarm to ExpertSender gateway

Reads incoming messages using SMTP, translates to the REST API.


## Running

Preferred way:

```
$ docker run --rm -p 1025:1025/tcp --name mailwarm-bridge -v /var/www/ersties.com/live:/var/www ersties/mailwarm-bridge
```

That's all.  The SMTP server is available on TCP port 1025.  Files would be stored in `/var/www/ersties.com/live/cache/mailwarm`.


## Testing

Success:

```
$ python3 src/test.py hex@umonkey.net
Message sent.
```

Invalid email address:

```
$ python3 src/test.py foobar@com
Traceback (most recent call last):
  File "src/test.py", line 37, in <module>
    s.sendmail(FROM, TO, msg.as_string().encode('utf-8'))
  File "/usr/lib/python3.8/smtplib.py", line 892, in sendmail
    raise SMTPDataError(code, resp)
smtplib.SMTPDataError: (554, b'Transaction failed: foobar@com: Subscriber email is invalid.')
```
