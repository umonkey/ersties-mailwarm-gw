# Mailwarm to ExpertSender gateway

Reads incoming messages using SMTP, translates to the REST API.


## Configuration

Environment variables:

- `EXPERTSENDER_API_KEY` -- secret key.
- `EXPERTSENDER_API_URL` -- URL to post to.

Store in `/etc/ersties/mailwarm-bridge.env`:

```
$ cat /etc/ersties/mailwarm-bridge.env
EXPERTSENDER_API_KEY=foobar
EXPERTSENDER_API_URL=https://api3.esv2.com/v2/Api/SystemTransactionals/6
```

## Running

(0) Prepare the image:

```
$ git clone https://github.com/umonkey/ersties-mailwarm-gw
$ cd ersties-mailwarm-gw
$ docker build --tag mailwarm-bridge:v1 .
```

(1) Run with docker run:

```
$ docker run --rm -p 1025:1025/tcp --name mailwarm-bridge --env-file /etc/ersties/mailwarm-bridge.env mailwarm-bridge:v1
...
Waiting for messages on *:1025
```

(2) Or, run with docker composer:

```
$ docker compose up
Recreating ersties-mailwarm-gw_bridge_1 ... done
Attaching to ersties-mailwarm-gw_bridge_1
bridge_1  | Waiting for messages on *:1025
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
