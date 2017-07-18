#!/usr/bin/python
from intouch2 import intouch2
import logging

spa = intouch2(logging.DEBUG)

# Set the MAC address of the device
spa.Mac = 'SPAd8:80:39:a1:a1:a1'

# Source Connection (?) value. Obtain this value from an existing communication from the App (using for example Wireshark)
spa.Srccn = 'XXX413c433-b343-4f24-a432-5ed5c53cb152c'

spa.connect()

print 'Channel: %d' % spa.getCurrentChannel()
print 'Setpoint: %d.  Current Temperature: %d.  Lights: %d.  Version: %s.  Base config: %s.' % spa.getStatus()

spa.disconnect()
