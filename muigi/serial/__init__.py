#!/usr/bin/env python
# -*- coding: UTF8 -*-

"""Communicate with microfluidics hardware via serial connections.

The python modules provide helper functions to communicate with the drivers. At
the moment, a single driver exists, to control LBNC's house-built
microcontroller. Eventually, each kind of supported controller will have its
own driver. The module thus contains a single client:

- lbnc_client.py

Check the client's documentation for the functions it provides.

The drivers are not meant to be imported into other python programs. When
executed, they start an RPyC server. The methods they expose via RPC allow
high-level control over the fluidic device.
"""
