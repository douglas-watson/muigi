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

from muigi.serial.easydaq import USB24mx as Controller
from muigi.serial.lbnc_settings import DEVICE

class testController:

    def setUp(self):
        self.c = Controller(DEVICE)
        self.c.connect()

    def tearDown(self):
        self.c.disconnect()

    def test_connection_handling(self):
        ''' Make sure errors are handled cleanly if connection is closed. '''

        # TODO
        assert False

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

        data = rand_data(24)
        self.c.set_states(data)
        data_back = self.c.read_states()

        print data
        print data_back
        assert data == data_back

    def test_set_state(self):
        ''' Set state of a single valve, check the read back is the same'''

        # For each channel and both states, one by one
        # TODO fix the indexing order
        print ("Fix the indexing order!")
        assert False

        for chan in range(1, 25):
            self.c.set_state(chan, 1)
            assert self.c.read_state(chan) == 1

            self.c.set_state(chan, 0)
            assert self.c.read_state(chan) == 0
