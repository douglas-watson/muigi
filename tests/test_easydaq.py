#!/usr/bin/env python
# -*- coding: UTF8 -*-
#
#   Test the easydaq library. Meant to be used with Nose testing framework.
#
#   AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#   DATE: started on 19th August 2011
#
#   LICENSE: GNU GPLv3
#
#################################################

from random import randint

import nose
from nose.tools import raises

from muigi.hardware.easydaq import USB24mx
from muigi.hardware.easydaq_settings import DEVICE
from muigi.hardware.lib import ConnectionError, needs_serial

class testUSB24mx:

    def setUp(self):
        self.c = USB24mx(DEVICE)
        self.c.connect()

        # reset all relays to off
        self.c.set_all_output()
        self.c.set_states([0] * 24)

    def tearDown(self):
        self.c.set_states([0] * 24)
        self.c.disconnect()

    def test_needs_serial(self):
        ''' Disconnects, and runs a fake function that 'needs serial'. The
        connection should be open again after executing that function. '''

        @needs_serial
        def foo(self):
            # note: "self" has to be the controller instance
            ''' Raises a SerialError if connection is not open '''
            if not self.daq.isOpen or not self.is_available():
                print "Serial not available"
                raise SerialError("Serial connection closed")

        self.c.disconnect()
        assert not self.c.daq.isOpen()

        foo(self.c) # says it needs serial, so the decorator should open it.
        assert self.c.daq.isOpen()

    def test_port_b(self):
        ''' Write random data to port B, and read it back (five times). The
        data read back should match what was written. '''

        rand_data = lambda N: ''.join([str(randint(0, 1)) for i in range(N)])
        self.c.set_port_directions("B", "00000000")
        for i in range(5):
            data = rand_data(8)
            self.c.set_port_states("B", data)
            data_back = self.c.read_port_states("B")

            assert data_back == data

    def test_port_c(self):
        ''' Write random data to port C, and read it back (five times). The
        data read back should match what was written. '''

        rand_data = lambda N: ''.join([str(randint(0, 1)) for i in range(N)])
        self.c.set_port_directions("C", "00000000")
        for i in range(5):
            data = rand_data(8)
            self.c.set_port_states("C", data)
            data_back = self.c.read_port_states("C")

            assert data_back == data

    def test_port_d(self):
        ''' Write random data to port D, and read it back (five times). The
        data read back should match what was written. '''

        rand_data = lambda N: ''.join([str(randint(0, 1)) for i in range(N)])
        self.c.set_port_directions("D", "00000000")
        for i in range(5):
            data = rand_data(8)
            self.c.set_port_states("D", data)
            data_back = self.c.read_port_states("D")

            assert data_back == data

    def test_set_states(self):
        ''' Set states of all 24 valves from a random array, and read it back.
        It should be the same. Also covers the read_states method. '''

        rand_data = lambda N: [randint(0, 1) for i in range (N)]
        self.c.set_all_output()

        # Do it ten times. The clicking sounds cool.
        for i in range(10):
            data = rand_data(24)
            self.c.set_states(data)
            data_back = self.c.read_states()

        assert data == data_back

    def test_set_state(self):
        ''' Set state of a single valve, check the read back is the same'''

        # For each channel and both states, one by one
        self.c.set_all_output()

        for chan in range(1, 25):
            self.c.set_state(chan, 1)
            assert self.c.read_state(chan) == 1

            self.c.set_state(chan, 0)
            assert self.c.read_state(chan) == 0
