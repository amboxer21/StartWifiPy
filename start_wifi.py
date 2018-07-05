#!/usr/bin/env python2.7

import pyroute2,re
from socket import AF_INET
from pyroute2 import IPRoute
from optparse import OptionParser

class StartWifi():

    def __init__(self):
        parser = OptionParser(usage="%prog <Interface Name> <IP Address> <ESSID>", version="%prog version 1.0.2")
        parser.add_option("-I", "--interface", dest='interface', help='Interface name.')
        parser.add_option("-i", "--ip_address", dest='ip_address',
            default="192.168.43.2", help='IP Address to assign to your device.')
        parser.add_option("-e", "--essid", dest='essid',
            default="AndroidAP", help='Network/Access point name.')
        parser.add_option("-g", "--gateway", dest='gateway',
            default="192.168.43.1", help='Specify the gateway address.')
        parser.add_option("-R", "--reset", dest='reset', action='store_true',
            default=False, help='Reset all wireless configuration that start_wifi.py just set.')
        (options, args) = parser.parse_args()

        self.ip = IPRoute()

        self.essid = options.essid
        self.gateway = options.gateway
        self.ip_address = options.ip_address

        if options.interface is None:
            self.interface = self.wirelessInterface()
        else:
            self.interface = options.interface
        if self.essid == 'AnthonyAP' or self.ip_address == '192.168.43.2' or self.gateway == '192.168.43.1':
            print("[INFO] - Using default args since none were specified.")
            print("\n[OPTIONS] - (defaults)")
            print("          - essid: " + self.essid)
            print("          - interface: " + self.interface)
            print("          - gateway: " + self.gateway)
            print("          - ip_address: " + self.ip_address)

    def ipAddress(self,interface):
        try:
            return self.ip.get_addr(label=interface)[0]['attrs'][0][1]
        except IndexError:
            print("[ERROR] - Could not get IP because interface \"" + interface + "\" was not found!")

    def wirelessInterface(self):
        try:
            for index in self.ip.get_addr():
                interface = re.search("^w[\w\d]+\d", str(dict(index)['attrs'][3][1]), re.M | re.I)
                if interface is not None:
                    print("[INFO] - Using the \"" + interface.group() + "\" wireless interface.")
                    return interface.group()
            if interface is None:
                print("[ERROR] - No wireless interface found.")
        except IndexError:
            print("[ERROR] - No wireless interface found.")

    def interfaceUp(self):
        print('')

    def interfaceDown(self):
        print('')

    def continueAnyway(self):
        answer = raw_input("Continue(Y|y|yes|YES|Yes)? ")
        regex  = re.search('(Y|y|yes|YES|Yes)', str(answer), re.M)
        if regex is not None:
            print("Continuing.")
            return True
        else:
            print("QUITING NOW!")
            return False

if __name__ == '__main__':
    startWifi = StartWifi()
    startWifi.continueAnyway()

