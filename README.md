# Mailwarm to ExpertSender gateway

Reads incoming messages using SMTP, translates to the REST API.


## Configuration

Environment variables:

- `EXPERTSENDER_API_KEY` -- secret key.
- `EXPERTSENDER_API_URL` -- URL to post to.


## Running

(1) With docker run:

```
$ cat /etc/ersties/mailwarm-bridge.env
EXPERTSENDER_API_KEY=123456
EXPERTSENDER_API_URL=https://api3.esv2.com/v2/Api/SystemTransactionals/6
$ docker run --rm -p 1025:1025/tcp --name mailwarm-bridge --env-file /etc/ersties/mailwarm-bridge.env mailwarm-bridge:v1
```

(2) With docker composer:

```
$ docker composer up
```


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
