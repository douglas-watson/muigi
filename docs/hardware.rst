Drivers
=======

What Muigi calls a "driver" is not actually a low-level kernel driver, but
rather a collection of methods that helps set up communication with your
microfluidics hardware (be it a DAQ, or a microcontroller), and then control
it. It should typically provide both low-level and high-level commands: the
low-level ones set the states of the valves one by one, the higher level ones
carry a function, such as flushing the chip, or whatever your experiments
usually call for.

There are currently a two drivers available: 

#. the LBNC driver, for LBNC's home-built valve driver.
#. EasyDAQ for the EasyDAQ USB24mx, which could be easily ported to other EasyDAQ relay cards 

.. automodule:: muigi.hardware
    :members:

Writing your own driver
-----------------------
.. todo: how to write your own driver.

LBNC driver
-----------

.. automodule:: muigi.hardware.lbnc_driver
    :members:

.. automodule:: muigi.hardware.lbnc_client
    :members:

EasyDAQ driver
--------------

.. automodule:: muigi.hardware.easydaq
    :members:
