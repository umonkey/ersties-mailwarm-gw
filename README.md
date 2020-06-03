# Mailwarm to ExpertSender gateway

Reads incoming messages using SMTP, translates to the REST API.


## Installation

```
# cd /opt
# git clone git@github.com:umonkey/ersties-mailwarm-gw.git
# pip install --no-cache-dir mail-parser requests
```


## Running

Direct forwarding:

```
# cd /opt/ersties-mailwarm-gw
# EXPERTSENDER_API_KEY='foobar' python3 src/server.py
...
Waiting for messages on *:1025
```

Dump files to a folder:

```
# mkdir -p /var/mailwarm-gw
# cd /opt/ersties-mailwarm-gw
# EXPERTSENDER_DUMP_FOLDER=/var/mailwarm-gw python3 src/server.py
...
Waiting for messages on *:1025
```

Using docker:

```
# mkdir -p /var/mailwarm-gw
# cd /opt/ersties-mailwarm-gw
# docker build --tag mailwarm-bridge:v1 .
# docker run --rm -p 1025:1025/tcp --name mailwarm-bridge --env EXPERTSENDER_DUMP_FOLDER=/var/mailwarm-gw --env EXPERTSENDER_API_KEY='foobar' mailwarm-bridge:v1
...
Waiting for messages on *:1025
```


## Configuration

Environment variables:

- `EXPERTSENDER_API_KEY` -- secret key.
- `EXPERTSENDER_API_URL` -- URL to post to.
- `EXPERTSENDER_DUMP_FOLDER` -- where to put JSON files with messages.


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
