#!/usr/bin/env python3

import argparse
import subprocess
import re
import sys

query_regex = re.compile(
    r"^(?P<time>\d+\.\d+)\s+IP\s+"
    r"(?P<ip_source>.+?)\.\d+\s+>\s+"
    r"(?P<ip_dest>.+?)\.\d+:\s+"
    r"(?P<query_id>\d+)\+?\s+[A-Z]+\?\s+"  
    r"(?P<domain>.+?)\s+(\(\d+\))$"
)

response_regex = re.compile(
    r"^(?P<time>\d+\.\d+)\s+IP\s+"
    r"(?P<ip_source>.+?)\.\d+\s+>\s+"
    r"(?P<ip_dest>.+?)\.\d+:\s+"
    r"(?P<query_id>\d+)\s+"
    r"[\d/]+\s*"
    r"(?P<records_string>.*?)"
    r"\s*\(\d+\)$"
)

def monitor_dns(interface: str):
    """
    Runs tcpdump and monitors its output to calculate DNS response times.

    Args:
        interface: The network interface to monitor (e.g., 'eth0', 'wlan0').
    """
    # -n: don't convert addresses to names
    # -tt: print unix timestamp
    # -l: line-buffer output
    command = ["sudo", "tcpdump", "-i", interface, "-n", "-tt", "-l", "port", "53"]
    
    # A dictionary to store pending queries: {query_id: {time, domain, dns_ip}}
    queries = {}

    print(f"🚀 Starting DNS monitor on interface: {interface}")
    print("Waiting for DNS traffic... (Press Ctrl+C to stop)")

    try:
        # We need stdout and stderr to be pipes so we can read them.
        # bufsize=1 means line-buffered.
        # We decode as 'utf-8' and ignore errors.
        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                encoding='utf-8',
                errors='ignore'
            )
        except FileNotFoundError:
            print("Error: 'tcpdump' command not found.", file=sys.stderr)
            print("Please install tcpdump and ensure it's in your PATH.", file=sys.stderr)
            sys.exit(1)

        # Monitor for errors from tcpdump
        if process.stderr:
        # Read from stdout line by line
            for line in iter(process.stdout.readline, ''):
                # Check for a query
                query_match = query_regex.search(line)
                if query_match:
                    query_data = query_match.groupdict()
                    query_id = query_data['query_id']
                    queries[query_id] = query_data
                    continue

                response_match = response_regex.search(line)
                if response_match:
                    response_data = response_match.groupdict()
                    query_id = response_data['query_id']
                    query_info = queries.pop(query_id, None)

                    response_ms = 1000*(float(response_data['time']) - float(query_info['time']))
                    records_string = response_data['records_string']                    
                        
                    print(f"⏱️  DNS: {query_info['ip_dest']} \t Response: {response_ms:8.2f} ms \t(ID: {query_id} Domain: {query_info['domain']} records: {records_string})")
                    continue

                print(line)

    except KeyboardInterrupt:
        print("\n👋 Stopping monitor...")
    except Exception as e:
        process.kill()
        print("Done.")

def main():
    """Parses command-line arguments and starts the DNS monitor."""
    parser = argparse.ArgumentParser(description="Live monitor for DNS query latency using tcpdump.")
    parser.add_argument("-i", "--interface", required=True, help="Network interface to monitor (e.g., 'eth0', 'wlan0')")
    args = parser.parse_args()
    monitor_dns(args.interface)

if __name__ == "__main__":
    main()
