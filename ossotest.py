#!/usr/bin/env python
"""
OSSO test script.
To run this you need to install devicetree support for
Osso board from https://github.com/unixmedia/Osso
and Adafruit I/O library for beaglebone
from https://github.com/adafruit/adafruit-beaglebone-io-python
(and, of course, python!)
"""
import sys, time
import Adafruit_BBIO.GPIO as GPIO

INPUTS={
         1:'P8_15',
         2:'P8_11',
         3:'P8_14',
         4:'P8_12',
         5:'P8_16',
         6:'P8_17',
         7:'P8_17',
         8:'P8_26'
      }

RELAYS={
         1:'P9_12',
         2:'P9_15',
         3:'P9_23',
         4:'P8_9',
         5:'P9_27',
         6:'P9_41',
         7:'P8_7',
         8:'P9_42'
      }

def printhelp():
   print "Usage:", sys.argv[0], "<input|relay>"
   print
   print "Example:"
   print
   print sys.argv[0], "input 3"
   print
   print sys.argv[0], "relay 2"
   print
def initialize():
   for i in INPUTS.values():
      GPIO.setup(i, GPIO.IN)
   for i in RELAYS.values():
      GPIO.setup(i, GPIO.OUT)

def relay(rel):
   GPIO.output(RELAYS[rel], GPIO.HIGH)
   print 'RELAY', rel, 'IS NOW ON (ctrl+C to exit, on exit any relay will be switched off)'
   while 1: time.sleep(1)

def digitalinp(inp):
   print 'INPUT', inp, 'IS', 'open' if GPIO.input(INPUTS[inp]) else 'close'
   print
   print 'Waiting for a state change... (or ctrl+C to exit)'
   GPIO.wait_for_edge(INPUTS[inp], GPIO.BOTH)
   time.sleep(.01) # Adafruit library needs a little time to detect right status
   print 'INPUT', inp, 'IS NOW', 'open' if GPIO.input(INPUTS[inp]) else 'close'

def custom_excepthook(type, value, traceback):
   if type is KeyboardInterrupt:
      print 'Exit.'
      return # do nothing
   else:
      sys.__excepthook__(type, value, traceback)

sys.excepthook=custom_excepthook

if __name__=='__main__':
   try:
      if (len(sys.argv)>=3
         and sys.argv[1]=='relay'
         and int(sys.argv[2]) in range(1, 9)):
         initialize()
         relay(int(sys.argv[2]))
         sys.exit(0)
      elif (len(sys.argv)>=3
         and sys.argv[1]=='input'
         and int(sys.argv[2]) in range(1, 9)):
         initialize()
         digitalinp(int(sys.argv[2]))
         sys.exit(0)
   except KeyboardInterrupt:
      sys.exit(0)
   printhelp()
   sys.exit(1)
