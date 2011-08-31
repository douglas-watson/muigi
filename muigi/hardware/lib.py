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

def needs_serial_new(func):

    def outFunc(*args, **kwargs):
        self = args[0]
        if self.daq.isOpen():
            func(*args, **kwargs)

    return outFunc


def needs_serial(func):
    ''' Makes sure Controller is connected to the hardware device. Raises a
    ConnectionError otherwise. 
    
    Warning: can only be used in the Controller class, if it is written
    according to Muigi standards.

    '''

    def check_connection(*args, **kwargs):
        self = args[0]
        # Attempt to reconnect if connection is lost
        if not self.daq.isOpen():
            with open('/home/douglas/Desktop/DEBUG2', 'a') as fo:
                fo.write("Connection lost when calling %s. Reconnecting..." %
                         func.__name__)
            self.connect()
        return func(*args, **kwargs)

    return check_connection
