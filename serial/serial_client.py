#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   serial_client.py - Connect to serial driver, to remotely control the
#   microfluidic chip 
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

import sys
import rpyc
from rpyc.utils.factory import DiscoveryError
from constants import HOST, PORT
from serial import SerialException

def set_states(a, b):
    """ 
    Attempts to set the ports valves on ports A and B to the specified values.

    INPUT
    both arguments are binary numbers as strings, each bit represents the 
    state of a valve
    a - state of port A
    b - same, for port B

    RETURNS
    A status code, and a message intended for relaying to the end user.
    Status codes:
    0 - Success
    1 - Serial Error (any kind)
    Any other kind of exception results in raising an actual exception.
    Other exceptions may appear. In any case, they will return a status code
    higher than 0.
    """
    SUCCESS, FAIL = 0, 1
    try:
        # Connect to RPyC server and get main object
        connection = rpyc.connect_by_service("CONTROLLER")
        r = connection.root
        r.open_serial()
    except DiscoveryError, e:
        return FAIL, "Serial interface daemon unreachable."
    except Exception, e:
        # Ugly hack to catch the SerialException, but only that one
        # Exceptions through RPyC are a little hard to track.
        if "SerialException" in e.args[0]:
            return FAIL, "Microcontroller unavailable."
        else:
            raise e
    else:
        # Reset communication to microcontroller and set new states
        r.reset()
        return_value_a = r.set_a_state(a)
        return_value_b = r.set_b_state(b)

        # Close nicely, and relay feedback to caller
        connection.close()
        return SUCCESS, "%s %s" % (return_value_a, return_value_b)

if __name__ == '__main__':
    from random import choice
    make_string = lambda: ''.join([choice(['0', '1']) for i in range(8)])
    state, feedback = set_states(make_string(), make_string())
    print feedback
    sys.exit(state)
