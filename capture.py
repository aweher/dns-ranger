#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

from scapy.all import *
import sys
import yaml
import json
import threading
import time
from scapy.layers.dns import DNS, DNSQR
from tqdm import tqdm

def read_config(config_file):
    with open(config_file, "r") as f:
        return yaml.safe_load(f)

def read_domain_records():
    try:
        with open(config['capture']['resultsfile'], 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def dnscapture(pkt):
    global packet_count
    packet_count += 1
    if pkt.haslayer(DNS):
        if pkt[DNS].qr == 0: # DNS query
            #print(f"Source IP address: {pkt[IP].src}, Domain: {pkt[DNSQR].qname.decode('utf-8')}")
            if DNSQR in pkt:
                domain = pkt[DNSQR].qname.decode('utf-8')
                ip = pkt[IP].src
                if domain not in domain_records:
                    domain_records[domain] = {ip: 1}
                else:
                    if ip not in domain_records[domain]:
                        domain_records[domain][ip] = 1
                    else:
                        domain_records[domain][ip] += 1

def print_packet_count():
    with tqdm(total=None, dynamic_ncols=True, bar_format='{desc}', unit='pkts') as pbar:
        count = 0
        while True:
            new_count = packet_count
            pbar.set_description_str(f"Number of packets captured: {new_count}")
            pbar.update(new_count - count)
            count = new_count
            time.sleep(1)

def save_domain_records(domain_records):
    temp_records = domain_records.copy()
    with open(config['capture']['resultsfile'], 'w') as f:
        json.dump(temp_records, f)

def save_domain_records_periodically():
    while True:
        time.sleep(config['capture']['dumpstats'])
        save_domain_records(domain_records)

def main():
    print(f"Starting DNS capture on interface {config['capture']['interface']}")
    ignorehosts = config['capture']['ignorehosts']
    ignore_filter = ' and '.join(f'not host {ip}' for ip in ignorehosts)
    sniff(iface=config['capture']['interface'], filter=f"port 53 and {ignore_filter}", prn=dnscapture, store=0)

if __name__ == '__main__':
    try:
        # Init
        packet_count = 0 
        config = read_config("config.yaml")
        domain_records = read_domain_records()

        # Start a background thread that saves domain_records periodically
        threading.Thread(target=print_packet_count).start()
        threading.Thread(target=save_domain_records_periodically, daemon=True).start()
        main()
    except KeyboardInterrupt:
        print(f'Interrupted by user. Number of packets captured: {packet_count}')
        print(f"Saving domain records to {config['capture']['resultsfile']}")
    finally:
        save_domain_records(domain_records)  # Also save when the script exits
        print("\nDomain records saved. Please press CTRL+C again...")
        save_domain_records(domain_records)
        sys.exit(0)