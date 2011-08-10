#!/bin/bash
#
#  start_rpc.sh - Starts the RPyC registry server and the serial driver; only
#  inteded for development.
#
#	AUTHOR: Douglas Watson <douglas@watsons.ch>
#
#	DATE: 10 August 2011
#
########################################

# activate virtualenv
source env/bin/activate

# Start RPyC registry server in the background
# Note: stopping it is a hack. Find the process id by running 
# `ps -elf | grep rpyc` 
python env/bin/rpyc_registry.py &

# Start serial driver (just wait for a few seconds, for the registry to init.)
cd serial/
sleep 3
python serial_driver.py
