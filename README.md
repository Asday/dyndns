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

Install `python` and `python-virtualenv`.

Assuming you have systemd, run

```shell
cd /path/to/which/to/install/
git clone git@github.com:Asday/dyndns.git
make install
```

If you don't have systemd, run

```shell
cd /path/to/which/to/install/
git clone git@github.com:Asday/dyndns.git
make
```

Then figure out how to run [`src/main.py`](src/main.py) with the virtual environment on your own.
