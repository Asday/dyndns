#!/bin/env python

import ipaddress
import json
import os

import boto3
import requests


hosted_zone_id = os.environ["HOSTED_ZONE_ID"]
a_records = json.loads(os.environ["A_RECORDS"])

raw_ip = requests.get("https://ifconfig.co/ip").text.strip()

# Sanity check what `ifconfig.co` returned wasn't garbage.
ip = ipaddress.ip_address(raw_ip)
if ip.version != 4: raise ValueError(f"{ip} is not an IPv4 address")

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
