#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   easydaqUSB24mx_client.py - test client for the EasyDAQ USB card 
#
#   PURPOSE: Just test the driver
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 18 August 2011
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
    easydaqUSB24mx_client.py

A debugging script for the EasyDAQ USB24mx driver. When run alone, it will
sequentially activate each relay, for all three ports at the same time (check
for LEDs switching on, on the far side of the board).

"""

import rpyc
import time

def flash_channels(r):
    """ Open then close each channel sequentially, for all ports at once. """
    ports = ['B', 'C', 'D']
    # Set all channels as outputs
    r.set_all_to_output()

    # Activate outputs one by one, every half second.
    for i in range(8):
        state = ''.join(str(int(k == i)) for k in range(8))
        for port in ports:
            r.set_states(port, state)
        time.sleep(0.5)

def read_channel(r):
    """ Read the state of channels """

    print r.read_states('B')
    print r.read_states('C')
    print r.read_states('D')

if __name__ == '__main__':
    s = rpyc.connect_by_service("EASYDAQ")
    r = s.root
    r.open_serial()

    flash_channels(r)
    read_channel(r)

    s.close()




