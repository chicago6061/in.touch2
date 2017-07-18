#!/usr/bin/python
import socket
import logging
import re
from struct import *

class Watercare:
        AwayFromHome, Standard, EnergySaving, Supersaver, Weekender = range(0, 5)

class Messages:
	Hello = '<HELLO>%d</HELLO>'
	GetCurrentChannel = '<PACKT><SRCCN>%s</SRCCN><DESCN>%s</DESCN><DATAS>CURCH%d</DATAS></PACKT>'
	GetWatercare = '<PACKT><SRCCN>%s</SRCCN><DESCN>%s</DESCN><DATAS>GETWC%d</DATAS></PACKT>'
	GetStatus = '<PACKT><SRCCN>%s</SRCCN><DESCN>%s</DESCN><DATAS>STATU%d\x00\x00\x02\x00</DATAS></PACKT>'

class intouch2:
	server_address = ('intouch.geckoal.com', 10022)
        sock = None
        sqn = 1
	Srccn = 'dummy'
	Mac = ''

	def __init__(self, level):
		logging.basicConfig(level=level,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='intouch2.log')

	def connect(self):
		logging.info('Connecting to %s:%d' % (self.server_address[0], self.server_address[1]))
        	# Create a UDP socket
        	self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        	# We'll wait up to 1 second for a response
        	self.sock.settimeout(1)
		# Starting sequence number
        	self.sqn = 1


	def disconnect(self):
		logging.info('Disconnecting')
        	self.sock.close();

	def sendWithSrccnMacSqn(self, msg, srccn, mac):
		buf = msg % (srccn, mac, self.sqn)
        	self.sqn = self.sqn + 1	
		return self.send(buf)

	def sendWithSqn(self, msg):
        	buf = msg % (self.sqn)
        	self.sqn = self.sqn + 1	
		return self.send(buf)

	def send(self, msg):
		logging.debug('Sending `%s`' % msg)
        	sent = self.sock.sendto(msg, self.server_address)

	def recv(self):
		logging.debug('Waiting to receive data')
		try:
			data, server = self.sock.recvfrom(4096)
		except:
			logging.error('Timeout! No data received')
	 		return None
		logging.debug('Received `%s`' % data)
		return data

	def sendHello(self):
		self.sendWithSqn(Messages.Hello)
		return self.recv()

	def getCurrentChannel(self):
		logging.debug('Sending GetCurrentChannel message')
	 	self.sendWithSrccnMacSqn(Messages.GetCurrentChannel, self.Srccn, self.Mac)
		data = self.recv()
		m = re.search(r'<DATAS>CHCUR(.*)</DATAS>', data, re.DOTALL)
		(channel, rest) = unpack('>bb', m.group(1))
		return channel

	def getCurrentWatercare(self):
		logging.debug('Sending GetWatercare message')
		self.sendWithSrccnMacSqn(Messages.GetWatercare)
		data = self.recv()
		m = re.search(r'<DATAS>WCGET(.*)</DATAS>', data)
		(value) = unpack('b', m.group(1))
		return Watercare(value[0])

	def getStatus(self):
		logging.debug('Sending GetStatus message')
		self.sendWithSrccnMacSqn(Messages.GetStatus, self.Srccn, self.Mac)
		while True:
			data = self.recv()
			m = re.search(r'<DATAS>STATV(.*)</DATAS>', data, re.DOTALL)
			(seq, next, rest) = unpack('>bb{0}s'.format(len(m.group(1))-2), m.group(1))
			logging.debug('Status message: Seq: %s. Next: %s. Length: %s' % (seq, next, len(rest)))
			#print [hex(ord(c)) for c in rest]
			# If next sequence number is 0, that appears to be the end of the messages
			if (next == 0): 
				break;
			# Some interesting fields are present in the 7th message
			if (seq == 7):
				(f1, f2, f3, setpoint, temp, junk1, YT1, YT2, YT3, config, j1, j2, j3, j4, lights, junk2) = unpack('>bbbhh18shbbhbbbbb4s', rest)
				setpoint = setpoint/10.0+32.0
				temp = temp/10.0+32.0
				version = "inYT %s v%s.%s" % (YT1, YT2, YT3)
		return (setpoint, temp, lights, version, config)

