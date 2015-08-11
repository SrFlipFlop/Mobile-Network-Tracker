#!/usr/bin/env python

import socket, sys, getopt, os, datetime

#Global variables
ip = None
port = "8989"
file = False

def usage():
	print "Usage: master.py <options>\n"
	print "Options:"
	print "-i , --ip		IP address of master node."
	print "-p , --port		UDP port of master (default=8989)."
	print "-h , --help		Print this help message."
	print "-f , --file		Save data in a file (default=false)."
	print "\nExample: master.py -i 192.168.1.1 -p 7777"

def parseOptions(argv):
	global ip, port, file
	try:
		opts, args = getopt.getopt(argv, "i:p:hf", ["help","ip", "port", "file"])
		for opt, arg in opts:
			if opt in ("-h", "--help"):
				usage()
				sys.exit()
			if opt in ("-i", "--ip"):
				ip = arg
			if opt in ("-p", "--port"):
				port = arg
			if opt in ("-f", "--file"):
				file = True

		if ip != None:
			return (ip, port)
		else:
			usage()
			sys.exit()

	except getopt.GetoptError:
		usage()
		sys.exit()

def createSocket(ip, port):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	endpoint = (ip, int(port))
	sock.bind(endpoint)
	return sock

def calculateDistance(RSSI):
	#RSSI = -10nlog(d)+A
	A = -35.0 	#RSSI a 1m del receptor
	n = 3.2		#Environment 1.6/2.7
	distance = 10.0**((A-int(RSSI))/(10.0*n))
	return str(distance)

def parseMessage(msg):
	mac, senyal = msg.split('@')
	distance = calculateDistance(senyal)
	date = datetime.datetime.now()
	print mac + "#" + senyal + "#" + distance + "#" + str(date) 

def main(argv):
	global ip, port, file
	(ip, port) = parseOptions(argv)
	sock = createSocket(ip, port)
	os.system("clear")
	print "Running master.py ..."
	if file:
		f = open("master_file.txt", "w")	
		while True:
			data, addr = sock.recvfrom(1024)
			f.write(parseMessage(data) + "\n")

	if not file:
		while True:
			data, addr = sock.recvfrom(1024)
			parseMessage(data)

if __name__ == "__main__":
	main(sys.argv[1:])
