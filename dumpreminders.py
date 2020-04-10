#!/usr/bin/python
import socket
import struct
from struct import *
import re
import xml.etree.ElementTree as ET

global sock
global server_address
global sqn

# 1)
# Replace xxx with ID
# Replace yyy with MAC
reqrm = '<PACKT><SRCCN>xxx</SRCCN><DESCN>yy</DESCN><DATAS>REQRM#SEQ#\x00\x00\x02\x00</DATAS></PACKT>'

# 2)
# Download SpaPackStruct.xml from http://intouch.geckoal.com/gecko/prod/SpaPackStruct.xml

# 3)
# Replace IP address below

def connect():
        global sock
        global sqn
        global server_address

        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', 0))
        localport = sock.getsockname()[1]
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
        # We'll wait up to 20 second for a response
        sock.settimeout(20)
        connected = True
        server_address = ('192.168.2.231', 10022)
        print "Connected. ", server_address
        sqn = 1

def send(msg):
        global sqn
        buf = msg.replace('#SEQ#', struct.pack('b', sqn))
#       print >>sys.stderr, 'sending "%s"' % buf
        sent = sock.sendto(buf, server_address)
        sqn = sqn + 1

def recv():
    try:
        data, server = sock.recvfrom(4096)
    except:
        print "Timeout! No data received.."
        return None
    return data

def disconnect():
        sock.close();

desc = ["Invalid", "RinseFilter", "CleanFilter", "ChangeWater", "CheckSpa", "ChangeOzonator", "ChangeVisionCartridge"]
def getReminders(log, config):
        send(reqrm)
	position = 0
        data = recv()
        m = re.search(r'<DATAS>RMREQ(.*)</DATAS>', data, re.DOTALL)
	rest = m.group(1)
	while (len(rest) > 0):
        	(t, days, dummy, push, rest) = unpack('>bbbb{}s'.format(len(rest)-4), rest)
		if (t > 0):
			print "%s %d days" % (desc[t], days)

def lookup(root, index):
	t = root.findall(".//*[@Pos='"+str(index)+"']")
	result = ""
	for e in t:
		if ('BitPos' in e.attrib):
			result = result + e.tag + "(" + e.attrib['BitPos'] + "),"
		else:
			result = result + e.tag + ","
	return result

tree = ET.parse('SpaPackStruct.xml')

# Replace 'InYT' with the applicable model
# Hardcoded to use the first structure/version of Log and Config Structures
log = tree.findall(".//*[@Name='InYT']/LogStructures[0]/LogStructure")
config = tree.findall(".//*[@Name='InYT']/ConfigStructures[0]/ConfigStructure")

connect()
getReminders(log[0], config[0])
disconnect()
