#!/usr/bin/env python
# -*- coding: UTF8 -*-

"""
The Muigi hardware sub-package
==============================

Communicate with microfluidics hardware via serial.

The modules here are drivers for different controllers for microfluidics. Each
driver implements a set of hardware-specific, low-level functions (check the
individual docs for those), as well as a set of standard functions. If the
class representing the microcontroller is importer as Controller, the standard
methods are::

    from your_driver import YourController as Controller

    c = Controller('/dev/ttyUSB1' [, baudrate])) # initializes connection
    c.read_states()                 # return state of all valves
    c.set_states(array_of_states)   # set the valves open or closed
    c.read_state(N)                 # return state of valve N
    c.set_state(N, state)           # set state of valve N (state is 1 or 0)

This allows code to be ported to a different hardware setup just by changing
the import line::

    # swap this:
    from old_driver import OldHardware as Controller
    # ...for that:
    from new_driver import NewHardware as Controller

"""
