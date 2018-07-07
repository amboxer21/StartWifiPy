#!/usr/bin/env python2.7

import pyroute2,re,sys
from socket import AF_INET
from pyroute2 import IPRoute,IPDB
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

        self.ipdb    = IPDB()
        self.iproute = IPRoute()

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

    def ipAddress(self,catch_noneInterface_state):
        try:
            return self.iproute.get_addr(label=interface)[0]['attrs'][0][1]
        except IndexError:
            print("[ERROR] - Could not get IP because interface \"" + interface + "\" was not found!")
            sys.exit(0)

    def wirelessInterface(self):
        try:
            for i in self.ipdb.interfaces:
                interface = re.search("^w[\w\d]+\d", str(i), re.M | re.I)
                if interface is not None:
                    print("[INFO] - Using the \"" + interface.group() + "\" wireless interface.")
                    return interface.group()
            if interface is None:
                print("[ERROR] - No wireless interface found.")
                sys.exit(0)
        except IndexError:
            print("[ERROR] - No wireless interface found.")
            sys.exit(0)

    def interfaceIndex(self,interface):
        return self.iproute.link_lookup(ifname=self.catchNoneInterfaceState(interface))[0]

    def setInterfaceUp(self,interface):
        try:
            self.iproute.link("set", index=self.interfaceIndex(self.catchNoneInterfaceState(interface)), state="up")
            print('[INFO] - Brought ' + interface + ' interface \"UP\" successfully.')
        except:
            print('[ERROR] - Could not bring interface '+ interface + ' up.')
            sys.exit(0)

    def setInterfaceDown(self,interface):
        try:
            self.iproute.link("set", index=self.interfaceIndex(self.catchNoneInterfaceState(interface)), state="down")
            print('[INFO] - Brought ' + interface + ' interface \"DOWN\" successfully.')
        except:
            print('[ERROR] - Could not bring interface '+ interface + ' down.')
            sys.exit(0)

    def interfaceState(self,interface):
        try:
            iface = re.search("up|down", str(self.ipdb.interfaces[self.catchNoneInterfaceState(interface)].operstate), re.M | re.I)
            if iface is None:
                print("[ERROR] - Interface state is unknown or not found.")
                sys.exit(0)
            return iface.group()
        except IndexError:
            print("[ERROR] - Interface not found.")
            sys.exit(0)

    def defaultRoute(self):
        try:
            return self.ipdb.routes[{'dst': 'default', 'family': AF_INET}]
        except KeyError:
            print("[ERROR] - Default route not present. Adding it now.")
            # Add default route here

    def routes(self):
        try:
            for route in ip.route('dump'):
                #print(str(route))
                return str(dict(route)['attrs'])
        except IndexError:
            pass

    def addRoute(self):
        print('')

    def removeRoute(self):
        print('')

    def catchNoneInterfaceState(self,interface):
        if interface is None:
            interface = self.interface
        return interface

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
    try:
        startWifi = StartWifi()
        startWifi.continueAnyway()
    except KeyboardInterrupt:
        print("\n[INFO] - Control + C caught. Exiting now!")
        sys.exit(0)
