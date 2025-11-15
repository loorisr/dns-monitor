# dns-monitor

Tool to monitor UDP DNS queries using tcpdump and calculate DNS response time.

Root needed

# Usage

Replace enp3so with your interface
    python3 dns_mon.py -i enp3s0

Output example:

- ⏱️  DNS: 1.1.1.1          Response:    10.41 ms  (ID: 34435 Domain: web.whatsapp.com. records: CNAME mmx-ds.cdn.whatsapp.net.)
- ⏱️  DNS: 1.1.1.1          Response:    11.82 ms  (ID: 46466 Domain: web.whatsapp.com. records: CNAME mmx-ds.cdn.whatsapp.net., A 185.60.219.60)
- ⏱️  DNS: 1.1.1.1          Response:    11.82 ms  (ID: 62614 Domain: mmx-ds.cdn.whatsapp.net. records: )
- ⏱️  DNS: 1.1.1.1          Response:    11.76 ms  (ID: 12592 Domain: mmx-ds.cdn.whatsapp.net. records: AAAA 2a03:2880:f33c:120:face:b00c:0:167)
- ⏱️  DNS: 1.1.1.1          Response:    12.56 ms  (ID: 6743 Domain: static.whatsapp.net. records: CNAME mmx-ds.cdn.whatsapp.net., A 157.240.195.56)
- ⏱️  DNS: 1.1.1.1          Response:    12.70 ms  (ID: 23228 Domain: static.whatsapp.net. records: CNAME mmx-ds.cdn.whatsapp.net., AAAA 2a03:2880:f27b:2cc:face:b00c:0:167)
- ⏱️  DNS: 1.1.1.1          Response:    11.40 ms  (ID: 20851 Domain: mmx-ds.cdn.whatsapp.net. records: )
