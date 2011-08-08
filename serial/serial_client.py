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
#   LICENSE: GNU GPL
#
#################################################

import rpyc
from constants import HOST, PORT

def set_states(a, b):
    connection = rpyc.connect(HOST, PORT)
    c = connection.root
    c.reset()
    return_value_a = c.set_a_state(a)
    return_value_b = c.set_a_state(b)
    connection.close()
    return return_value_a, return_value_b

if __name__ == '__main__':
    from random import choice
    make_string = lambda: ''.join([choice(['0', '1']) for i in range(8)])
    set_states(make_string(), make_string())
