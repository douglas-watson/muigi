#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   easydaqUSB24mx_lib.py - library for easyDAQ USB24mx USB relay card
#
#   PURPOSE: 
#       Provide a set of functions to easily control the easyDAQ USB24mx
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 19th August 2011
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

""" The easyDAQ library

Provides an API to control the EasyDAQ USB24Mx 24-relay USB card.
The card has three 'ports' (B, C, and D), each controlling eight relays, making
a total of twenty-four. Relays 1 to 8 are on port A, relays 9 to 16 on port B,
relays 17 to 24 on port C.

To control the DAQ, create an instance of the Controller class, then establish
a connection, and start sending commands:

>> from easydaq24 import Controller
>> daq = Controller()
>> daq.connect()
>> daq.activate_channel(15) # activates channel 12
>> time.sleep(10)
>> daq.set_states([1] * 12 + [0] * 12) # activate first 12 channels.
>> daq.disconnect()

Please note that the terminology adapted (in terms of ports, channels, and
directions for example), are those used by EasyDAQ in their datasheet.

"""

import sys
import serial
from serial import SerialException
import time

version = 'pre-alpha'

class USB24mx():

    def __init__(self, device, baudrate=9600):
        self.ports = ['B', 'C', 'D']
        self._device = device
        self._baudrate = baudrate

        self.daq = None # replaced later by self.connect()
        """ A standard serial.Serial object """

        # Attempt connection:
        self.connect() # raises SerialException if connection fails


    def connect(self):
        ''' Open serial connection to DAQ.
        
        A SerialException will be raised if the DAQ is not available.

        ''' 

        self.daq = serial.Serial(self._device, self._baudrate) 
        if not self.daq.isOpen():
            raise SerialException("Could not open device '%s'" % self._device)

    def disconnect(self):
        # TODO: figure out how to execute this automatically on shutdown.
        # Close serial port
        if self.daq is not None:
            self.daq.close()

    def set_all_output(self):
        """ Set all the relays to outputs. """

        for port in self.ports:
            self.set_port_directions(port, "00000000")

    def set_all_input(self):
        """ Set all the relays to inputs. """

        for port in self.ports:
            self.set_port_directions(port, "11111111")

    def set_port_directions(self, port, directions):
        """ Set directions of a port's channels to input or output (low-level)
        
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
        time.sleep(0.01) # sleeping 10 ms prevents lost bytes
        # self.daq.flushOutput()
        self.daq.write(lookup[port] + dirs)

    def set_port_states(self, port, states):
        """ Set the states of relays on a port, if they are set as active.
        (low-level)

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

        # Writing instructions to ports starts by these letters:
        lookup = {'B': 'C', 'C': 'F', 'D': 'J'}

        # Set states:
        time.sleep(0.01) # sleeping 10 ms prevents lost bytes
        # self.daq.flushOutput()
        self.daq.write(lookup[port] + st)

    def read_port_states(self, port):
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
        self.daq.write(lookup[port] + "A")
        # And read response
        answer = self.daq.read(1)
        return "%08d" % int(bin(ord(answer))[2:])

    def set_state(self, relay, state):
        ''' Set the state of a single relay (1 for active, 0 for inactive)

        Arguments:
        relay - Number of the relay, from 1 to 24 (included)
        state - 1 for active, 0 for inactive

        '''

        states = self.read_states()
        states[relay - 1] = state
        self.set_states(states)

    def set_states(self, states):
        ''' Set the states of all 24 relays at once 
        
        Arguments:
        states - an array of 24 integers, either 1 (active) or 0 (inactive).
            Note that element 0 of the array corresponds to channel 1, etc.
        
        '''
        
        # first eight go to port B, next to port C, last eight to port D.
        self.set_port_states('B', ''.join(str(i) for i in states[:8]))
        self.set_port_states('C', ''.join(str(i) for i in states[8:16]))
        self.set_port_states('D', ''.join(str(i) for i in states[16:]))


    def read_state(self, relay):
        ''' Return the state of a single channel. Relays indexed from 1. '''

        return self.read_states()[relay-1]

    def read_states(self):
        ''' Return the states of all 24 relays as an array of ints. '''

        states = []
        for port in self.ports:
            states += [int(i) for i in list(self.read_port_states(port))]

        return states

if __name__ == '__main__':
    # run some simple test code
    import time
    from optparse import OptionParser

    p = OptionParser(version=version)
    p.add_option('-b', '--baudrate', action="store", type="string", 
            dest="baudrate", default=9600, help="Baudrate for communication")
    opts, args = p.parse_args()

    if args:
        device = args[0]
    else:
        p.print_help()
        sys.exit(1)
        
    c = Controller(device, opts.baudrate)
    c.connect()

    for port in c.ports:
        c.set_port_directions(port, "00000000")

    for i in range(8):
        state = ''.join(str(int(i == k)) for k in range(8))
        for port in c.ports:
            c.set_port_states(port, state)
        time.sleep(0.2)
