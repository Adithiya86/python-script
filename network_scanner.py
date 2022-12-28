import scapy.all as scapy
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="specify the interface")
    options = parser.parse_args()
    if not options.target:
        # parser.error("[-] enter the target, use --help for more info.")
        print("[-] enter the target, use --help for more info.")
    return options.target

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast/arp_request
    answered_list = scapy.srp(arp_packet, timeout=1, verbose=False)[0]
    client_list=[]
    for element in answered_list:
        client_dict={"ip":element[1].psrc,"mac": element[1].hwsrc}
        client_list.append(client_dict)
    return client_list

def print_result(results_list):
    print("---------------------------------------------------")
    print("IP\t\t\t\tMAC ADDRESS")
    print("---------------------------------------------------")
    for client in results_list:
        print(client["ip"] +"\t\t\t"+ client["mac"])
    print("- - - - - - - - - - - - - - - - - - - - - - - - - -")

target=get_arguments()
scan_result =scan(target)
if not scan_result:
    pass
else:
    print_result(scan_result)