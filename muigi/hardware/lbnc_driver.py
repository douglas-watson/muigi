#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   lbnc_driver.py - 'driver' for LBNC's custom microcontroller 
#
#   PURPOSE: 
#       Provide an RPC interface to the microcontroller, as well as high
#       level functions for operation of the microfluidic chip.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 8th August 2011
#
#   LICENSE: GNU GPLv3
#
#   Copyright (C) 2011 Douglas Watson
#
#   This program is free software: you can redistribute it and/or modify it
#   under the terms of the GNU General Public License as published by the Free
#   Software Foundation, either version 3 of the License, or (at your option)
#   any later version.
#  
#   This program is distributed in the hope that it will be useful, but WITHOUT
#   ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#   FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#   more details.
# 
#   You should have received a copy of the GNU General Public License along
#   with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################

"""
LBNC Driver
===========

A driver for LBNC's home built microcontroller. This driver was written as an
early test piece, and does not fulfill the 'standard' set by the EasyDAQ
driver. It does not provide a simple library, intended to be re-used by other
software, but is instead a standalone RPyC server.

The newer approach is the have the driver only look after serial communication, and only use RPC if stricly necessary, for example in the case where the web
server should be able to run on a different computer than the hardware
computer.

"""

usage = """

    lbnc_driver.py [-p PORT] [-d DEVICE]

    If executed alone, start an RPC server, providing control over the LBNC
    microcontroller. If the RPyC name server is running, it will advertise the
    service "LBNCCONTROLLER" through the name server, allowing a connection to
    be established with the rpyc.connect_by_service() function.


Configuration:

    Settings are kept in the lbnc_settings.py file. If the driver cannot
    connect to the microcontroller, check the DEVICE variable. For convenience,
    the settings can be overidden with command line arguments.
"""

import sys
import rpyc
import serial
from serial import SerialException
import logging

from lbnc_settings import PORT, DEVICE

version = 'pre-alpha'

class LBNCControllerService(rpyc.Service):

    def on_connect(self):
        print "Connection received"
        self.daq = None # replaced later by self.exposed_open_serial()

    def on_disconnect(self):
        print "Connection closed"
        # Close serial port
        if self.daq is not None:
            self.daq.close()

    def reset_a(self):
        """ Reset communication to valve A """
        self.daq.write("!A" + chr(0))

    def reset_b(self):
        """ Reset communication to valve B """
        self.daq.write("!B" + chr(0))

    def exposed_open_serial(self):
        ''' Open serial connection to DAQ.
        
        This has to be implemented as a standalone method to send feedback to
        the user. 
        
        ''' 

        try: 
            self.daq = serial.Serial(DEVICE) 
        except SerialException, e:
            raise SerialException(e) 
        return "Serial connection established."

    def exposed_reset(self):
        """ Reset state of all valves on ports A and B, and enable
        communication. 
        
        """

        self.reset_a()
        self.reset_b()

    def exposed_set_a_state(self, state):
        """ Set state of valves on port A.

        ARGUMENTS:
        state - 8 char long string of 1's and 0's. Represents the state of the
                valves (1 for open, 0 for closed).

        """
        state = state.encode('ascii').strip()
        self.daq.write("A" + chr(int(state, 2)))
        print "A set to %s" % state
        return ("Set state of valves on port A: %s" % state)

    def exposed_set_b_state(self, state):
        """ Set state of valves on port B.

        ARGUMENTS:
        state - 8 char long string of 1's and 0's. Represents the state of the
                valves (1 for open, 0 for closed).

        """
        state = state.encode('ascii').strip()
        self.daq.write("B" + chr(int(state, 2)))
        # logging.debug("B set to %s" % state)
        print "B set to %s" % state
        return ("Set state of valves on port B: %s" % state)

if __name__ == '__main__':
    from optparse import OptionParser
    from rpyc.utils.server import ThreadedServer

    # Parse options
    parser = OptionParser(version=version, usage=usage)
    parser.add_option('-p', '--port', action="store", type="string", 
            dest="PORT", help="Port number for server to listen on")
    parser.add_option('-d', '--device', action="store", type="string", 
            dest="DEVICE", help="Device file for the microcontroller")
    (options, args) = parser.parse_args()

    if options.PORT: PORT = options.PORT
    if options.DEVICE: DEVICE = options.DEVICE

    t = ThreadedServer(LBNCControllerService, port=PORT)
    t.start()
