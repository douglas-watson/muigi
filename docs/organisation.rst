Framework organisation
======================

Muigi is separated into three components: ``muigi.hardware``,
``muigi.applications``, and ``muigi.web``. All three work together to provide a
web interface to control microfluidic chips, in a flexible manner. The hardware
component contains drivers for various microcontrollers used to drive solenoid
valves in microfluidics. The drivers provide a standard set of functions that
other components can then build on, regardless of the specific microcontroller.
The applications layer then defines a set of functions for individual
applications. 

.. toctree::
    applications
    hardware
    web
