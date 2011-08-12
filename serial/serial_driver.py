#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   serial_driver.py - Provides an RPC interface to the microcontroller, as
#   well as high level functions for operation of the microfluidic chip.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 8th August 2011
#
#   LICENSE: GNU GPLv3
#
#   Copyright (C) 2011 Douglas Watson
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#  
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
# 
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################

import rpyc
import serial
from serial import SerialException
import logging

from constants import PORT, DEVICE

class ControllerService(rpyc.Service):

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
        ''' Open serial port to DAQ 
        
        I have to implement this as a standalone method to send feedback to the
        user. '''
        try:
            self.daq = serial.Serial(DEVICE)
        except SerialException, e:
            # raise it on the client side? TODO check this is necessary
            raise SerialException(e)
        return "Serial connection established."


    def exposed_reset(self):
        """ Resets state of all valves on ports A and B, and enables
        communication """

        self.reset_a()
        self.reset_b()

    def exposed_set_a_state(self, state):
        """ Sets state of valves on port A.

        INPUT:

        state - 8 char long string of 1's and 0's. Represents the state of the
        valves (1 for open, 0 for closed).
        """
        state = state.encode('ascii').strip()
        self.daq.write("A" + chr(int(state, 2)))
        print "A set to %s" % state
        return ("Set state of valves on port A: %s" % state)

    def exposed_set_b_state(self, state):
        """ Sets state of valves on port B.

        INPUT:

        state - 8 char long string of 1's and 0's. Represents the state of the
        valves (1 for open, 0 for closed).
        """
        state = state.encode('ascii').strip()
        self.daq.write("B" + chr(int(state, 2)))
        # logging.debug("B set to %s" % state)
        print "B set to %s" % state
        return ("Set state of valves on port B: %s" % state)

if __name__ == '__main__':
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(ControllerService, port=PORT)
    t.start()
