#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   serial_driver.py - Provides an RPC interface to the microcontroller (through
#   serial)
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 8th August 2011
#
#   LICENSE: GNU GPL
#
#################################################

import rpyc
import serial

from constants import PORT, DEVICE

class ControllerService(rpyc.Service):

    def on_connect(self):
        print "Connection received"
        # Open serial port
        self.daq = serial.Serial(DEVICE)

    def on_disconnect(self):
        print "Connection lost"
        # Close serial port
        self.daq.close()

    def reset_a(self):
        """ Reset communication to valve A """
        self.daq.write("!A" + chr(0))

    def reset_b(self):
        """ Reset communication to valve B """
        self.daq.write("!B" + chr(0))

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
        self.reset_a()
        self.daq.write("A" + chr(int(state.strip(), 2)))
        return ("Set state of valves on port A: %s" % state)

    def exposed_set_b_state(self, state):
        """ Sets state of valves on port B.

        INPUT:

        state - 8 char long string of 1's and 0's. Represents the state of the
        valves (1 for open, 0 for closed).
        """
        self.reset_b()
        self.daq.write("B" + chr(int(state.strip(), 2)))
        return ("Set state of valves on port B: %s" % state)

if __name__ == '__main__':
    from rpyc.utils.server import ThreadedServer
    t = ThreadedServer(ControllerService, port=PORT)
    t.start()
