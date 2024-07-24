#!/bin/env python

import ipaddress
import json
import os
from pathlib import Path

import boto3
import requests


hosted_zone_id = os.environ["HOSTED_ZONE_ID"]
a_records = json.loads(os.environ["A_RECORDS"])

raw_ip = requests.get("https://ifconfig.co/ip").text.strip()

# Sanity check what `ifconfig.co` returned wasn't garbage.
ip = ipaddress.ip_address(raw_ip)
if ip.version != 4: raise ValueError(f"{ip} is not an IPv4 address")

ipfile = Path(os.getenv("STATE_DIRECTORY", ".")).resolve() / "ip"
print(f"checking {ipfile}")
if not ipfile.exists():
    with open(ipfile, "w"): pass

with open(ipfile, "r") as f:
    if raw_ip == f.read():
        print("ip has not changed")
        exit(0)

change_batch = {
    "Changes": [
        {
            "Action": "UPSERT",
            "ResourceRecordSet": {
                "Name": a_record,
                "ResourceRecords": [{"Value": raw_ip}],
                "TTL": 300,
                "Type": "A",
            },
        }
        for a_record in a_records
    ],
}

c = boto3.client('route53')

c.change_resource_record_sets(
    ChangeBatch=change_batch,
    HostedZoneId=hosted_zone_id,
)

with open(ipfile, "w") as f:
    f.write(raw_ip)

print(f"successfully updated IP to {raw_ip}")
