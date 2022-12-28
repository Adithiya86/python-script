import subprocess
import optparse
import re
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="specify the interface")
    parser.add_option("-m", "--macaddress", dest="New_mac", help="specify the mac address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[-] enter the interface, use --help for more info.")
    elif not options.New_mac:
        parser.error("[-] enter the mac address to change, use --help for more info.")
    return options

def change_mac(interface, New_mac):
    subprocess.call(["ifconfig",interface, "down"])
    subprocess.call(["ifconfig",interface,"hw", "ether",New_mac])
    subprocess.call(["ifconfig",interface,"up"])
    subprocess.call(["ifconfig",interface])


options = get_arguments()
# change_mac(options.interface, options.New_mac)
ifconfig_result = subprocess.check_output(["ifconfig", options.interface]).decode()
mac_search_result = re.search(r'\w\w:\w\w:\w\w:\w\w:\w\w:\w\w', ifconfig_result)
if mac_search_result:
    print(mac_search_result.group(0))
else:
    print("could not read the mac address")


