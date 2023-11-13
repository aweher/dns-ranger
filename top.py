#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import yaml
from collections import Counter

def read_config(config_file):
    with open(config_file, "r") as f:
        return yaml.safe_load(f)

def read_domain_records(cfg):
    try:
        with open(cfg['capture']['resultsfile'], 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def top_domains(dnsdata, number=10):
    domain_counter = Counter()
    for domain, ip_data in dnsdata.items():
        domain_counter[domain] = sum(ip_data.values())
    return domain_counter.most_common(10)

def top_ips_per_domain(dnsdata, domain, number=10):
    ip_counter = Counter()
    for ip, count in dnsdata[domain].items():
        ip_counter[ip] = count
    return ip_counter.most_common(10)

if __name__ == '__main__':
    config = read_config('config.yaml')
    datos = read_domain_records(config)
    for domain, queries in top_domains(datos):
        print(f"\nDomain --> {domain} Queries --> {queries}")
        for ip, count in sorted(top_ips_per_domain(datos, domain), key=lambda x: x[1], reverse=True):
            print(f"\tIP: {ip} Queries: {count}")