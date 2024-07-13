# DynDNS

Exceedingly stupidly simple script to run inside your network to keep your home-hosted site online when your ISP changes your IP for some reason.

## Setup

Create an IAM user in the AWS console with at least `{ "Effect": "Allow", "Action": "route53:ChangeResourceRecordSets" }` permissions, and create an access key, then:

```shell
cp example.envrc .envrc
${EDITOR:-nano} .envrc  # Fill in your details here.
```

## Running

```shell
./src/main.py
```

This will grab the IP you're currently on from [`ifconfig.co`](https://ifconfig.co), and set it as the A records specified in your environment variables, then exit.

## Installation.

Use systemd to run it on a timer or something I dunno bro, whatever you want.  Set up a cron.  Set up uptimerobot and have mozilla thunderbird run a command whenever you get an email from it.  World's your oyster.
