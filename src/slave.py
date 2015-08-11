#!/usr/bin/env python
"""
Dependencies:
	- arimon-ng
	- scapy
"""
from scapy.all import *

import getopt, sys, os, socket

#Global variables
master = None
interface = None
port = "8989"
macAnterior = ""

def usage():
	print "Usage: slave.py <options>\n"
	print "Options:"
	print "-m , --master		IP address of master node."
	print "-p , --port		UDP port of master (default=8989)"
	print "-i , --interface		Wireless interface."
	print "-h , --help		Print this help message."
	print "\nExample: slave.py -m 192.168.1.1 -i wlan0"

def parseOptions(argv):
	global master, interface, port
	try:
		opts, args = getopt.getopt(argv, "m:p:i:h", ["help","master","port","interface"])
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				usage()
				sys.exit()
			if opt in ("-m", "--master"):
				master = arg
			if opt in ("-p", "--port"):
				port = arg
			if opt in ("-i", "--interface"):
				interface = arg

		if interface != None and master != None:
			return (master, interface, port)
		else:
			usage()
			sys.exit()

	except getopt.GetoptError:
		usage()
		sys.exit()

def changeMonitorInterface(interface):
	command = "airmon-ng start " + interface
	os.system(command)

def changeNormalInterface():
	command = "airmon-ng stop mon0"
	os.system(command)

def init():
	changeNormalInterface()
	changeMonitorInterface(interface)
	os.system("clear")

def handlePacket(pkt):
	global macAnterior
	#Wlan 802.11 packet
	if pkt.haslayer(Dot11):
		#Type 0 (management) subtype 4 (probe request)
		if pkt.type == 0 and pkt.subtype == 4:
			#Sender MAC addr
			signal = -(256-ord(pkt.notdecoded[-4:-3]))
			macActual = pkt.addr2
			if macActual != macAnterior:
				msg = macActual + "@" + str(signal)
				sendMessageToMaster(msg)
				macAnterior = macActual

def sendMessageToMaster(msg):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	endpoint = (master,int(port))
	sock.sendto(msg, endpoint)

def main(argv):
	global master, interface, port
	(master, interface, port) = parseOptions(argv)
	init()
	print "Running slave.py ..."
	sniff(iface="mon0", prn = handlePacket)

if __name__ == "__main__":
	main(sys.argv[1:])
