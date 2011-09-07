#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   tamagotchip_client.py - Client for the Tamagotchip game
#
#   PURPOSE: 
#       Connect to the Tamagotchip server. Import this module from another
#       application that needs tamagotchip (the web interface, typically) to
#       avoid messing with RPC stuff.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 7th September 2011
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
tamagotchip_client.py
=====================

Connect to the Tamagotchip server. Import this module from another application
that needs tamagotchip (the web interface, typically) to avoid messing with RPC
stuff.

"""

usage = """

When executed on its own, sets the state passed on command line. Describe the
states as a concatenated string of 1s and 0s. If no state is given, set a
random state.

"""

import sys
import rpyc
from rpyc.utils.factory import DiscoveryError
from serial import SerialException

from muigi import __version__


def set_states(states):
    """ Connects to the server and sets the states of all twelve valves to the
    specified value

    :param states: twelve element-long array of ints, representing the states
        of each valve
    :type states: array of integers
    :return: A return code (0 for success, 1 for failure), and a feedback
        message (to be relayed to the user).

    """

    SUCCESS, FAIL = 0, 1 # Return codes, used by the web app

    try:
        # Connect to RPyC server and get main object
        connection = rpyc.connect_by_service("TAMAGOTCHIP")
        r = connection.root
    except DiscoveryError, e:
        return FAIL, "Serial interface daemon unreachable."
    except Exception, e:
        # Ugly hack to catch the SerialException, but only that one
        # Exceptions through RPyC are a little hard to track.
        if "SerialException" in e.args[0]:
            print e
            return FAIL, "Microcontroller unavailable."
        else:
            raise e
    else:
        # Reset communication to microcontroller and set new states
        msg = r.set_states(states)

        # Close nicely, and relay feedback to caller
        connection.close()
        return SUCCESS, msg

if __name__ == '__main__':
    from optparse import OptionParser
    from random import choice
    random_states = lambda: [choice(['0', '1']) for i in range(12)]

    parser = OptionParser(version=__version__)
    options, args = parser.parse_args()

    if args:
        states = list(args[0])
    else:
        states = random_states()

    # Set two random states, print feedback from driver, and exit.
    exit_code, feedback = set_states(states)
    print feedback
    sys.exit(exit_code)
