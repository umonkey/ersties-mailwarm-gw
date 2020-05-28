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
