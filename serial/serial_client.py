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

import rpyc
from constants import HOST, PORT

def set_states(a, b):
    # Connect and get main object
    connection = rpyc.connect_by_service("CONTROLLER")
    c = connection.root

    # Reset communication to microcontroller and set new states
    c.reset()
    return_value_a = c.set_a_state(a)
    return_value_b = c.set_a_state(b)

    # Close nicely, and relay feedback to caller
    connection.close()
    return return_value_a, return_value_b

if __name__ == '__main__':
    from random import choice
    make_string = lambda: ''.join([choice(['0', '1']) for i in range(8)])
    set_states(make_string(), make_string())
