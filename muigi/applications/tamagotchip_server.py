#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   tamagotchip.py - RPC interface for the Tamagotchip microfluidic game
#
#   PURPOSE: 
#       Provides an RPC interface to functions of the tamagotchip microfluidic
#       game. The web application can connect to this using the RPyC library,
#       and control the chip using high-level commands.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 5th September 2011
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

usage = """

    tamagotchip.py [-p PORT]

    If executed alone, start an RPC server, providing control over the
    tamagotchip game. If the RPyC name server is running, it will advertise the
    service "TAMAGOTCHIP" through the name server, allowing a connection to
    be established with the rpyc.connect_by_service() function.

"""

import sys
import rpyc
import types
import serial
from serial import SerialException
import logging

from muigi import __version__
# NOTE: change this line if you change the controller (whatever drives your
# solenoid valves)
from muigi.hardware.easydaq import USB24mx as Controller

class TamagotchipService(rpyc.Service):
    
    ''' Represents the Tamagotchip game. The available methods correspond to
    functions of the game. 
    
    Note that it uses by default the EasyDAQ USB24mx driver (this is
    hardcoded), and only uses the first twelve channels, as only twelve
    electronic valves are used on the hardware setup. 
    
    '''

    def on_connect(self):
        self.c = Controller() # use driver's defaults for config
        self.c.set_all_output()
        
    def on_disconnect(self):
        self.c.disconnect()

    def exposed_set_states(self, states):
        ''' Set the states of the 12 available valves 
        
        :param states: A 12 item-long list of integers, representing the state
            of each valve. Open is 1, closed is 0.
        :type states: list
        :raises TypeError: if `states` cannot be cast to a list.
        :raises ValueError: if length of `states` is inappropriate.
            
        '''

        states = list(states)

        if len(states) != 12:
            raise ValueError("'states' must be a 12 item-long list")

        try:
            self.c.set_states(states + [0] * 12) # close the last 12 valves
        except Exception, e:
            raise e # TODO not too sure what I'm catching yet.
        else:
            return "Valves set to %s" % str(states)


if __name__ == '__main__':
    from optparse import OptionParser
    from rpyc.utils.server import ThreadedServer
    from tamagotchip_settings import PORT

    # Parse options
    parser = OptionParser(version=__version__, usage=usage)
    parser.add_option('-p', '--port', action="store", type="string", 
            dest="PORT", help="Port number for server to listen on")
    (options, args) = parser.parse_args()

    if options.PORT: PORT = options.PORT

    t = ThreadedServer(TamagotchipService, port=PORT)
    t.start()
