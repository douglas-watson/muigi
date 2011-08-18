#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   easydaqUSB24mx_driver.py - 'driver' for easyDAQ USB24mx USB relay card
#
#   PURPOSE: 
#       Provide an RPC interface to the DAQ, as well as high
#       level functions for operation of the microfluidic chip.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 18th August 2011
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

""" The easyDAQ driver

Provides an RPyC interface to control the EasyDAQ USB24Mx 24-relay USB card.
The card has three 'ports' (B, C, and D), each controlling eight relays, making
a total of twenty-four. Relays 1 to 8 are on port A, relays 9 to 16 on port B,
relays 17 to 24 on port C.

To connect to the driver, first ensure the RPyC Registry server is running,
then execute the driver. This starts a server, which can be connected to using:

>> import rpyc
>> service = rpyc.connect_by_service
>> daq = service.root

Please note that the terminology adapted (in terms of ports, bits, and
directions for example), are those used by EasyDAQ in their datasheet.

"""

usage = """

    easydaq24_driver.py [-p PORT] [-d DEVICE]

    If executed alone, start an RPC server, providing control over the LBNC
    microcontroller. If the RPyC name server is running, it will advertise the
    service "EASYDAQ" through the name server, allowing a connection to
    be established with the rpyc.connect_by_service("EASYDAQ") function.


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
import time

from lbnc_settings import PORT, DEVICE, BAUDRATE

version = 'pre-alpha'

class EasyDAQService(rpyc.Service):

    def on_connect(self):
        print "Connection received"
        self.daq = None # replaced later by self.exposed_open_serial()

        # Now I'm just using this method as an __init__ function
        self.ports = ['B', 'C', 'D']

    def on_disconnect(self):
        print "Connection closed"
        # Close serial port
        if self.daq is not None:
            self.daq.close()

    def exposed_open_serial(self):
        ''' Open serial connection to DAQ.
        
        This has to be implemented as a standalone method to send feedback to
        the user. The connection is closed automatically when client
        disconnects.
        
        ''' 

        try: 
            self.daq = serial.Serial(DEVICE, BAUDRATE) 
        except SerialException, e:
            raise SerialException(e) 
        return "Serial connection established."

    def exposed_serial_write(self, string):
        """ Directly write a string to the DAQ """

        print "Sending:", string
        self.daq.write(string)

    def exposed_serial_read(self, num_bytes):
        """ Directly read num_bytes from DAQ. Return the read bytes. """

        answer = self.daq.read(num_bytes)
        return answer

    def exposed_serial_flush(self):
        """ Flush serial input and output. Wait until all data is written """
        self.daq.flush()

    def exposed_set_all_to_output(self):
        """ Set all the relays to outputs. """

        for port in self.ports:
            self.exposed_set_directions(port, "00000000")

    def exposed_set_directions(self, port, directions):
        """ Set directions of a port's channels to input or output
        
        Arguments:
        * port - the letter addressing the port. Either 'B', 'C', or 'D'
        * directions - eight-character string of 1s and 0s, defining the state
                of each channel on the port. 1 = Input, 0 = Output. Addressed
                in reverse order: '01000000' set channel 7 to input, all others
                output.

        Returns:
        Nothing, the card provides no feedback.

        Raises:
        Raises a ValueError if one of the arguments is invalid.

        Examples:
        From the client side if r is the connection's root object (i.e this
        class)
        
        Set all bits on port B to output:
        >> r.set_directions('B', '00000000')

        Set bits 1-4 to outputs, 5-8 to inputs on port C:
        >> r.set_directions('C', '11110000')

        To control valves in the microfluidic application, the channels have to
        be set as outputs.

        """

        # Check arguments
        if port not in self.ports:
            raise ValueError("Port %s does not exist." % port)
        if len(directions) != 8:
            raise ValueError("Directions string must be 8 characters long.")
        # try to convert string to a character; raises ValueError if invalid
        dirs = chr(int(directions, 2))

        # Ports aren't adressed actually adressed by their letter;
        lookup = {'B': 'B', 'C': 'E', 'D': 'H'}
        # Set modes:
        print "Sending:", lookup[port] + directions
        time.sleep(0.01) # sleeping 10 ms prevents lost bytes
        self.daq.flushOutput()
        self.daq.write(lookup[port] + dirs)

    def exposed_set_states(self, port, states):
        """ Set the states of relays on a port, if they are set as active.

        Arguments:
        * port - the letter addressing the port. Either 'B', 'C', or 'D'    
        * states - eight-character string of 1s and 0s, defining the state
                of each relay on the port. 1 = Active, 0 = Inactive. Addressed
                in reverse order: '01000000' sets relay 7 to active, all others
                inactive.

        Returns:
        Nothing, the card does not return anything.

        Raises:
        Raises a ValueError if one of the arguments is invalid, such as a port
        that doesn't exist.

        """

        # Check arguments
        if port not in self.ports:
            raise ValueError("Port %s does not exist." % port)
        if len(states) != 8:
            raise ValueError("State string must be 8 characters long.")
        # try to convert string to a character; raises ValueError if invalid
        st = chr(int(states, 2))

        # For writing, we need to use different letters
        lookup = {'B': 'C', 'C': 'F', 'D': 'J'}

        # Set states:
        print "Sending:", lookup[port] + states, lookup[port] + st
        time.sleep(0.01) # sleeping 10 ms prevents lost bytes
        self.daq.flushOutput()
        self.daq.write(lookup[port] + st)

    def exposed_read_states(self, port):
        """ Reads the state of channels on one port

        Arguments:
        * port - The letter addressing the port, Either 'B', 'C', or 'D'.

        Returns:
        The value returned by the microcontroller, converted to a string of
        eight 1s or 0s (1 = Active, 0 = Inactive).

        Raises:
        ValueError if the specified port is not valid.

        """

        # check arguments
        if port not in self.ports:
            raise ValueError("Port %s does not exist." % port)

        lookup = {'B': 'A', 'C': 'D', 'D': 'G'}

        time.sleep(0.01) # sleeping 10 ms prevents lost bytes
        # Flush input; otherwise we could be reading an errant byte
        self.daq.flushInput()
        self.daq.flushOutput()
        # Request state of channels on that port
        self.exposed_serial_write(lookup[port] + "A")
        # And read response
        answer = self.exposed_serial_read(1)
        return "%08d" % int(bin(ord(answer))[2:])

if __name__ == '__main__':
    from optparse import OptionParser
    from rpyc.utils.server import ThreadedServer

    # Parse options
    parser = OptionParser(version=version, usage=usage)
    parser.add_option('-p', '--port', action="store", type="string", 
            dest="PORT", help="Port number for server to listen on")
    parser.add_option('-d', '--device', action="store", type="string", 
            dest="DEVICE", help="Device file for the microcontroller")
    parser.add_option('-b', '--baudrate', action="store", type="string", 
            dest="BAUDRATE", help="Baudrate for communication")
    (options, args) = parser.parse_args()

    if options.PORT: PORT = options.PORT
    if options.DEVICE: DEVICE = options.DEVICE
    if options.BAUDRATE: BAUDRATE = options.BAUDRATE

    t = ThreadedServer(EasyDAQService, port=PORT)
    t.start()
