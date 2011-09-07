# This is a link to the device. Avoids having to change /dev/ttyUSB* all the
# time.

__all__ = [
    'DEVICE',
    'BAUDRATE',
]

DEVICE = '/dev/serial/by-id/usb-FTDI_USB__-__Serial-if00-port0'
BAUDRATE = 9600
