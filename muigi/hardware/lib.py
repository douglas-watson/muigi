#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   lib.py - Contains shared code for modules of the Muigi hardware package.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 31 August 2011
#
#   LICENSE: GNU GPLv3
#
#################################################

'''

Muigi.hardware.lib
======================

Contains code shared by modules of the muigi hardware package, such as
exceptions or decorators.

'''

__all__ = [
    'ConnectionError',
    'needs_serial',
]

import sys
from serial import SerialException
import termios
import logging

##############################
# Exceptions
##############################

class ConnectionError(Exception):
    ''' Raised when connection to device is not opened. 
    
    This is usually fixed by calling Controller.connect().

    '''

    def __init__(self, device, msg=None):
        if msg:
            self.msg = msg
        else:
            self.msg = "Not connected to device %s" % device

    def __str__(self):
        print self.msg

##############################
# Useful Decorators 
##############################

def needs_serial(func):
    ''' Makes sure Controller is connected to the hardware device. Raises a
    ConnectionError otherwise. 
    
    Warning: can only be used in the Controller class, if it is written
    according to Muigi standards.

    '''

    def check_connection(*args, **kwargs):
        self = args[0]
        # Attempt to reconnect if connection is lost

        try:
            return_value = func(*args, **kwargs)
        except (OSError, SerialException, termios.error), e:
            # The connection was dropped somewhere along the line
            print e
            logging.debug("Connection lost calling %s(%s)," + \
                          "attempting reconnection", func.__name__,
                          str(args[1:]))
            if self.reconnect():
                # and try again...
                logging.debug("Reconnected, now trying again:")
                return_value = check_connection(*args, **kwargs)
            else:
                logging.debug("Reconnection Impossible. Bye bye")
                sys.exit(1) # TODO get rid of this!
            logging.debug(return_value)
            return return_value
        else:
            return return_value

    return check_connection
